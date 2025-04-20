"use client";

import { useState } from "react";
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [filteredImageUrl, setFilteredImageUrl] = useState(null);
  const [selectedFilter, setSelectedFilter] = useState("normal");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const filters = [
    { value: "neblina", label: "Neblina" },
    { value: "noche", label: "Noche" },
    { value: "lluvia", label: "Lluvia" },
    { value: "sol", label: "Sol" },
    { value: "nieve", label: "Nieve" },
  ];

  const filterEndpoints = {
    neblina: "/filter?condition=neblina",
    noche: "/filter?condition=noche",
    lluvia: "/filter?condition=lluvia",
    sol: "/filter?condition=sol",
    nieve: "/filter?condition=nieve",
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      
      // Create preview URL for the original image
      const fileUrl = URL.createObjectURL(file);
      setPreviewUrl(fileUrl);
      
      // Reset filtered image when new file is selected
      setFilteredImageUrl(null);
      setError(null);
    }
  };

  const handleFilterChange = (e) => {
    setSelectedFilter(e.target.value);
    // Reset filtered image when filter changes
    setFilteredImageUrl(null);
  };

  const applyFilter = async () => {
    if (!selectedFile) {
      setError("Por favor selecciona una imagen primero");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append("image", selectedFile);
      
      // Determine which API endpoint to use based on selected filter
      const endpoint = filterEndpoints[selectedFilter];
      const apiUrl = `http://localhost:8000${endpoint}`;
      
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }
      
      // Create URL from response blob
      const blob = await response.blob();
      const filteredUrl = URL.createObjectURL(blob);
      setFilteredImageUrl(filteredUrl);
    } catch (err) {
      console.error("Error applying filter:", err);
      setError(`Error al aplicar filtro: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>Filtros Atmosféricos</h1>
        
        <div className={styles.controls}>
          <div className={styles.inputGroup}>
            <label htmlFor="image-upload" className={styles.label}>
              Selecciona una imagen:
            </label>
            <input
              id="image-upload"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className={styles.fileInput}
            />
          </div>
          
          <div className={styles.inputGroup}>
            <label htmlFor="filter-select" className={styles.label}>
              Selecciona un filtro:
            </label>
            <select
              id="filter-select"
              value={selectedFilter}
              onChange={handleFilterChange}
              className={styles.select}
            >
              {filters.map((filter) => (
                <option key={filter.value} value={filter.value}>
                  {filter.label}
                </option>
              ))}
            </select>
          </div>
          
          <button 
            onClick={applyFilter} 
            disabled={!selectedFile || loading}
            className={styles.button}
          >
            {loading ? "Procesando..." : "Aplicar Filtro"}
          </button>
        </div>
        
        {error && <div className={styles.error}>{error}</div>}
        
        <div className={styles.imageContainer}>
          {previewUrl && (
            <div className={styles.imageBox}>
              <h2>Imagen Original</h2>
              <div className={styles.imageWrapper}>
                <img
                  src={previewUrl}
                  alt="Imagen Original"
                  className={styles.image}
                />
              </div>
            </div>
          )}
          
          {filteredImageUrl && (
            <div className={styles.imageBox}>
              <h2>Imagen con Filtro {selectedFilter}</h2>
              <div className={styles.imageWrapper}>
                <img
                  src={filteredImageUrl}
                  alt="Imagen Filtrada"
                  className={styles.image}
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

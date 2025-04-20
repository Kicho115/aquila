from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import io
from filtros import adaptive_filter, enhance_image, reduce_rain_noise, gamma_correction, enhance_winter_image

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/filter")
async def apply_filter(image: UploadFile = File(...), condition: str = "normal"):
    """
    Apply the appropriate filter based on the atmospheric condition.
    Conditions: neblina, noche, lluvia, sol, nieve, normal
    """
    # Validate the file is an image
    content_type = image.content_type
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    # Read the image
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    # Apply filter
    filtered_img = adaptive_filter(img, condition)
    
    # Convert the filtered image back to bytes
    success, encoded_img = cv2.imencode('.png', filtered_img)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode the filtered image")
    
    # Return the image as a response
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")


@app.post("/filter/enhance")
async def apply_enhance(image: UploadFile = File(...)):
    """Apply the enhance_image filter to improve night/low light images"""
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    filtered_img = enhance_image(img)
    success, encoded_img = cv2.imencode('.png', filtered_img)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode the filtered image")
    
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")


@app.post("/filter/rain")
async def apply_rain_filter(image: UploadFile = File(...)):
    """Apply the rain noise reduction filter"""
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    filtered_img = reduce_rain_noise(img)
    success, encoded_img = cv2.imencode('.png', filtered_img)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode the filtered image")
    
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")


@app.post("/filter/gamma")
async def apply_gamma(image: UploadFile = File(...)):
    """Apply the gamma correction filter (for sun/bright conditions)"""
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    filtered_img = gamma_correction(img)
    success, encoded_img = cv2.imencode('.png', filtered_img)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode the filtered image")
    
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")


@app.post("/filter/winter")
async def apply_winter_filter(image: UploadFile = File(...)):
    """Apply the winter/snow enhancement filter"""
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    filtered_img = enhance_winter_image(img)
    success, encoded_img = cv2.imencode('.png', filtered_img)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode the filtered image")
    
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")
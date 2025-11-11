@app.post("/Extract-Jantung")
async def extract_jantung(file: UploadFile = File(...)):
    try:
        # Simulating processing
        file_contents = await file.read()
        logging.info(f"File {file.filename} uploaded successfully with size {len(file_contents)} bytes.")
        
        # Instead of calling jantung.py, just simulate processing and return a success response
        return JSONResponse({"status": "success", "message": "File processed successfully."})
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500})

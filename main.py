from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from jantung import process_jantung_data
from ranap import process_ranap_data
from resumemedis import process_resumemedis_data
import os
import io
import tempfile

app = FastAPI(title="Extraction APIs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Extraction APIs"}

# Jantung extraction endpoint
@app.post("/Extract-Jantung")
async def extract_jantung(file: UploadFile = File(...)):
    try:
        # Create a temporary directory to store the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, dir='/tmp') as tmp_file:
            input_path = tmp_file.name
            with open(input_path, "wb") as f:
                f.write(await file.read())

        # Define the output path in the same temporary directory
        output_path = input_path.replace("uploaded_", "processed_")

        # Process the file
        process_jantung_data(input_path, output_path)
        
        # Read the processed file into memory
        with open(output_path, mode="r", encoding="utf-8") as file:
            csv_content = file.read()

        # Return the processed CSV file as a download
        return StreamingResponse(io.StringIO(csv_content), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={os.path.basename(output_path)}"})

    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

# Ranap extraction endpoint
@app.post("/Extract-Ranap")
async def extract_ranap(file: UploadFile = File(...)):
    try:
        # Use the temporary directory provided by Vercel
        with tempfile.NamedTemporaryFile(delete=False, dir='/tmp') as tmp_file:
            input_path = tmp_file.name
            with open(input_path, "wb") as f:
                f.write(await file.read())

        # Define the output path in the temporary directory as well
        output_path = input_path.replace("uploaded_", "processed_")
        
        # Process the file
        process_ranap_data(input_path, output_path)

        # Read the processed file into memory
        with open(output_path, mode="r", encoding="utf-8") as file:
            csv_content = file.read()

        # Return the processed CSV file as a download
        return StreamingResponse(io.StringIO(csv_content), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={os.path.basename(output_path)}"})

    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

# Resume Medis extraction endpoint
@app.post("/Extract-ResumeMedis")
async def extract_resumemedis(file: UploadFile = File(...)):
    try:
        # Use the temporary directory provided by Vercel
        with tempfile.NamedTemporaryFile(delete=False, dir='/tmp') as tmp_file:
            input_path = tmp_file.name
            with open(input_path, "wb") as f:
                f.write(await file.read())

        # Define the output path in the temporary directory as well
        output_path = input_path.replace("uploaded_", "processed_")
        
        # Process the file
        process_resumemedis_data(input_path, output_path)

        # Read the processed file into memory
        with open(output_path, mode="r", encoding="utf-8") as file:
            csv_content = file.read()

        # Return the processed CSV file as a download
        return StreamingResponse(io.StringIO(csv_content), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={os.path.basename(output_path)}"})

    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)



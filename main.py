import os
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from jantung import process_jantung_data
from ranap import process_ranap_data
from resumemedis import process_resumemedis_data

app = FastAPI()

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

# Helper function to handle file processing
def handle_file(file: UploadFile, process_function, prefix: str):
    try:
        # Save the uploaded file to the /tmp directory in Vercel
        input_path = f"/tmp/uploaded_{file.filename}"
        with open(input_path, "wb") as f:
            f.write(file.file.read())
        
        # Set the output path for the processed file in /tmp directory
        output_path = f"/tmp/processed_{prefix}_{file.filename}"
        
        # Process the file using the corresponding function
        process_function(input_path, output_path)

        # Read the processed file
        with open(output_path, mode="r", encoding="utf-8") as file:
            csv_content = file.read()

        # Clean up the temporary files
        os.remove(input_path)
        os.remove(output_path)

        # Return the processed CSV file as a response
        return StreamingResponse(io.StringIO(csv_content), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={output_path}"})

    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)


# Medical CSV Extraction System

This project consists of a **FastAPI backend** and a simple **HTML/JS frontend** for processing raw medical CSV exports and converting them into fully cleaned, structured datasets.  
It supports extraction and transformation for **three medical record types**:

- **Jantung** — Heart / Outpatient examination  
- **Ranap** — Inpatient records  
- **Resume Medis** — Medical summary  

Each processor module removes unnecessary EMR noise, normalizes values, and uses the **Google Gemini API** to extract structured medical information.

---

## Repository Links

- **Frontend:** https://github.com/RandomKings/medical_extraction_frontend.git  
- **Backend:** https://github.com/RandomKings/Medical_extraction_backend.git  

---

## Project Structure

```
.
├── main.py                # FastAPI application
├── jantung.py             # Processor for Jantung CSV files
├── ranap.py               # Processor for Ranap CSV files
├── resumemedis.py         # Processor for Resume Medis CSV files
├── requirements.txt       # Backend dependencies
└── .env                   # Gemini API key (excluded from repo)
```

---

# Installation Guide

## Frontend Setup

### Option A — Run locally (simplest)
1. Open the frontend GitHub repository  
2. Download the HTML file 
3. Open in any browser — no build step required
   Note - When running backend locally, change the api url in the HTML to local.
### Option B — Deploy the frontend
Upload the HTML files to:
- Netlify  
- Vercel  
(or any static hosting provider)

---

## Backend Setup
### Option A — Run locally (simplest)
### 1. Clone the backend repository
```bash
git clone https://github.com/RandomKings/Medical_extraction_backend.git
cd Medical_extraction_backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
```
GEMINI_API_KEY=your_api_key_here
```

---

# Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URLs:

- **API Base:** http://127.0.0.1:8000  
- **Swagger Docs:** http://127.0.0.1:8000/docs  

---
### Option B — Deploy the backend
1. Upload the whole folder into your own github repository.
2. Go to vercel and import the github, making sure to choose FastApi framework(Default)
3. once it is deployed, copy the link
4. Go to the frontend and replace the api url with the provided link



# Processing Pipeline Overview

## 1. Column Cleanup
- Removes nested and irrelevant EMR fields  
- Strips metadata (UUIDs, timestamps, flags)  
- Removes personal identifiers  

## 2. AI-Assisted Extraction (Google Gemini)
Structured extraction of:
- Vitals (nadi, suhu, SPO2, etc.)  
- Blood pressure (systolic & diastolic)  
- Chief complaints (keluhan utama)  

## 3. Value Normalization
- Cleans number formatting  
- Standardizes units  
- Renames fields for clarity:
  - `O` → `detailPemeriksaan`  
  - `S` → `detailKeluhan`  
  - `P` → `detailPengobatan`  

## 4. Output
Produces a final, clean CSV ready for analysis.

---

# Environment Variables

```
GEMINI_API_KEY=your_gemini_api_key
```

---

# Requirements

```
fastapi
uvicorn
pandas
numpy
google-genai
python-dotenv
```

---


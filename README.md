# Medical CSV Extraction System

A comprehensive data processing solution featuring a **FastAPI backend** and **HTML/JavaScript frontend** designed to transform raw medical CSV exports into structured, analysis-ready datasets. The system intelligently processes three distinct medical record types while leveraging AI-powered extraction for accurate data normalization.

## 📋 Table of Contents

- [Overview](#overview)
- [Supported Record Types](#supported-record-types)
- [Repository Links](#repository-links)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Processing Pipeline](#processing-pipeline)
- [Screenshots](#screenshots)
---

## Overview

The Medical CSV Extraction System automates the conversion of raw electronic medical record (EMR) exports into clean, structured datasets. By utilizing the Google Gemini API for intelligent data extraction, the system removes unnecessary EMR metadata, normalizes medical values, and produces standardized output suitable for analysis and reporting.

## Supported Record Types

### 1. Jantung (Cardiac/Outpatient Examination)
Processes cardiovascular and general outpatient examination records including vital signs, physical examinations, and treatment plans.

### 2. Ranap (Inpatient Records)
Handles comprehensive inpatient admission records, including daily progress notes, treatment protocols, and discharge summaries.

### 3. Resume Medis (Medical Summary)
Extracts and structures condensed medical summaries, diagnoses, and treatment outcomes.

## Repository Links

- **Frontend Repository**: [medical_extraction_frontend](https://github.com/RandomKings/medical_extraction_frontend.git)
- **Backend Repository**: [Medical_extraction_backend](https://github.com/RandomKings/Medical_extraction_backend.git)
- **Live Demo**: [https://medical-extraction-frontend.vercel.app/](https://medical-extraction-frontend.vercel.app/)

## Project Structure

```
Medical_extraction_backend/
├── main.py                # FastAPI application entry point
├── jantung.py             # Cardiac/Outpatient record processor
├── ranap.py               # Inpatient record processor
├── resumemedis.py         # Medical summary processor
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration (not tracked)
└── README.md              # Project documentation
```

---

## Installation

### Frontend Setup

#### Option A: Local Deployment (Recommended for Development)

1. Clone the frontend repository:
   ```bash
   git clone https://github.com/RandomKings/medical_extraction_frontend.git
   cd medical_extraction_frontend
   ```

2. Open `index.html` in your preferred web browser
   - No build process or dependencies required
   - For local backend testing, update the API URL in the HTML file

#### Option B: Production Deployment

Deploy to any static hosting provider:

**Netlify:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

**Vercel:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

---

### Backend Setup

#### Option A: Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RandomKings/Medical_extraction_backend.git
   cd Medical_extraction_backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Start the development server:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API:**
   - **API Base URL**: `http://127.0.0.1:8000`
   - **Interactive Documentation**: `http://127.0.0.1:8000/docs`

#### Option B: Production Deployment (Vercel)

1. **Prepare your repository:**
   ```bash
   # Fork or upload to your GitHub account
   git clone https://github.com/RandomKings/Medical_extraction_backend.git
   cd Medical_extraction_backend
   git remote set-url origin https://github.com/YOUR_USERNAME/Medical_extraction_backend.git
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Navigate to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Import Project"
   - Select your GitHub repository
   - Choose **FastAPI** as the framework (or leave as default)
   - Add environment variables in the Vercel dashboard:
     - `GEMINI_API_KEY`: Your Google Gemini API key
   - Deploy

3. **Update frontend configuration:**
   - Copy your Vercel deployment URL
   - Update the API endpoint in your frontend HTML file

---

## Usage

### Web Interface

1. Navigate to the frontend URL (local or deployed)
2. Select the medical record type (Jantung, Ranap, or Resume Medis)
3. Upload your CSV file
4. Click "Process" to initiate extraction
5. Download the cleaned, structured CSV output

### API Integration

---

## Processing Pipeline

### 1. Data Ingestion & Validation
- Validates CSV structure and encoding
- Identifies record type and applicable processing rules

### 2. Column Cleanup & Sanitization
- Removes nested JSON structures and redundant EMR fields
- Strips metadata (UUIDs, timestamps, system flags)
- Eliminates personal identifiers for privacy compliance

### 3. AI-Assisted Structured Extraction
Utilizes Google Gemini API to extract:
- **Vital Signs**: Heart rate (nadi), temperature (suhu), SpO2, respiratory rate
- **Blood Pressure**: Systolic and diastolic measurements
- **Chief Complaints**: Primary symptoms (keluhan utama)
- **Clinical Observations**: SOAP note components

### 4. Value Normalization & Standardization
- Cleans numeric formatting (removes commas, standardizes decimals)
- Converts and standardizes measurement units
- Renames fields for consistency:
  - `O` → `detailPemeriksaan` (Objective findings)
  - `S` → `detailKeluhan` (Subjective complaints)
  - `P` → `detailPengobatan` (Plan/Treatment)
  - `A` → `detailAssessment` (Assessment/Diagnosis)

### 5. Output Generation
Produces a cleaned, structured CSV file optimized for:
- Statistical analysis
- Data visualization
- Machine learning pipelines
- Regulatory reporting

---

## Screenshots

### Frontend Interface

<!-- Add your screenshots here -->

**Upload Interface:**
![Upload Interface](https://github.com/user-attachments/assets/ce4fccc0-0991-4bbf-b5a8-3900ab32ab71)

*CSV file upload interface*

**Results Download:**
![Results Download](https://github.com/user-attachments/assets/18d4c7fd-8bc6-493c-a28f-a61c214f7093)

*Successfully processed data ready for download*

### API Documentation

**Swagger UI:**
![Swagger UI](https://github.com/user-attachments/assets/6c11a2d1-9f42-4ad0-8f28-ffc0ac27d694)

*Interactive API documentation at /docs endpoint*

---

## Configuration

### Environment Variables

Create a `.env` file in the backend root directory:

```env
# Required
GEMINI_API_KEY=your_google_gemini_api_key
```

### Obtaining a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

---

## Dependencies

### Backend (Python 3.8+)

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pandas>=2.0.0
numpy>=1.24.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
python-multipart>=0.0.6
```

### Frontend

- Modern web browser with JavaScript enabled
- No additional dependencies required

---

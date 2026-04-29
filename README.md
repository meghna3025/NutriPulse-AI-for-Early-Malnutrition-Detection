# NutriPulse 🛡️  
### AI-Powered Early Malnutrition Risk Detection & Intervention Platform

## Live Demo
🔗 App: https://nutripulse-825662706084.asia-south1.run.app  
📘 API Docs: https://nutripulse-825662706084.asia-south1.run.app/docs

---

## Overview
NutriPulse is an AI-powered nutrition intelligence platform that detects hidden malnutrition risks early using diet patterns, symptom signals, biomarker-style reasoning, and vulnerability analysis.

Rather than reacting after health decline, NutriPulse focuses on **preventive nutrition intelligence** by identifying risk, explaining why it is flagged, and simulating how interventions can reduce future nutritional risk.

---

## Problem Statement
Hidden nutritional deficiencies such as iron, protein and micronutrient gaps often go undetected until they become major health issues.

NutriPulse addresses this by providing:

- Early risk screening  
- Explainable AI-driven deficiency reasoning  
- Personalized food interventions  
- Preventive risk reduction simulation

---

## Features

### Clinical Nutrition Index
- Dynamic nutrition risk scoring  
- Low / Moderate / High risk categorization  
- Clinical-style severity visualization

### Biomarker Risk Analysis
- Iron Deficiency Risk  
- Protein Intake Efficiency  
- Vitamin Adequacy Analysis  

Dynamic severity bars use risk-based visualization and color coding:
- Green → Low risk  
- Amber → Moderate risk  
- Red → High risk

---

## Explainable AI Risk Drivers
The system explains **why** a user was flagged through major contributing factors such as:

- Low protein intake  
- Low food diversity  
- Symptom-driven deficiency signals  
- Vulnerability indicators

---

## Personalized Intervention Planning
Provides actionable recommendations across:

- Dietary Actions  
- Lifestyle Actions  
- Monitoring Advice

Examples:
- Increase protein intake  
- Improve iron absorption pairing  
- Support Vitamin D through sunlight exposure

---

## What-if Nutrition Simulator
Simulates projected improvement in nutrition risk if recommended interventions are followed.

Example:

Current Risk → Projected Reduced Risk

Adds preventive forecasting beyond static screening.

---

## Architecture
Frontend (React + Stitch)  
↓  
FastAPI Risk Engine  
↓  
Multi-Factor Nutrition Inference Layer  
↓  
Explainable Intervention Engine  
↓  
Google Cloud Run Deployment

---

## Tech Stack
- Stitch (Frontend UI)  
- Antigravity (Prompt-driven backend workflow)  
- FastAPI  
- React / Vite  
- Python  
- Docker  
- Google Cloud Run

---

## How It Works
### User Inputs
Users provide:
- Food habits  
- Symptoms  
- Meal frequency  
- Food diversity indicators

### AI Risk Pipeline Analyzes
- Diet risk  
- Deficiency signals  
- Vulnerability risk  
- Intervention planning

### Dashboard Returns
- Risk score  
- Biomarker analysis  
- Explainable AI insights  
- Personalized recommendations

---

## Running Locally

### Start Backend
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## Cloud Deployment
Deployed using **Google Cloud Run** with Dockerized full-stack deployment.

Public deployment:

https://nutripulse-825662706084.asia-south1.run.app

---

## Impact
NutriPulse aims to support:

- Preventive healthcare  
- Early malnutrition detection  
- Food-based intervention support  
- Nutrition intelligence for at-risk populations

---

## Future Improvements
- Community nutrition risk heatmaps  
- Rural health worker screening mode  
- Longitudinal nutrition monitoring  
- Population-level nutrition surveillance

---

Built for Promptathon 🚀

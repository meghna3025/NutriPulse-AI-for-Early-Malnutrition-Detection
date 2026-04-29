# NutriShield 🛡️  
### AI-Powered Early Malnutrition Risk Detection & Intervention Platform

NutriShield is an AI-powered nutrition intelligence platform that detects hidden malnutrition risks early using diet patterns, symptoms, biomarker-style reasoning, and vulnerability analysis.

Rather than reacting after health decline, NutriShield focuses on **preventive nutrition intelligence** by identifying risk, explaining why it is flagged, and simulating how interventions can reduce future nutritional risk.

---

## Problem Statement
Hidden nutritional deficiencies such as iron, protein and micronutrient gaps often go undetected until they become health issues.

NutriShield addresses this by providing:
- Early risk screening  
- Explainable AI-driven deficiency reasoning  
- Personalized food interventions  
- Preventive risk reduction simulation

---

## Features

### Clinical Nutrition Index
- Dynamic nutrition risk scoring  
- Low / Moderate / High risk categorization

### Biomarker Risk Analysis
- Iron Deficiency Risk
- Protein Intake Efficiency
- Vitamin Adequacy Analysis

Dynamic severity bars use risk-based visualization and color coding.

---

## Explainable AI Risk Drivers
The platform explains **why** a user was flagged by showing major contributing factors such as:
- Low protein intake  
- Low food diversity  
- Symptom-driven risk signals

---

## Personalized Intervention Planning
Provides actionable interventions across:
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

This adds preventive forecasting to screening.

---

## Tech Stack
- Stitch (Frontend UI)
- Antigravity (Prompt-driven backend workflow)
- FastAPI
- Next.js / React
- Python

---

## How It Works
1. User enters:
- Food habits
- Symptoms
- Meal patterns
- Food diversity

2. Multi-agent backend analyzes:
- Diet risk
- Deficiency signals
- Vulnerability risk
- Intervention planning

3. Dashboard returns:
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

http://localhost:3000

---

## Impact
NutriShield aims to support:
- Preventive healthcare
- Early malnutrition detection
- Food-based intervention support
- Nutrition intelligence for at-risk populations

---

## Demo
(https://nutripulse-825662706084.asia-south1.run.app/)

---

## Future Improvements
- Community nutrition risk heatmaps  
- Rural health worker screening mode  
- Longitudinal nutrition monitoring

---

Built for Promptathon 🚀

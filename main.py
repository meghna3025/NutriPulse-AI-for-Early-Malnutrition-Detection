from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

app = FastAPI(title="NutriShield Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---

class AnalysisRequest(BaseModel):
    user_category: str  # Child, Elderly, Pregnant, Adult
    protein_intake_frequency: str  # Daily, Weekly, Rarely
    daily_food_habits: str
    symptoms: List[str]
    meal_frequency: int
    food_diversity_quality: str  # High, Medium, Low

class NutritionalGaps(BaseModel):
    IronDeficiencyRisk: int
    ProteinIntakeEfficiency: int
    VitaminLevels: int
    MicronutrientRisk: Dict[str, int]  # New: e.g., {"Zinc": 40, "Magnesium": 60}
    SymptomExplanations: Dict[str, str] # New: Map symptoms to clinical reasons

class SummaryInsights(BaseModel):
    Metabolism: str
    Immunity: str
    Energy: str
    ClinicalStatus: str # New: e.g., "Critical", "Warning", "Optimal"

class ProjectedMetrics(BaseModel):
    RiskScore: int
    IronDeficiencyRisk: int
    ProteinIntakeEfficiency: int
    VitaminLevels: int
    OverallReduction: int

class InterventionPlan(BaseModel):
    DietaryActions: List[str]
    LifestyleActions: List[str]
    MonitoringAdvice: List[str]

class AnalysisResponse(BaseModel):
    RiskScore: int
    RiskCategory: str
    RiskInterpretation: str
    RiskDrivers: List[Dict[str, Any]]
    NutritionalGaps: NutritionalGaps
    PriorityFoods: List[Dict[str, str]]
    InterventionPlan: InterventionPlan # Updated: Categorized object
    SummaryInsights: SummaryInsights
    ProjectedMetrics: ProjectedMetrics
    ProjectionSummary: str

# --- Agent Logic ---

def diet_risk_analyzer(request: AnalysisRequest) -> Dict[str, Any]:
    """Agent 1: Detect protein, iron and vitamin deficiency risks and track drivers (positive and negative)."""
    protein_risk = 0
    drivers = []
    
    # Protein Logic
    if request.protein_intake_frequency.lower() == "rarely":
        protein_risk = 80
        drivers.append({"factor": "Rare protein intake frequency", "impact": "+35", "type": "warning"})
    elif request.protein_intake_frequency.lower() == "weekly":
        protein_risk = 40
        drivers.append({"factor": "Sub-optimal weekly protein intake", "impact": "+15", "type": "warning"})
    else:
        drivers.append({"factor": "Adequate protein intake lowered risk", "impact": "-10", "type": "positive"})
    
    iron_risk = 20
    if "fatigue" in [s.lower() for s in request.symptoms]:
        iron_risk += 30
        drivers.append({"factor": "Reported fatigue symptoms", "impact": "+10", "type": "warning"})
    else:
        drivers.append({"factor": "Stable symptom profile", "impact": "-8", "type": "positive"})
    
    vitamin_risk = 20
    if request.food_diversity_quality.lower() == "low":
        iron_risk += 30
        vitamin_risk = 70
        drivers.append({"factor": "Low dietary diversity", "impact": "+25", "type": "warning"})
    else:
        drivers.append({"factor": "Diverse food intake reduced risk", "impact": "-15", "type": "positive"})
        vitamin_risk = 30
        
    return {
        "protein_risk": protein_risk,
        "iron_risk": min(100, iron_risk),
        "vitamin_risk": vitamin_risk,
        "drivers": drivers
    }

def symptom_reasoner(symptoms: List[str], protein_risk: int, iron_risk: int) -> Dict[str, Any]:
    """Agent 2: Map symptoms to possible nutritional gaps and clinical explanations with severity awareness."""
    gaps = []
    explanations = {}
    lower_symptoms = [s.lower() for s in symptoms]
    
    # Iron Analysis
    if "fatigue" in lower_symptoms or "pale skin" in lower_symptoms or iron_risk > 30:
        gaps.append("Iron")
        if iron_risk > 60:
            explanations["Iron"] = "Elevated iron deficiency risk may impact oxygen transport and energy levels."
        elif iron_risk > 30:
            explanations["Iron"] = "Possible emerging iron deficiency indicators detected."
        else:
            explanations["Iron"] = "Iron biomarkers appear stable within normal range."
    else:
        explanations["Iron"] = "Iron biomarkers appear stable within normal range."

    # Protein Analysis
    if "hair loss" in lower_symptoms or "brittle nails" in lower_symptoms or protein_risk > 50:
        gaps.append("Protein/Biotin")
        if protein_risk > 70:
            explanations["Protein"] = "CRITICAL: Severe protein malnutrition. Structural tissue integrity (hair, nails, muscle) is at risk."
        else:
            explanations["Protein"] = "MODERATE: Sub-optimal protein synthesis detected. Increased intake recommended."
    else:
        explanations["Protein"] = "OPTIMAL: Protein metabolic efficiency is currently high."
        
    return {
        "suspected_deficiencies": list(set(gaps)),
        "explanations": explanations
    }

def vulnerability_agent(base_risk: int, category: str) -> int:
    """Agent 3: Adjust risk for children, elderly and pregnant users."""
    multiplier = 1.0
    cat = category.lower()
    if cat == "child":
        multiplier = 1.6 # Increased for realism
    elif cat == "pregnant":
        multiplier = 2.1 # Critical window
    elif cat == "elderly":
        multiplier = 1.5
    
    return int(min(100, base_risk * multiplier))

def food_intervention_agent(gaps: List[str]) -> Dict[str, Any]:
    """Agent 4: Generate structured clinical action plan categorized by type."""
    foods = []
    dietary = []
    lifestyle = [
        "Improve meal timing consistency",
        "Support sleep duration (7-9h) to improve metabolic recovery"
    ]
    monitoring = [
        "Reassess symptoms after 14 days of dietary improvements",
        "Monitor fatigue or energy fluctuations",
        "Consider clinical nutritional screening if risks persist"
    ]
    
    if "Iron" in gaps:
        foods.append({"name": "Spinach", "rationale": "high iron bioavailability when cooked"})
        foods.append({"name": "Lentils", "rationale": "supports red blood cell synthesis"})
        dietary.append("Add lentils at least 4 times per week to your main meals.")
        dietary.append("Pair spinach with lemon or other Vitamin C sources to improve iron absorption.")
    
    if "Protein/Biotin" in gaps:
        foods.append({"name": "Soybeans", "rationale": "high protein density"})
        foods.append({"name": "Greek Yogurt", "rationale": "improves protein bioavailability"})
        foods.append({"name": "Pumpkin Seeds", "rationale": "supports magnesium and protein levels"})
        dietary.append("Increase protein intake to 1.2g per kg of body weight.")
        dietary.append("Consume Greek yogurt daily to boost amino acid profile.")
        
    if not gaps:
        foods = [
            {"name": "Quinoa", "rationale": "complete plant-based protein"},
            {"name": "Mixed Berries", "rationale": "high antioxidant density"},
            {"name": "Walnuts", "rationale": "supports cognitive and metabolic health"}
        ]
        dietary.append("Maintain high food diversity with at least 5 different colors per day.")
        lifestyle.append("Increase morning sunlight exposure for 15 minutes to support Vitamin D levels.")
    else:
        # Default lifestyle for any gaps
        lifestyle.append("Increase morning sunlight exposure for 15 minutes to support Vitamin D levels.")
        
    return {
        "priority_foods": foods[:4],
        "intervention_plan": {
            "DietaryActions": dietary,
            "LifestyleActions": lifestyle,
            "MonitoringAdvice": monitoring
        }
    }

def risk_score_synthesizer(diet_data: Dict, symptom_data: Dict, vuln_score: int) -> Dict:
    """Agent 5: Generate final structured output with XAI reasoning."""
    
    if vuln_score < 35:
        category = "Optimal"
        interpretation = "Low Risk — Nutritional status appears stable"
        status = "Healthy"
    elif vuln_score < 65:
        category = "Moderate Risk"
        interpretation = "Moderate Risk — Early intervention recommended"
        status = "Caution"
    else:
        category = "Critical Risk"
        interpretation = "High Risk — Significant nutritional gaps detected"
        status = "Emergency Intervention Required"
        
    # Combine drivers
    drivers = diet_data["drivers"]
    if vuln_score > 50 and not any(d["factor"] == "Vulnerability factors" for d in drivers):
        drivers.append({"factor": "High vulnerability window (Age/Category)", "impact": "+15"})

    # Micronutrient simulation based on food diversity
    micro_risk = {
        "Zinc": int(vuln_score * 0.8),
        "Magnesium": int(vuln_score * 0.6),
        "Vitamin B12": 90 if diet_data["protein_risk"] > 70 else 30
    }
    
    # Systemic Health Indicators Logic
    # Metabolism
    if diet_data["protein_risk"] < 30:
        metabolism = "Optimal"
    elif diet_data["protein_risk"] < 50:
        metabolism = "Stable"
    elif diet_data["protein_risk"] < 75:
        metabolism = "At Risk"
    else:
        metabolism = "Metabolic Stress"
        
    # Immunity
    if vuln_score < 30 and diet_data["vitamin_risk"] < 30:
        immunity = "Stable"
    elif vuln_score < 50:
        immunity = "Mild Vulnerability"
    elif vuln_score < 75:
        immunity = "At Risk"
    else:
        immunity = "Compromised"
        
    # Energy
    if diet_data["iron_risk"] < 30 and "fatigue" not in [s.lower() for s in symptom_data["explanations"].keys()]:
        energy = "Stable"
    elif vuln_score < 60:
        energy = "Fluctuating"
    else:
        energy = "Low"

    insights = {
        "Metabolism": metabolism,
        "Immunity": immunity,
        "Energy": energy,
        "ClinicalStatus": status
    }
    
    # Simulation for What-if Simulator
    projected_iron = int(diet_data["iron_risk"] * 0.5) # 50% improvement
    projected_protein = min(100, (100 - diet_data["protein_risk"]) + 35) # +35 efficiency
    projected_vitamin = min(100, (100 - diet_data["vitamin_risk"]) + 35) # +35 adequacy
    
    projected_total_risk = int((projected_iron + (100 - projected_protein) + (100 - projected_vitamin)) / 3)
    reduction = vuln_score - projected_total_risk
    
    projected_metrics = {
        "RiskScore": projected_total_risk,
        "IronDeficiencyRisk": projected_iron,
        "ProteinIntakeEfficiency": projected_protein,
        "VitaminLevels": projected_vitamin,
        "OverallReduction": reduction
    }
    
    projection_summary = f"Following the recommended interventions may reduce nutritional risk by approximately {reduction}%."
    
    return {
        "RiskScore": vuln_score,
        "RiskCategory": category,
        "RiskInterpretation": interpretation,
        "RiskDrivers": drivers,
        "NutritionalGaps": {
            "IronDeficiencyRisk": diet_data["iron_risk"],
            "ProteinIntakeEfficiency": 100 - diet_data["protein_risk"],
            "VitaminLevels": 100 - diet_data["vitamin_risk"],
            "MicronutrientRisk": micro_risk,
            "SymptomExplanations": symptom_data["explanations"]
        },
        "SummaryInsights": insights,
        "ProjectedMetrics": projected_metrics,
        "ProjectionSummary": projection_summary
    }

# --- API Endpoint ---

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_risk(request: AnalysisRequest):
    try:
        # Step 1: Diet Analysis
        diet_results = diet_risk_analyzer(request)
        
        # Step 2: Symptom Mapping (Now severity aware)
        symptom_results = symptom_reasoner(request.symptoms, diet_results["protein_risk"], diet_results["iron_risk"])
        
        # Step 3: Vulnerability Check
        base_risk = (diet_results["protein_risk"] + diet_results["iron_risk"] + diet_results["vitamin_risk"]) / 3
        final_risk = vulnerability_agent(base_risk, request.user_category)
        
        # Step 4: Interventions
        interventions = food_intervention_agent(symptom_results["suspected_deficiencies"])
        
        # Step 5: Synthesis
        final_output = risk_score_synthesizer(diet_results, symptom_results, final_risk)
        
        # Combine everything
        response_data = {
            **final_output,
            "PriorityFoods": interventions["priority_foods"],
            "InterventionPlan": interventions["intervention_plan"]
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve frontend static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(frontend_path):
    # Serve static assets (js, css, etc.)
    assets_path = os.path.join(frontend_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    # Serve index.html and other root files
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # 1. Try to serve specific file from dist
        file_path = os.path.join(frontend_path, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # 2. Default to index.html (SPA support)
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        
        return {"detail": "Frontend assets not found. Please build the frontend."}
else:
    @app.get("/")
    async def root_warning():
        return {"detail": "Frontend not found at frontend/dist. Please run 'npm run build' in the frontend directory."}

if __name__ == "__main__":
    import uvicorn
    # Use port from environment variable for Google Cloud Run
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

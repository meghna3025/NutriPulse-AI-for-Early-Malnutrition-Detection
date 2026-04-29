// Navigation Logic
window.showView = (viewId) => {
    document.querySelectorAll('.view').forEach(view => {
        view.classList.add('hidden');
    });
    document.getElementById(viewId).classList.remove('hidden');
    window.scrollTo(0, 0);
};

// Form Submission Logic
const riskForm = document.getElementById('risk-form');
const submitBtn = document.getElementById('submit-btn');
const spinner = submitBtn.querySelector('.spinner');
const btnText = submitBtn.querySelector('.btn-text');

// Dropdown Helper Text Logic
const foodDiversitySelect = document.getElementById('food-diversity-select');
const foodDiversityHelper = document.getElementById('food-diversity-helper');

const diversityDescriptions = {
    'High': 'Varied vegetables, grains, and diverse protein sources.',
    'Medium': 'Consistent meals but with limited variety in food groups.',
    'Low': 'Monotonous diet with very few food types represented.'
};

const updateHelperText = () => {
    const value = foodDiversitySelect.value;
    foodDiversityHelper.textContent = diversityDescriptions[value] || '';
};

if (foodDiversitySelect) {
    foodDiversitySelect.addEventListener('change', updateHelperText);
    updateHelperText(); // Initial call
}

riskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Set loading state
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');
    btnText.textContent = 'Analyzing...';

    const formData = new FormData(riskForm);
    
    // Process symptoms: Combine reported and other
    const reportedSymptoms = formData.getAll('reportedSymptoms');
    const otherSymptomsStr = formData.get('otherSymptoms');
    const otherSymptoms = otherSymptomsStr ? otherSymptomsStr.split(',').map(s => s.trim()).filter(s => s) : [];
    const allSymptoms = [...reportedSymptoms, ...otherSymptoms];

    const payload = {
        user_category: formData.get('userCategory'),
        protein_intake_frequency: formData.get('proteinIntakeFrequency'),
        daily_food_habits: formData.get('dailyFoodHabits'),
        symptoms: allSymptoms,
        meal_frequency: parseInt(formData.get('mealFrequency')),
        food_diversity_quality: formData.get('foodDiversityQuality')
    };

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const result = await response.json();
        
        // Save results and bind to dashboard
        localStorage.setItem('nutrishield_results', JSON.stringify(result));
        bindDashboard(result);
        showView('results-dashboard');

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis. Please check if the backend server is running on port 8000.');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        spinner.classList.add('hidden');
        btnText.textContent = 'Analyze Risk';
    }
});

// Dashboard Data Binding
function bindDashboard(data) {
    // Risk Score & Category
    const scoreElement = document.getElementById('risk-score');
    const gaugeFill = document.getElementById('risk-gauge-fill');
    const categoryBadge = document.getElementById('risk-category');
    const interpretationBanner = document.getElementById('risk-interpretation');
    const statusElement = document.getElementById('clinical-status');

    scoreElement.textContent = data.RiskScore;
    gaugeFill.style.height = `${data.RiskScore}%`;
    categoryBadge.textContent = data.RiskCategory;
    interpretationBanner.textContent = data.RiskInterpretation;
    statusElement.textContent = data.SummaryInsights.ClinicalStatus;
    
    // Color based on risk
    const riskColor = data.RiskScore > 65 ? '#BA1A1A' : (data.RiskScore > 35 ? '#F57C00' : '#4CAF50');
    gaugeFill.style.backgroundColor = riskColor;
    categoryBadge.style.backgroundColor = `${riskColor}11`;
    categoryBadge.style.color = riskColor;
    
    // Banner styling
    interpretationBanner.style.backgroundColor = `${riskColor}11`;
    interpretationBanner.style.color = riskColor;
    interpretationBanner.style.border = `1px solid ${riskColor}33`;

    // Biomarker Risk Bars
    const ironFill = document.getElementById('iron-fill');
    const proteinFill = document.getElementById('protein-fill');
    const vitaminFill = document.getElementById('vitamin-fill');

    // Widths
    ironFill.style.width = `${data.NutritionalGaps.IronDeficiencyRisk}%`;
    proteinFill.style.width = `${data.NutritionalGaps.ProteinIntakeEfficiency}%`;
    vitaminFill.style.width = `${data.NutritionalGaps.VitaminLevels}%`;

    // Colors & Labels (Traffic Light System)
    const getSeverity = (value, type) => {
        // type 'risk': high is bad
        // type 'efficiency/adequacy': low is bad
        if (type === 'risk') {
            if (value > 60) return { label: 'High Risk', color: '#BA1A1A' };
            if (value > 30) return { label: 'Moderate Risk', color: '#F57C00' };
            return { label: 'Optimal', color: '#4CAF50' };
        } else {
            if (value < 40) return { label: 'Critical', color: '#BA1A1A' };
            if (value < 70) return { label: 'Moderate', color: '#F57C00' };
            return { label: 'Optimal', color: '#4CAF50' };
        }
    };

    const ironSev = getSeverity(data.NutritionalGaps.IronDeficiencyRisk, 'risk');
    const proteinSev = getSeverity(data.NutritionalGaps.ProteinIntakeEfficiency, 'efficiency');
    const vitaminSev = getSeverity(data.NutritionalGaps.VitaminLevels, 'efficiency');

    // Apply Iron
    ironFill.style.backgroundColor = ironSev.color;
    document.getElementById('iron-severity').textContent = ironSev.label;
    document.getElementById('iron-severity').style.color = ironSev.color;
    document.getElementById('iron-severity').style.backgroundColor = `${ironSev.color}11`;

    // Apply Protein
    proteinFill.style.backgroundColor = proteinSev.color;
    document.getElementById('protein-severity').textContent = proteinSev.label;
    document.getElementById('protein-severity').style.color = proteinSev.color;
    document.getElementById('protein-severity').style.backgroundColor = `${proteinSev.color}11`;

    // Apply Vitamin
    vitaminFill.style.backgroundColor = vitaminSev.color;
    document.getElementById('vitamin-severity').textContent = vitaminSev.label;
    document.getElementById('vitamin-severity').style.color = vitaminSev.color;
    document.getElementById('vitamin-severity').style.backgroundColor = `${vitaminSev.color}11`;

    // Symptom Explanations (Severity Aware)
    const ironExpl = document.getElementById('iron-explanation');
    const proteinExpl = document.getElementById('protein-explanation');
    
    ironExpl.textContent = data.NutritionalGaps.SymptomExplanations["Iron"];
    proteinExpl.textContent = data.NutritionalGaps.SymptomExplanations["Protein"] || "Protein biomarkers appear stable within normal range.";
    
    // Style borders based on severity
    ironExpl.style.borderColor = ironSev.color;
    proteinExpl.style.borderColor = proteinSev.color;

    // Micronutrient Grid
    const microGrid = document.getElementById('micronutrient-grid');
    microGrid.innerHTML = Object.entries(data.NutritionalGaps.MicronutrientRisk).map(([name, risk]) => `
        <div class="micro-item">
            <div class="micro-label">${name}</div>
            <div class="micro-value" style="color: ${risk > 60 ? '#BA1A1A' : 'var(--text)'}">${risk}%</div>
        </div>
    `).join('');

    // XAI Risk Drivers
    const driversList = document.getElementById('risk-drivers-list');
    driversList.innerHTML = data.RiskDrivers.map(driver => `
        <li class="driver-item ${driver.type === 'positive' ? 'positive' : ''}">
            <span class="driver-factor">${driver.factor}</span>
            <span class="driver-impact">${driver.impact}</span>
        </li>
    `).join('');

    // Lists
    const foodsList = document.getElementById('priority-foods-list');
    foodsList.innerHTML = data.PriorityFoods.map(food => `
        <li class="food-item">
            <strong>${food.name}</strong>
            <span class="food-rationale">— ${food.rationale}</span>
        </li>
    `).join('');

    const dietaryList = document.getElementById('dietary-actions-list');
    dietaryList.innerHTML = data.InterventionPlan.DietaryActions.map(item => `<li>${item}</li>`).join('');

    const lifestyleList = document.getElementById('lifestyle-actions-list');
    lifestyleList.innerHTML = data.InterventionPlan.LifestyleActions.map(item => `<li>${item}</li>`).join('');

    const monitoringList = document.getElementById('monitoring-advice-list');
    monitoringList.innerHTML = data.InterventionPlan.MonitoringAdvice.map(item => `<li>${item}</li>`).join('');

    // Insights
    const applyIndicator = (id, value) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = value;
        el.className = 'value'; // Reset
        
        const low = ['Optimal', 'Stable', 'Healthy'];
        const med = ['At Risk', 'Mild Vulnerability', 'Fluctuating', 'Caution'];
        const high = ['Compromised', 'Metabolic Stress', 'Low', 'Emergency Intervention Required'];

        if (low.includes(value)) el.classList.add('indicator-healthy');
        else if (med.includes(value)) el.classList.add('indicator-warning');
        else if (high.includes(value)) el.classList.add('indicator-danger');
    };

    applyIndicator('insight-metabolism', data.SummaryInsights.Metabolism);
    applyIndicator('insight-immunity', data.SummaryInsights.Immunity);
    applyIndicator('insight-energy', data.SummaryInsights.Energy);

    // What-if Simulator
    document.getElementById('sim-current-score').textContent = data.RiskScore;
    document.getElementById('sim-projected-score').textContent = data.ProjectedMetrics.RiskScore;

    document.getElementById('sim-iron-before').textContent = `${data.NutritionalGaps.IronDeficiencyRisk}%`;
    document.getElementById('sim-iron-after').textContent = `${data.ProjectedMetrics.IronDeficiencyRisk}%`;

    document.getElementById('sim-protein-before').textContent = `${data.NutritionalGaps.ProteinIntakeEfficiency}%`;
    document.getElementById('sim-protein-after').textContent = `${data.ProjectedMetrics.ProteinIntakeEfficiency}%`;

    document.getElementById('sim-vitamin-before').textContent = `${data.NutritionalGaps.VitaminLevels}%`;
    document.getElementById('sim-vitamin-after').textContent = `${data.ProjectedMetrics.VitaminLevels}%`;

    document.getElementById('projection-summary').textContent = data.ProjectionSummary;
}

// Initial state: check if we have data to show dashboard
const savedResults = localStorage.getItem('nutrishield_results');
if (savedResults) {
    try {
        bindDashboard(json.parse(savedResults));
    } catch(e) {}
}

"""
Web Dashboard for PureSpectrum Survey Monitoring
Simple HTML interface accessible via web browser
"""
from fastapi.responses import HTMLResponse
import os
import aiohttp
from .scraper import PureSpectrumScraper

# Get credentials from environment
PURESPECTRUM_USERNAME = os.getenv("PURESPECTRUM_USERNAME", "")
PURESPECTRUM_PASSWORD = os.getenv("PURESPECTRUM_PASSWORD", "")


async def dashboard_home():
    """Main dashboard page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PureSpectrum Survey Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .header h1 {
                color: #333;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
            }
            
            .controls {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-right: 10px;
                transition: background 0.3s;
            }
            
            .btn:hover {
                background: #5568d3;
            }
            
            .btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }
            
            .survey-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .survey-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            
            .survey-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            .survey-card h3 {
                color: #333;
                margin-bottom: 15px;
                font-size: 18px;
            }
            
            .survey-id {
                color: #667eea;
                font-weight: bold;
                font-size: 14px;
                margin-bottom: 10px;
            }
            
            .progress-bar {
                width: 100%;
                height: 25px;
                background: #e0e0e0;
                border-radius: 12px;
                overflow: hidden;
                margin: 10px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                transition: width 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 15px;
            }
            
            .stat {
                text-align: center;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 5px;
            }
            
            .stat-label {
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
            }
            
            .stat-value {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            
            .quota-section {
                background: white;
                padding: 25px;
                border-radius: 10px;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                display: none;
            }
            
            .quota-section.active {
                display: block;
            }
            
            .quota-group {
                margin-bottom: 25px;
            }
            
            .quota-group h4 {
                color: #333;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }
            
            .quota-item {
                padding: 15px;
                margin-bottom: 10px;
                background: #f9f9f9;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            
            .quota-name {
                font-weight: bold;
                color: #333;
                margin-bottom: 8px;
            }
            
            .quota-progress {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }
            
            .error {
                background: #fee;
                color: #c33;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 PureSpectrum Survey Dashboard</h1>
                <p>Monitor your active surveys, check status, and view detailed quota breakdowns</p>
            </div>
            
            <div class="controls">
                <button class="btn" onclick="loadSurveys()">🔄 Refresh Surveys</button>
                <button class="btn" onclick="clearData()">Clear</button>
            </div>
            
            <div id="loading" class="loading" style="display: none;">
                Loading surveys...
            </div>
            
            <div id="error" class="error" style="display: none;"></div>
            
            <div id="surveys" class="survey-grid"></div>
            
            <div id="quotas" class="quota-section"></div>
        </div>
        
        <script>
            async function loadSurveys() {
                const loading = document.getElementById('loading');
                const error = document.getElementById('error');
                const surveysDiv = document.getElementById('surveys');
                const quotasDiv = document.getElementById('quotas');
                
                loading.style.display = 'block';
                error.style.display = 'none';
                surveysDiv.innerHTML = '';
                quotasDiv.innerHTML = '';
                quotasDiv.classList.remove('active');
                
                try {
                    const response = await fetch('/api/surveys');
                    if (!response.ok) throw new Error('Failed to load surveys');
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    if (data.surveys && Object.keys(data.surveys).length === 0) {
                        surveysDiv.innerHTML = '<div class="loading">No active surveys found</div>';
                        loading.style.display = 'none';
                        return;
                    }
                    
                    surveysDiv.innerHTML = '';
                    
                    for (const [surveyId, survey] of Object.entries(data.surveys)) {
                        const progress = survey.target > 0 ? (survey.completes / survey.target * 100) : 0;
                        const card = document.createElement('div');
                        card.className = 'survey-card';
                        card.innerHTML = `
                            <div class="survey-id">Survey ID: ${surveyId}</div>
                            <h3>${survey.title || 'Untitled Survey'}</h3>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progress}%">
                                    ${progress.toFixed(1)}%
                                </div>
                            </div>
                            <div class="stats">
                                <div class="stat">
                                    <div class="stat-label">Status</div>
                                    <div class="stat-value">${survey.status || 'Unknown'}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Progress</div>
                                    <div class="stat-value">${survey.completes}/${survey.target}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">CPI</div>
                                    <div class="stat-value">$${survey.cpi?.toFixed(2) || '0.00'}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Cost</div>
                                    <div class="stat-value">$${survey.currentCost?.toFixed(2) || '0.00'}</div>
                                </div>
                            </div>
                            <button class="btn" onclick="loadQuotas('${surveyId}')" style="margin-top: 15px; width: 100%;">
                                View Quotas
                            </button>
                        `;
                        surveysDiv.appendChild(card);
                    }
                    
                } catch (err) {
                    error.textContent = 'Error: ' + err.message;
                    error.style.display = 'block';
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            async function loadQuotas(surveyId) {
                const quotasDiv = document.getElementById('quotas');
                const loading = document.getElementById('loading');
                
                loading.style.display = 'block';
                quotasDiv.innerHTML = '';
                quotasDiv.classList.add('active');
                
                try {
                    const response = await fetch(`/api/quotas/${surveyId}`);
                    if (!response.ok) throw new Error('Failed to load quotas');
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    quotasDiv.innerHTML = `<h3>Quota Details for Survey ${surveyId}</h3>`;
                    
                    // Group quotas
                    const grouped = {};
                    data.quotas.forEach(quota => {
                        const group = quota.group_key || 'General';
                        if (!grouped[group]) grouped[group] = [];
                        grouped[group].push(quota);
                    });
                    
                    for (const [groupName, quotas] of Object.entries(grouped)) {
                        const groupDiv = document.createElement('div');
                        groupDiv.className = 'quota-group';
                        groupDiv.innerHTML = `<h4>${groupName}</h4>`;
                        
                        quotas.forEach(quota => {
                            const name = generateQuotaName(quota);
                            const fielded = quota.achieved || 0;
                            const goal = quota.required_count || 0;
                            const progress = goal > 0 ? (fielded / goal * 100) : 0;
                            
                            const quotaItem = document.createElement('div');
                            quotaItem.className = 'quota-item';
                            quotaItem.innerHTML = `
                                <div class="quota-name">${name}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${progress}%">
                                        ${progress.toFixed(1)}%
                                    </div>
                                </div>
                                <div class="quota-progress">
                                    Fielded: ${fielded}/${goal} | Target: ${quota.current_target || goal} | 
                                    Open: ${quota.currently_open || 0} | In Progress: ${quota.in_progress || 0}
                                </div>
                            `;
                            groupDiv.appendChild(quotaItem);
                        });
                        
                        quotasDiv.appendChild(groupDiv);
                    }
                    
                    // Scroll to quotas
                    quotasDiv.scrollIntoView({ behavior: 'smooth' });
                    
                } catch (err) {
                    quotasDiv.innerHTML = `<div class="error">Error loading quotas: ${err.message}</div>`;
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            function generateQuotaName(quota) {
                const criteria = quota.criteria || [];
                if (criteria.length === 0) {
                    return quota.quota_title || 'General Quota';
                }
                
                const parts = [];
                criteria.forEach(criterion => {
                    const qualName = criterion.qualification_name || '';
                    const conditions = criterion.condition_names || [];
                    
                    if (qualName === 'Gender' && conditions.length > 0) {
                        parts.push(conditions[0]);
                    } else if (qualName === 'Age') {
                        const rangeSets = criterion.range_sets || [];
                        if (rangeSets.length > 0) {
                            const range = rangeSets[0];
                            const fromAge = range.from || '';
                            const toAge = range.to || '';
                            if (fromAge && toAge) {
                                parts.push(`${fromAge}-${toAge} yr`);
                            }
                        }
                    }
                });
                
                return parts.length > 0 ? parts.join(', ') : (quota.quota_title || 'General Quota');
            }
            
            function clearData() {
                document.getElementById('surveys').innerHTML = '';
                document.getElementById('quotas').innerHTML = '';
                document.getElementById('quotas').classList.remove('active');
                document.getElementById('error').style.display = 'none';
            }
            
            // Load surveys on page load
            window.addEventListener('load', () => {
                loadSurveys();
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


async def get_surveys():
    """API endpoint to get all live surveys"""
    if not PURESPECTRUM_USERNAME or not PURESPECTRUM_PASSWORD:
        return {"error": "PureSpectrum credentials not configured"}
    
    try:
        scraper = PureSpectrumScraper(PURESPECTRUM_USERNAME, PURESPECTRUM_PASSWORD)
        
        async with aiohttp.ClientSession() as session:
            if not await scraper.login(session):
                return {"error": "Failed to authenticate with PureSpectrum"}
            
            survey_data = await scraper.get_survey_data(session)
            
            return {"surveys": survey_data}
    except Exception as e:
        return {"error": str(e)}


async def get_quotas(survey_id: str):
    """API endpoint to get quotas for a specific survey"""
    if not PURESPECTRUM_USERNAME or not PURESPECTRUM_PASSWORD:
        return {"error": "PureSpectrum credentials not configured"}
    
    try:
        scraper = PureSpectrumScraper(PURESPECTRUM_USERNAME, PURESPECTRUM_PASSWORD)
        
        async with aiohttp.ClientSession() as session:
            if not await scraper.login(session):
                return {"error": "Failed to authenticate with PureSpectrum"}
            
            quotas = await scraper.get_survey_quotas(session, survey_id)
            
            return {"quotas": quotas}
    except Exception as e:
        return {"error": str(e)}


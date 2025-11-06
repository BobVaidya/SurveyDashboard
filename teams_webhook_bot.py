"""
Teams Outgoing Webhook Bot - No Azure Required!
Simplified bot for Teams using Outgoing Webhooks
"""
import os
import hmac
import hashlib
import base64
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()

app = FastAPI(title="Teams Survey Bot")


class PureSpectrumAPI:
    """Simple wrapper for PureSpectrum API calls"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = None
    
    async def get_live_surveys(self):
        """Get live surveys - uses your existing scraper logic"""
        from app.scraper import PureSpectrumScraper
        
        scraper = PureSpectrumScraper(self.username, self.password)
        
        async with aiohttp.ClientSession() as session:
            if await scraper.login(session):
                survey_data = await scraper.get_survey_data(session)
                
                # Format for display
                if not survey_data:
                    return "No active surveys found."
                
                response = f"**Found {len(survey_data)} Active Surveys**\n\n"
                
                for survey_id, survey in survey_data.items():
                    title = survey.get('title', 'Untitled')
                    status = survey.get('status', 'Unknown')
                    completes = survey.get('completes', 0)
                    target = survey.get('target', 0)
                    cpi = survey.get('cpi', 0)
                    progress_pct = (completes / target * 100) if target > 0 else 0
                    
                    # Progress bar
                    bar_length = 15
                    filled = int(bar_length * progress_pct / 100)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    
                    response += f"**Survey ID:** {survey_id}\n"
                    response += f"**Title:** {title}\n"
                    response += f"**Status:** {status}\n"
                    response += f"**Progress:** {completes}/{target} ({progress_pct:.1f}%)\n"
                    response += f"[{bar}] {progress_pct:.1f}%\n"
                    response += f"**CPI:** ${cpi:.2f}\n"
                    response += f"\n"
                
                return response
            else:
                return "❌ Failed to authenticate with PureSpectrum"
    
    async def get_survey_status(self, survey_id: str):
        """Get status for specific survey"""
        from app.scraper import PureSpectrumScraper
        
        scraper = PureSpectrumScraper(self.username, self.password)
        
        async with aiohttp.ClientSession() as session:
            if await scraper.login(session):
                survey_data = await scraper.get_survey_data(session, survey_id)
                
                if not survey_data or survey_id not in survey_data:
                    return f"❌ Survey {survey_id} not found"
                
                survey = survey_data[survey_id]
                title = survey.get('title', 'Untitled')
                status = survey.get('status', 'Unknown')
                completes = survey.get('completes', 0)
                target = survey.get('target', 0)
                cpi = survey.get('cpi', 0)
                incidence = survey.get('incidence', 0)
                loi = survey.get('loi', 0)
                current_cost = survey.get('currentCost', 0)
                
                progress_pct = (completes / target * 100) if target > 0 else 0
                bar_length = 15
                filled = int(bar_length * progress_pct / 100)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                response = f"**Survey {survey_id} Status**\n\n"
                response += f"**Title:** {title}\n"
                response += f"**Status:** {status}\n"
                response += f"**Progress:** {completes}/{target} ({progress_pct:.1f}%)\n"
                response += f"[{bar}] {progress_pct:.1f}%\n"
                response += f"**CPI:** ${cpi:.2f}\n"
                response += f"**Incidence:** {incidence*100:.1f}%\n"
                response += f"**LOI:** {loi} minutes\n"
                response += f"**Current Cost:** ${current_cost:.2f}\n"
                
                return response
            else:
                return "❌ Failed to authenticate with PureSpectrum"
    
    async def get_quotas(self, survey_id: str):
        """Get quota details for survey"""
        from app.scraper import PureSpectrumScraper
        
        scraper = PureSpectrumScraper(self.username, self.password)
        
        async with aiohttp.ClientSession() as session:
            if await scraper.login(session):
                quotas = await scraper.get_survey_quotas(session, survey_id)
                
                if not quotas:
                    return f"❌ No quota data found for survey {survey_id}"
                
                response = f"**Quota Details for Survey {survey_id}**\n\n"
                
                # Group quotas
                grouped = {}
                for quota in quotas:
                    group = quota.get('group_key', 'General')
                    if group not in grouped:
                        grouped[group] = []
                    grouped[group].append(quota)
                
                for group, group_quotas in grouped.items():
                    response += f"**{group}**\n"
                    
                    for quota in group_quotas:
                        # Generate quota name
                        name = self._generate_quota_name(quota)
                        fielded = quota.get('achieved', 0)
                        goal = quota.get('required_count', 0)
                        currently_open = quota.get('currently_open', 0)
                        
                        progress_pct = (fielded / goal * 100) if goal > 0 else 0
                        bar_length = 20
                        filled = int(bar_length * progress_pct / 100)
                        bar = "█" * filled + "░" * (bar_length - filled)
                        
                        # Get additional quota details
                        current_target = quota.get('current_target', goal)
                        in_progress = quota.get('in_progress', 0)
                        
                        response += f"  • **{name}**\n"
                        response += f"    Fielded: {fielded}/{goal} ({progress_pct:.1f}%)\n"
                        response += f"    Progress: [{bar}] {progress_pct:.1f}%\n"
                        response += f"    Target: {current_target} | Open: {currently_open} | In Progress: {in_progress}\n"
                    
                    response += "\n"
                
                return response
            else:
                return "❌ Failed to authenticate with PureSpectrum"
    
    def _generate_quota_name(self, quota: dict) -> str:
        """Generate meaningful quota name from criteria"""
        criteria = quota.get('criteria', [])
        if not criteria:
            return quota.get('quota_title', 'General Quota')
        
        parts = []
        for criterion in criteria:
            qual_name = criterion.get('qualification_name', '')
            conditions = criterion.get('condition_names', [])
            
            if qual_name == 'Gender' and conditions:
                parts.append(conditions[0])
            elif qual_name == 'Age':
                range_sets = criterion.get('range_sets', [])
                if range_sets:
                    age_range = range_sets[0]
                    from_age = age_range.get('from', '')
                    to_age = age_range.get('to', '')
                    if from_age and to_age:
                        parts.append(f"{from_age}-{to_age} yr")
        
        return ', '.join(parts) if parts else quota.get('quota_title', f"Quota {quota.get('ps_quota_id', '')[:8]}")


def verify_teams_signature(request: Request, body: bytes) -> bool:
    """Verify the request is from Teams using HMAC"""
    security_token = os.getenv("TEAMS_SECURITY_TOKEN", "")
    
    if not security_token:
        # If no token set, skip validation (for initial testing)
        return True
    
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header.startswith("HMAC "):
        return False
    
    signature = auth_header[5:]  # Remove "HMAC " prefix
    
    # Calculate expected signature
    expected = base64.b64encode(
        hmac.new(
            security_token.encode('utf-8'),
            body,
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    return hmac.compare_digest(signature, expected)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Teams Survey Bot is running!"}


@app.get("/health")
async def health():
    """Health check for Railway"""
    return {"status": "healthy"}


@app.post("/webhook")
async def teams_webhook(request: Request):
    """
    Teams Outgoing Webhook endpoint
    This is where Teams will send messages when bot is @mentioned
    """
    try:
        body = await request.body()
        
        # Verify request is from Teams
        if not verify_teams_signature(request, body):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse the Teams message
        data = await request.json()
        
        # Extract message text (removing @mention)
        text = data.get("text", "").strip()
        
        # Remove bot mention from text
        # Teams sends: "@BotName command args"
        # We want: "command args"
        if text.startswith("@"):
            text = " ".join(text.split()[1:])
        
        text = text.strip().lower()
        
        # Get PureSpectrum credentials
        ps_username = os.getenv("PURESPECTRUM_USERNAME")
        ps_password = os.getenv("PURESPECTRUM_PASSWORD")
        
        if not ps_username or not ps_password:
            return JSONResponse({
                "type": "message",
                "text": "❌ Bot configuration error: PureSpectrum credentials not set"
            })
        
        api = PureSpectrumAPI(ps_username, ps_password)
        
        # Process commands
        if not text or text == "help":
            response_text = """**Teams Survey Bot - Commands**

• `@SurveyBot live` - Show all active surveys
• `@SurveyBot status <surveyId>` - Show survey status
• `@SurveyBot quotas <surveyId>` - Show quota details
• `@SurveyBot help` - Show this help

**Examples:**
• `@SurveyBot live`
• `@SurveyBot status 45104633`
• `@SurveyBot quotas 45104633`
"""
        
        elif text == "live" or text == "surveys":
            response_text = await api.get_live_surveys()
        
        elif text.startswith("status "):
            survey_id = text.split()[1] if len(text.split()) > 1 else ""
            if survey_id:
                response_text = await api.get_survey_status(survey_id)
            else:
                response_text = "❌ Please provide a survey ID. Example: `@SurveyBot status 45104633`"
        
        elif text.startswith("quotas "):
            survey_id = text.split()[1] if len(text.split()) > 1 else ""
            if survey_id:
                response_text = await api.get_quotas(survey_id)
            else:
                response_text = "❌ Please provide a survey ID. Example: `@SurveyBot quotas 45104633`"
        
        else:
            response_text = f"❌ Unknown command: `{text}`\n\nSay `@SurveyBot help` for available commands."
        
        # Return response in Teams format
        return JSONResponse({
            "type": "message",
            "text": response_text
        })
    
    except Exception as e:
        return JSONResponse({
            "type": "message",
            "text": f"❌ Error: {str(e)}"
        })


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("teams_webhook_bot:app", host="0.0.0.0", port=port, reload=True)


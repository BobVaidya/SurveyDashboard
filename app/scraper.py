"""
Web scraping for PureSpectrum dashboard using session cookies
This approach avoids the complex captcha by reusing authenticated session cookies
"""
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class PureSpectrumScraper:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.auth_file = Path("purespectrum_auth.json")
        self.auth_data = self._load_auth()
        self.last_known_data = {}
        
    def _load_auth(self) -> Dict:
        """Load saved auth token from file"""
        if self.auth_file.exists():
            try:
                with open(self.auth_file, 'r') as f:
                    auth_data = json.load(f)
                    logger.info("✅ Loaded saved authentication token")
                    return auth_data
            except Exception as e:
                logger.error(f"Failed to load auth: {e}")
        return {}
    
    def _save_auth(self, auth_data: Dict):
        """Save auth data to file for reuse"""
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(auth_data, f, indent=2)
            logger.info("✅ Saved authentication token")
        except Exception as e:
            logger.error(f"Failed to save auth: {e}")
    
    def _get_auth_headers(self) -> Dict:
        """Get authorization headers for API requests"""
        token = self.auth_data.get('token', '')
        return {
            'access-token': token,
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://platform.purespectrum.com',
            'Referer': 'https://platform.purespectrum.com/'
        }
    
    def _map_status(self, status_code) -> str:
        """Map PureSpectrum status codes to human-readable strings"""
        status_map = {
            22: 'Active',  # or 'All' - needs confirmation
            33: 'Paused',
            # Add more as we discover them
        }
        return status_map.get(status_code, f'Status {status_code}')
    
    async def login(self, session: aiohttp.ClientSession) -> bool:
        """
        Check if existing auth token is valid, otherwise prompt for manual login
        """
        try:
            # Try to access a protected endpoint with existing token
            if self.auth_data.get('token'):
                logger.info("🔐 Testing existing authentication token...")
                
                headers = self._get_auth_headers()
                
                timeout = aiohttp.ClientTimeout(total=30)
                async with session.get(
                    'https://spectrumsurveys.com/buyers/v2/surveys?limit=1',
                    headers=headers,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            data = await response.json()
                            # Auth worked! data is a list of surveys (or empty list)
                            user_email = self.auth_data.get('user_id', 'User')
                            logger.info(f"✅ Token valid! Authenticated as user {user_email}")
                            logger.info(f"   Found {len(data) if isinstance(data, list) else 'N/A'} surveys")
                            return True
                        else:
                            # Got HTML instead of JSON - auth failed
                            text = await response.text()
                            logger.error(f"❌ Got HTML response instead of JSON (auth failed)")
                            logger.error(f"Response preview: {text[:200]}")
                    else:
                        logger.warning(f"❌ Token expired or invalid (status {response.status})")
            
            # If we get here, we need a fresh token
            logger.error("=" * 80)
            logger.error("⚠️  MANUAL TOKEN EXTRACTION REQUIRED")
            logger.error("=" * 80)
            logger.error("")
            logger.error("PureSpectrum uses a complex captcha that requires manual login.")
            logger.error("Please follow these steps:")
            logger.error("")
            logger.error("1. Open your browser and go to: https://platform.purespectrum.com/login")
            logger.error(f"2. Log in with:")
            logger.error(f"   Username: {self.username}")
            logger.error(f"   Password: {self.password}")
            logger.error("")
            logger.error("3. After successful login, press F12 (Developer Tools)")
            logger.error("4. Go to the 'Console' tab")
            logger.error("5. Copy and paste this command:")
            logger.error("")
            logger.error("   JSON.parse(localStorage.getItem('authStateStorage')).token")
            logger.error("")
            logger.error("6. Copy the token (long string starting with 'eyJ...')")
            logger.error("")
            logger.error("7. Create 'purespectrum_auth.json' in this format:")
            logger.error("   {")
            logger.error('     "token": "PASTE_YOUR_TOKEN_HERE",')
            logger.error('     "user_id": "26340",')
            logger.error('     "company_id": "1853"')
            logger.error("   }")
            logger.error("")
            logger.error("8. Save the file and restart the bot")
            logger.error("")
            logger.error("=" * 80)
            
            return False
            
        except Exception as e:
            logger.error(f"Login check failed: {e}")
            return False
    
    async def get_survey_data(self, session: aiohttp.ClientSession, survey_id: Optional[str] = None) -> Dict:
        """
        Scrape survey data from PureSpectrum API
        
        Args:
            session: aiohttp session
            survey_id: Optional specific survey ID to fetch
        
        Returns:
            Dictionary of survey data
        """
        try:
            # Use PureSpectrum's buyer API endpoint
            if survey_id:
                # Get specific survey
                api_url = f'https://spectrumsurveys.com/buyers/v2/surveys/{survey_id}'
            else:
                # Get all surveys (with pagination)
                api_url = 'https://spectrumsurveys.com/buyers/v2/surveys?UI=1&page=1&limit=100'
            
            logger.info(f"📡 Fetching survey data from API: {api_url}")
            
            headers = self._get_auth_headers()
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with session.get(api_url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Got survey data")
                    
                    # Process the data into our format
                    surveys = {}
                    if isinstance(data, list):
                        # Multiple surveys from list endpoint
                        for survey in data:
                            survey_id = str(survey.get('ps_survey_id') or survey.get('id') or survey.get('_id', 'unknown'))
                            
                            # Map PureSpectrum field names to our standard format
                            surveys[survey_id] = {
                                'surveyId': survey_id,
                                'title': survey.get('survey_title') or survey.get('title', 'Untitled'),
                                'status': self._map_status(survey.get('ps_survey_status')),
                                'statusCode': survey.get('ps_survey_status'),
                                'completes': survey.get('fielded', 0),
                                'target': survey.get('completes_required', 0),
                                'quotas': survey.get('quotas', []),
                                'cpi': survey.get('average_cpi', 0),
                                'loi': survey.get('expected_loi', 0),
                                'incidence': survey.get('expected_ir') or survey.get('current_incidence', 0),
                                'billingId': survey.get('billing_id', ''),
                                'countryCode': survey.get('country_code', ''),
                                'locale': survey.get('locale', {}),
                                'launchDate': survey.get('survey_launch_date'),
                                'lastCompleteDate': survey.get('project_last_complete_date'),
                                'currentCost': survey.get('current_cost', 0),
                                'updatedAt': survey.get('project_last_complete_date') or survey.get('mod_on', ''),
                                # Include full raw data for advanced queries
                                '_raw': survey
                            }
                    elif isinstance(data, dict):
                        # Single survey from detail endpoint
                        survey_id = str(data.get('ps_survey_id') or data.get('id') or data.get('_id', 'unknown'))
                        
                        surveys[survey_id] = {
                            'surveyId': survey_id,
                            'title': data.get('survey_title') or data.get('title', 'Untitled'),
                            'status': self._map_status(data.get('ps_survey_status')),
                            'statusCode': data.get('ps_survey_status'),
                            'completes': data.get('fielded', 0),
                            'target': data.get('completes_required', 0),
                            'quotas': data.get('quotas', []),
                            'cpi': data.get('average_cpi', 0),
                            'loi': data.get('expected_loi', 0),
                            'incidence': data.get('expected_ir') or data.get('current_incidence', 0),
                            'billingId': data.get('billing_id', ''),
                            'countryCode': data.get('country_code', ''),
                            'locale': data.get('locale', {}),
                            'launchDate': data.get('survey_launch_date'),
                            'lastCompleteDate': data.get('project_last_complete_date'),
                            'currentCost': data.get('current_cost', 0),
                            'updatedAt': data.get('project_last_complete_date') or data.get('mod_on', ''),
                            '_raw': data
                        }
                    
                    return surveys
                elif response.status == 401:
                    logger.error("❌ Session expired - please log in again manually")
                    return {}
                else:
                    logger.error(f"❌ API request failed with status {response.status}")
                    text = await response.text()
                    logger.error(f"Response: {text[:500]}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Failed to fetch survey data: {e}")
            return {}
    
    async def get_survey_quotas(self, session: aiohttp.ClientSession, survey_id: str) -> List[Dict]:
        """
        Get quota details for a specific survey
        
        Args:
            session: aiohttp session
            survey_id: Survey ID
            
        Returns:
            List of quota details
        """
        try:
            api_url = f'https://spectrumsurveys.com/buyers/v2/surveys/{survey_id}/quotas?UI=1&QBS=1&page=1&limit=100'
            
            logger.info(f"📊 Fetching quotas for survey {survey_id}")
            
            headers = self._get_auth_headers()
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with session.get(api_url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Got {len(data) if isinstance(data, list) else 'N/A'} quotas")
                    return data if isinstance(data, list) else []
                else:
                    logger.error(f"❌ Failed to get quotas: status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Failed to fetch quotas: {e}")
            return []
    
    async def get_survey_health(self, session: aiohttp.ClientSession, survey_id: str) -> Dict:
        """
        Get health metrics for a specific survey
        
        Args:
            session: aiohttp session
            survey_id: Survey ID
            
        Returns:
            Dictionary of health metrics
        """
        try:
            api_url = f'https://spectrumsurveys.com/buyers/v2/surveys/{survey_id}/health?kpis=AQP'
            
            logger.info(f"🏥 Fetching health metrics for survey {survey_id}")
            
            headers = self._get_auth_headers()
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with session.get(api_url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Got health metrics")
                    return data if isinstance(data, dict) else {}
                else:
                    logger.error(f"❌ Failed to get health metrics: status {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Failed to fetch health metrics: {e}")
            return {}
    
    async def detect_changes(self, current_data: Dict) -> List[Dict]:
        """Detect changes from last known data"""
        changes = []
        
        for survey_id, current in current_data.items():
            if survey_id in self.last_known_data:
                last = self.last_known_data[survey_id]
                
                # Check for changes
                if (current.get('status') != last.get('status') or 
                    current.get('completes') != last.get('completes')):
                    changes.append({
                        'surveyId': survey_id,
                        'event': 'statusUpdate',
                        'status': current.get('status'),
                        'completes': current.get('completes'),
                        'target': current.get('target'),
                        'updatedAt': current.get('updatedAt')
                    })
            else:
                # New survey
                changes.append({
                    'surveyId': survey_id,
                    'event': 'surveyCreated',
                    'status': current.get('status'),
                    'completes': current.get('completes'),
                    'target': current.get('target'),
                    'updatedAt': current.get('updatedAt')
                })
        
        self.last_known_data = current_data.copy()
        return changes


# Helper function to extract token from browser
def print_token_extraction_help():
    """Print instructions for extracting auth token from browser"""
    print("=" * 80)
    print("HOW TO EXTRACT AUTH TOKEN FROM YOUR BROWSER")
    print("=" * 80)
    print()
    print("1. Log in to https://platform.purespectrum.com/login in your browser")
    print()
    print("2. Press F12 to open Developer Tools")
    print()
    print("3. Go to the 'Console' tab")
    print()
    print("4. Paste this JavaScript command and press Enter:")
    print()
    print("   " + "=" * 70)
    print("   JSON.parse(localStorage.getItem('authStateStorage')).token")
    print("   " + "=" * 70)
    print()
    print("5. Copy the token (long string starting with 'eyJ...')")
    print()
    print("6. Create 'purespectrum_auth.json' in this format:")
    print()
    print("   {")
    print('     "token": "PASTE_YOUR_TOKEN_HERE",')
    print('     "user_id": "26340",')
    print('     "company_id": "1853"')
    print("   }")
    print()
    print("7. Save the file in the project root")
    print()
    print("=" * 80)


if __name__ == "__main__":
    # If run directly, show token extraction help
    print_token_extraction_help()

# Live Dashboard Deployment Guide

This guide will help you deploy the live dashboard so analysts can access it with real-time updates on weekends.

## What's Different?

**Static Dashboard (GitHub Pages):**
- Data is embedded when you run `generate_dashboard.py`
- Requires manual updates
- Free hosting on GitHub Pages

**Live Dashboard (Web Server):**
- Fetches fresh data from PureSpectrum API on every page load/refresh
- Updates automatically - no manual intervention needed
- Requires hosting (Render, Heroku, etc.)

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

1. **Create Account:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `SurveyDashboard`

3. **Configure Settings:**
   - **Name:** `survey-dashboard` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (or paid for better performance)

4. **Set Environment Variables:**
   - Go to "Environment" tab
   - Add these variables:
     ```
     PURESPECTRUM_USERNAME=your_username@consultimi.com
     PURESPECTRUM_PASSWORD=your_password
     PORT=10000
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your dashboard will be live at: `https://your-app-name.onrender.com`

### Option 2: Heroku

1. **Install Heroku CLI:**
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create survey-dashboard
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set PURESPECTRUM_USERNAME=your_username@consultimi.com
   heroku config:set PURESPECTRUM_PASSWORD=your_password
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **Open Dashboard:**
   ```bash
   heroku open
   ```

### Option 3: Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project from GitHub repo
4. Add environment variables
5. Deploy automatically

## Testing Locally

Before deploying, test locally:

1. **Set up environment:**
   ```powershell
   # Create .env file (if not exists)
   PURESPECTRUM_USERNAME=your_username@consultimi.com
   PURESPECTRUM_PASSWORD=your_password
   ```

2. **Run the server:**
   ```powershell
   python -m uvicorn app.main:app --reload
   ```

3. **Open in browser:**
   ```
   http://localhost:8000
   ```

4. **Test features:**
   - Page should load surveys automatically
   - Click refresh button - should update
   - Click on a survey - should show quota details
   - Check mobile responsiveness

## Important Notes

### Security
- **Never commit `.env` file** - it contains passwords
- Environment variables are set in hosting platform, not in code
- Dashboard is public (no login) - anyone with link can view

### Performance
- First load may take 5-10 seconds (fetching from PureSpectrum API)
- Subsequent refreshes will also take a few seconds
- Free tier on Render may "spin down" after inactivity (first request after 15 min will be slow)

### Cost
- **Render Free Tier:** Free, but spins down after 15 min inactivity
- **Render Starter:** $7/month - always on
- **Heroku:** No free tier anymore, starts at $5/month
- **Railway:** $5/month with $5 credit

## Recommended Setup

For weekend analyst access, I recommend:

1. **Use Render Free Tier** for now
   - Free to use
   - First request after inactivity may be slow (30-60 seconds)
   - Subsequent requests are fast

2. **Upgrade to Render Starter ($7/month)** if needed
   - Always on, no spin-down delays
   - Better for weekend monitoring

3. **Share the link:**
   ```
   https://your-app-name.onrender.com
   ```
   - Analysts can bookmark this
   - Refresh button updates data in real-time
   - Works on mobile devices

## Troubleshooting

### Dashboard shows "Error: Failed to authenticate"
- Check environment variables are set correctly
- Verify PureSpectrum credentials are valid
- Check `purespectrum_auth.json` token is still valid

### Dashboard loads but shows "No active surveys"
- Check if there are actually active surveys in PureSpectrum
- Verify API is returning data (check browser console)

### Slow loading
- First request after inactivity on free tier is normal (30-60 sec)
- PureSpectrum API calls take a few seconds
- Consider upgrading to paid tier for always-on performance

### Quota details not loading
- Check browser console for errors
- Verify survey ID is correct
- Check API endpoint is accessible

## Support

If you encounter issues:
1. Check Render/Heroku logs for errors
2. Test locally first to isolate issues
3. Verify PureSpectrum API is accessible
4. Check environment variables are set correctly


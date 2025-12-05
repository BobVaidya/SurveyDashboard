# GitHub Pages Live Dashboard Setup

This guide shows you how to host the live dashboard on GitHub Pages (free hosting) while using a backend API for real-time data.

## Architecture

- **Frontend:** Hosted on GitHub Pages (free, static HTML/JS)
- **Backend API:** Hosted on Render/Heroku (handles PureSpectrum API calls)
- **Connection:** Frontend makes API calls to backend

## Step 1: Deploy Backend API

First, deploy the backend API to Render or Heroku:

### Option A: Render (Recommended)

1. Go to https://render.com
2. Create new Web Service from your GitHub repo
3. Settings:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `PURESPECTRUM_USERNAME=your_username@consultimi.com`
   - `PURESPECTRUM_PASSWORD=your_password`
5. Deploy and note your URL: `https://your-app.onrender.com`

### Option B: Heroku

1. Install Heroku CLI
2. Run:
   ```bash
   heroku create your-app-name
   heroku config:set PURESPECTRUM_USERNAME=your_username@consultimi.com
   heroku config:set PURESPECTRUM_PASSWORD=your_password
   git push heroku main
   ```
3. Note your URL: `https://your-app-name.herokuapp.com`

## Step 2: Deploy Frontend to GitHub Pages

1. **Copy the live dashboard file:**
   ```powershell
   Copy-Item dashboard_live.html index_live.html
   ```

2. **Commit and push:**
   ```powershell
   git add dashboard_live.html index_live.html
   git commit -m "Add live dashboard for GitHub Pages"
   git push origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repo: https://github.com/BobVaidya/SurveyDashboard
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `/ (root)`
   - Save

4. **Your dashboard will be at:**
   ```
   https://bobvaidya.github.io/SurveyDashboard/dashboard_live.html
   ```

## Step 3: Configure API URL

When users first visit the dashboard:

1. They'll see an API configuration box at the top
2. Enter your backend API URL (e.g., `https://your-app.onrender.com`)
3. Click "Save"
4. The URL is saved in browser localStorage
5. Dashboard will automatically load surveys

## Alternative: Pre-configure API URL

If you want to pre-configure the API URL so users don't need to enter it:

1. Edit `dashboard_live.html`
2. Find this line:
   ```javascript
   return '';
   ```
3. Replace with:
   ```javascript
   return 'https://your-app.onrender.com'; // Your actual API URL
   ```
4. Commit and push

## Benefits

✅ **Free hosting** on GitHub Pages  
✅ **Live data** - refreshes on every page load  
✅ **No manual updates** needed  
✅ **Shareable link** - analysts can bookmark it  
✅ **Works on mobile** - responsive design  
✅ **Always available** - GitHub Pages is reliable  

## Troubleshooting

### "Please configure API URL first"
- User needs to enter the backend API URL
- Make sure backend is deployed and running
- Check backend URL is correct

### "Failed to load surveys"
- Check backend is running (visit API URL directly)
- Check CORS is enabled (backend should allow requests from GitHub Pages)
- Check browser console for errors

### CORS Issues

If you get CORS errors, update `app/main.py` to allow GitHub Pages:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific: ["https://bobvaidya.github.io"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Two Dashboard Options

You now have two options:

1. **Static Dashboard** (`index.html`)
   - `https://bobvaidya.github.io/SurveyDashboard/`
   - Requires manual updates via `generate_dashboard.py`

2. **Live Dashboard** (`dashboard_live.html`)
   - `https://bobvaidya.github.io/SurveyDashboard/dashboard_live.html`
   - Updates automatically via backend API

## Recommended Setup

For weekend analyst access:
- Use **Live Dashboard** (`dashboard_live.html`)
- Deploy backend to Render (free tier)
- Share the GitHub Pages link
- Analysts can refresh to get latest data


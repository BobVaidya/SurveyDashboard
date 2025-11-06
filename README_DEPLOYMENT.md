# 🤖 Teams Survey Bot - Ready to Deploy!

## ✅ What This Bot Does

Shows PureSpectrum survey data directly in Microsoft Teams:
- **Live Surveys** - All active surveys with progress
- **Survey Status** - Detailed metrics (CPI, LOI, incidence, cost)
- **Quota Breakdown** - Detailed demographics with progress bars

**Exactly like your `test_live_surveys.py` output - but in Teams!**

---

## 🎯 Deployment Setup: Dedicated Channel

You'll create a **#survey-updates** channel where your team can:
- Check survey status anytime
- See quota breakdowns
- Monitor progress together
- Keep survey discussions organized

---

## 📋 Files You Need to Know

### **Start Here:**
1. **`FINAL_DEPLOYMENT_STEPS.md`** ⭐ - Complete step-by-step guide (15 min)
2. **`DEPLOYMENT_CHECKLIST.txt`** - Simple checklist to track progress

### **Code Files:**
- `teams_webhook_bot.py` - Main bot code (ready to deploy!)
- `Procfile` - Railway deployment config
- `runtime.txt` - Python version
- `requirements.txt` - Dependencies

### **Reference:**
- `EXAMPLE_OUTPUT.md` - See what bot responses look like
- `QUICK_DEPLOY_GUIDE.md` - Quick reference
- `RAILWAY_DEPLOY.md` - Detailed Railway guide
- `TEAMS_SETUP.md` - Detailed Teams guide

---

## 🚀 Quick Start (3 Steps)

### Step 1: Deploy to Railway (5 min)
```
1. Go to railway.app
2. Login with GitHub
3. Deploy this repository
4. Add environment variables
5. Generate domain
```

### Step 2: Setup Teams Channel (5 min)
```
1. Create #survey-updates channel
2. Add team members
3. Add Outgoing Webhook
4. Copy security token
```

### Step 3: Connect Them (2 min)
```
1. Add security token to Railway
2. Wait for redeploy
3. Test in Teams!
```

**Total Time: 15 minutes**

---

## 💰 Cost

**$0 - Completely Free!**

- Railway: Free tier ($5/month credits - plenty for this)
- Teams: Already have it
- Azure: Not needed!

---

## 👥 Team Usage

Everyone in #survey-updates can use these commands:

```bash
@Survey Bot live              # Show all active surveys
@Survey Bot status 45104633   # Show survey details
@Survey Bot quotas 45104633   # Show quota breakdown
@Survey Bot help              # Show commands
```

No setup needed for team members - just @mention the bot!

---

## 📊 What Your Team Will See

### Command: `@Survey Bot live`
```
**Found 3 Active Surveys**

**Survey ID:** 45104633
**Title:** MCD FLAGPOLE W218 Menu Heist
**Status:** Active
**Progress:** 9/250 (3.6%)
[█░░░░░░░░░░░░░░] 3.6%
**CPI:** $2.67
...
```

### Command: `@Survey Bot quotas 45104633`
```
**Quota Details for Survey 45104633**

**Nested**
  • **50-65 yr, Male**
    Fielded: 1/36 (2.8%)
    Progress: [█░░░░░░░░░░░░░░░░░░░] 2.8%
    Target: 38 | Open: 37 | In Progress: 0
    
  • **40-49 yr, Male**
    Fielded: 0/26 (0.0%)
    Progress: [░░░░░░░░░░░░░░░░░░░░] 0.0%
    Target: 26 | Open: 26 | In Progress: 0
...
```

**See `EXAMPLE_OUTPUT.md` for full examples!**

---

## 🎯 Architecture

```
Teams Channel (#survey-updates)
    ↓
User: @Survey Bot live
    ↓
Teams Outgoing Webhook
    ↓
Railway (your bot running)
    ↓
PureSpectrum API (fetch data)
    ↓
Format & Return to Teams
    ↓
User sees results in channel
```

**No Azure hosting needed!**

---

## ✅ Features

✅ **No Azure Hosting** - Uses Railway (free tier)  
✅ **No Azure Bot Registration** - Uses Teams Outgoing Webhook  
✅ **Works on Work PC** - No restrictions  
✅ **Team Access** - Everyone in channel can use  
✅ **Multiple Channels** - Add to different channels  
✅ **Real-time Data** - Fetches live from PureSpectrum  
✅ **Detailed Quotas** - Full demographic breakdown  
✅ **Progress Bars** - Visual progress indicators  

---

## 🔧 Technology Stack

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Hosting:** Railway
- **Integration:** Teams Outgoing Webhook
- **Data Source:** PureSpectrum API

---

## 📖 Deployment Instructions

### Option 1: Follow the Checklist
Open `DEPLOYMENT_CHECKLIST.txt` and check off each step as you go.

### Option 2: Follow the Guide
Open `FINAL_DEPLOYMENT_STEPS.md` for detailed instructions with screenshots descriptions.

### Option 3: Quick Deploy
Open `QUICK_DEPLOY_GUIDE.md` for a condensed version.

**All paths get you to the same place in 15 minutes!**

---

## 🧪 Local Testing (Optional)

Want to test before deploying?

```powershell
# Create .env file with credentials
python teams_webhook_bot.py

# Visit in browser
http://localhost:8000/health

# Run test script
python test_webhook.py
```

---

## 🔐 Environment Variables Needed

```env
PURESPECTRUM_USERNAME=svaidya@consultimi.com
PURESPECTRUM_PASSWORD=your-password
TEAMS_SECURITY_TOKEN=token-from-teams
```

That's it! Only 3 variables needed.

---

## 🎉 Success Criteria

You'll know it's working when:

✅ Railway health check shows "healthy"  
✅ Bot responds to `@Survey Bot help`  
✅ Bot shows surveys with `@Survey Bot live`  
✅ Bot shows quotas with `@Survey Bot quotas [ID]`  
✅ Team members can use it  

---

## 🚨 Troubleshooting

**Bot not responding?**
1. Check Railway health: `https://your-url/health`
2. Check Railway logs: Deployments → View Logs
3. Verify security token is set in Railway

**Auth failed?**
- Check PureSpectrum credentials in Railway variables

**See `FINAL_DEPLOYMENT_STEPS.md` for detailed troubleshooting!**

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app
- **Teams Webhook Docs:** https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-outgoing-webhook

---

## 🚀 Ready to Deploy?

### **Start Here:**

1. Print or open `DEPLOYMENT_CHECKLIST.txt`
2. Follow `FINAL_DEPLOYMENT_STEPS.md`
3. Check off items as you complete them
4. Test in Teams!

**Total time: 15 minutes**  
**Cost: $0**  
**Result: Working bot for your team!** 🎉

---

## 📅 What Happens After Deployment?

1. **Immediate:** Team can start using bot commands
2. **Day 1:** Team gets familiar with commands
3. **Week 1:** Bot becomes part of daily workflow
4. **Ongoing:** Monitor surveys efficiently in Teams

---

**Questions? Everything you need is in the guides!**

**Let's deploy! 🚀**


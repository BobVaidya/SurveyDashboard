# 🚀 FINAL DEPLOYMENT - Complete Guide

## Setup: Dedicated #survey-updates Channel

**Time:** 15 minutes total

---

## 📋 PART 1: Deploy Bot to Railway (5 min)

### Step 1: Go to Railway
1. Visit https://railway.app
2. Click **"Login with GitHub"** (or email)
3. Sign up (free - $5/month credits)

### Step 2: Deploy Your Code
1. Click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. Select your `TeamsPsChat` repository
4. Click **"Deploy Now"**

Railway auto-detects Python and starts deployment!

### Step 3: Add Environment Variables
1. In Railway, click **"Variables"** tab
2. Click **"+ New Variable"**
3. Add these three:

```
PURESPECTRUM_USERNAME
Value: svaidya@consultimi.com

PURESPECTRUM_PASSWORD
Value: your-password-here

TEAMS_SECURITY_TOKEN
Value: (leave empty for now)
```

4. Click outside to save

### Step 4: Generate Public URL
1. Click **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `https://teamspschat-production.up.railway.app`)

**✅ Save this URL - you'll need it in Part 2!**

### Step 5: Verify Deployment
Visit in browser: `https://your-bot.up.railway.app/health`

Should see: `{"status":"healthy"}`

✅ **Bot is live on Railway!**

---

## 📋 PART 2: Create Teams Channel & Add Bot (5 min)

### Step 1: Create Dedicated Channel
1. Open **Microsoft Teams**
2. Go to your team (or create new team)
3. Click **"..."** next to team name
4. Click **"Add channel"**
5. Fill in:
   ```
   Channel name: survey-updates
   Description: PureSpectrum survey status and quota monitoring
   Privacy: Standard (or Private if needed)
   ```
6. Click **"Add"**

### Step 2: Add Team Members
1. In the new **#survey-updates** channel
2. Click **"..."** → **"Manage channel"**
3. Click **"Members"** tab
4. Add your team members who need survey access
5. Click **"Done"**

### Step 3: Add Outgoing Webhook to Channel
1. In **#survey-updates** channel
2. Click **"..."** (three dots) next to channel name
3. Click **"Connectors"**
4. Search for **"Outgoing Webhook"**
5. Click **"Add"** (or "Configure")

### Step 4: Configure Webhook
Fill in the form:

```
Name: Survey Bot

Callback URL: https://your-railway-bot.up.railway.app/webhook
(Use the URL you copied from Railway)

Description: Get PureSpectrum survey status and quotas

Upload a picture (optional): Choose any 32x32 image or skip
```

Click **"Create"**

### Step 5: Copy Security Token
**CRITICAL:** Teams will show you a security token in a popup.

**Copy it immediately!** It looks like:
```
abcd1234efgh5678ijkl9012mnop3456qrst7890
```

**Don't close the popup until you've copied it!**

---

## 📋 PART 3: Connect Bot to Teams (2 min)

### Step 1: Add Token to Railway
1. Back to **Railway** → Your project
2. Click **"Variables"** tab
3. Find **TEAMS_SECURITY_TOKEN**
4. Paste the token you copied
5. Click outside to save

Railway will automatically redeploy (takes 30 seconds)

### Step 2: Wait for Redeploy
Watch the **"Deployments"** tab in Railway

When you see: ✅ **"Success"** - you're ready!

---

## 📋 PART 4: Test Your Bot! (3 min)

### Step 1: Go to #survey-updates Channel
In Microsoft Teams, open your new **#survey-updates** channel

### Step 2: Test Help Command
Type:
```
@Survey Bot help
```

**Expected Response:**
```
**Teams Survey Bot - Commands**

• `@SurveyBot live` - Show all active surveys
• `@SurveyBot status <surveyId>` - Show survey status
• `@SurveyBot quotas <surveyId>` - Show quota details
• `@SurveyBot help` - Show this help
...
```

✅ **If you see this, it's working!**

### Step 3: Test Live Surveys
Type:
```
@Survey Bot live
```

**Expected Response:**
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

✅ **Success! You see your live surveys!**

### Step 4: Test Detailed Quotas
Type:
```
@Survey Bot quotas 45104633
```

**Expected Response:**
```
**Quota Details for Survey 45104633**

**Nested**
  • **50-65 yr, Male**
    Fielded: 1/36 (2.8%)
    Progress: [█░░░░░░░░░░░░░░░░░░░] 2.8%
    Target: 38 | Open: 37 | In Progress: 0
  
  • **40-49 yr, Male**
    Fielded: 0/26 (0.0%)
    ...
```

✅ **Perfect! Detailed quotas working!**

---

## 🎉 YOU'RE DONE!

### Your team can now use these commands in #survey-updates:

```
@Survey Bot live              ← Show all active surveys
@Survey Bot status 45104633   ← Show detailed survey status
@Survey Bot quotas 45104633   ← Show detailed quota breakdown
@Survey Bot help              ← Show available commands
```

---

## 👥 Onboard Your Team

### Post this in #survey-updates channel:

```
📊 Survey Bot is now live!

Quick commands:
• @Survey Bot live - See all active surveys
• @Survey Bot status [ID] - Get survey details
• @Survey Bot quotas [ID] - See quota breakdown
• @Survey Bot help - Full command list

Example:
@Survey Bot quotas 45104633
```

Pin this message for easy reference!

---

## 🔧 Troubleshooting

### Bot not responding?

**Check 1: Railway is running**
- Visit: `https://your-bot.up.railway.app/health`
- Should show: `{"status":"healthy"}`

**Check 2: Security token is set**
- Railway → Variables → Check `TEAMS_SECURITY_TOKEN` has a value

**Check 3: Bot name**
- Make sure you @mention exactly: `@Survey Bot`
- Case sensitive, include space

**Check 4: Railway logs**
- Railway → Deployments → View Logs
- Look for errors when you send a command

### "Auth failed" error?

**Check credentials in Railway:**
- `PURESPECTRUM_USERNAME` = svaidya@consultimi.com
- `PURESPECTRUM_PASSWORD` = correct password

### Want to add bot to another channel?

1. Go to the other channel
2. Repeat Part 2, Step 3-5
3. Use the **same callback URL**
4. You can use the same security token or get a new one

---

## 💰 Costs

- ✅ **Railway:** $0 (free $5/month credits - plenty for this)
- ✅ **Teams:** $0 (already have it)
- ✅ **Azure:** $0 (not needed!)

**Total: $0** 🎉

---

## 📊 Usage Tips

### Pin Important Updates
When bot shows critical info, right-click → Pin to channel

### Create Shortcuts
Save common commands in channel description:
- live → Quick status check
- quotas [ID] → Detailed breakdown

### Regular Monitoring
Set up a routine:
- Morning: `@Survey Bot live`
- Check problematic surveys: `@Survey Bot quotas [ID]`

---

## 🚀 Next Steps

**Optional Enhancements:**

1. **Add to more channels** - Sales, Management, etc.
2. **Create alerts** - Pin low-performing quotas
3. **Team training** - Show team how to use commands
4. **Feedback** - Gather team feedback on useful features

---

## ✅ Deployment Checklist

- [ ] Railway account created
- [ ] Code deployed to Railway
- [ ] Environment variables set
- [ ] Railway domain generated
- [ ] Health check passed
- [ ] Teams channel #survey-updates created
- [ ] Team members added to channel
- [ ] Outgoing Webhook configured
- [ ] Security token copied
- [ ] Token added to Railway
- [ ] Bot tested with `help` command
- [ ] Bot tested with `live` command
- [ ] Bot tested with `quotas` command
- [ ] Team onboarded
- [ ] Welcome message posted and pinned

---

## 🎯 Quick Reference

**Railway URL:** https://your-bot.up.railway.app  
**Webhook Endpoint:** https://your-bot.up.railway.app/webhook  
**Health Check:** https://your-bot.up.railway.app/health  
**Teams Channel:** #survey-updates  

**Commands:**
- `@Survey Bot live`
- `@Survey Bot status [ID]`
- `@Survey Bot quotas [ID]`
- `@Survey Bot help`

---

**Ready to deploy? Start with Part 1! 🚀**

**Questions? Check Railway logs or the troubleshooting section above.**


# Teams App Package Instructions

## Step 1: Create Icon Files (2 minutes)

You need two icon files in the `teams-app` folder:

### Option A: Quick Placeholders (Easiest)

1. Go to: https://via.placeholder.com/192x192/4A90E2/FFFFFF?text=Survey
2. Right-click → Save Image As → Save as `color.png` in the `teams-app` folder

3. Go to: https://via.placeholder.com/32x32/FFFFFF/4A90E2?text=S
4. Right-click → Save Image As → Save as `outline.png` in the `teams-app` folder

### Option B: Use Any Images You Have

- **color.png** - 192x192 pixels, colorful icon
- **outline.png** - 32x32 pixels, simple icon

Just name them correctly and put them in `teams-app` folder.

---

## Step 2: Create ZIP File (1 minute)

1. Open File Explorer
2. Go to: `C:\Users\SwanandVaidya\TeamsPsChat\teams-app`
3. Select these 3 files:
   - ✅ manifest.json
   - ✅ color.png
   - ✅ outline.png
4. Right-click → **Send to** → **Compressed (zipped) folder**
5. Name it: `SurveyBot.zip`
6. Move `SurveyBot.zip` to your Desktop or Documents folder

---

## Step 3: Upload to Teams (2 minutes)

### On Your Work PC:

1. Open **Microsoft Teams**
2. Click **Apps** (left sidebar, bottom)
3. Click **"Manage your apps"** (or **"...")** → **"Upload a custom app"**)
4. Click **"Upload for me"** or **"Upload for [Your Team Name]"**
   - Choose "Upload for me" if available
5. Select `SurveyBot.zip`
6. Click **"Add"**

**Your bot is now in your work Teams!**

---

## Step 4: Test the Bot

After uploading:

1. The bot should open automatically, or
2. Go to **Apps** → Search "Survey Bot" → Click it → **"Add"**

### Test in 1-on-1 Chat:

Type: `help`
Should show available commands!

Type: `status 45104633`
Should show survey status!

Type: `quotas 45104633`
Should show detailed quotas!

---

## Step 5: Add to Channel

Once working in 1-on-1:

1. Go to your test channel
2. Click **"+"** tab at top
3. Search for **"Survey Bot"**
4. Add it to the channel

Or just @mention it:
```
@Survey Bot help
```

---

## ✅ Success Criteria

- ✅ ZIP file created with 3 files
- ✅ Uploaded to Teams
- ✅ Bot responds to `help` command
- ✅ Bot shows survey status
- ✅ Bot shows quota details
- ✅ Can use in channels and 1-on-1

---

## 🆘 Troubleshooting

**"Can't upload custom apps"**
→ Your organization disabled custom apps
→ Contact IT admin to allow custom apps or upload for you

**"Invalid manifest"**
→ Make sure all 3 files are in the ZIP
→ Files must be at root of ZIP (not in a subfolder)

**"Bot not responding"**
→ Check Render is still running (https://teamspschat.onrender.com/healthz)
→ Check Azure Bot messaging endpoint is correct

---

**Start with Step 1 - create the icons!**


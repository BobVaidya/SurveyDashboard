# 🚀 Create Teams App Package - Quick Guide

## ⏱️ Total Time: 5 Minutes

---

## **Step 1: Download Icon Images (2 min)**

### **Download Color Icon:**

1. Right-click this link and "Save Link As":
   - https://via.placeholder.com/192x192/0078D4/FFFFFF?text=Survey+Bot
2. Save as `color.png` in: `C:\Users\SwanandVaidya\TeamsPsChat\teams-app\`

### **Download Outline Icon:**

1. Right-click this link and "Save Link As":
   - https://via.placeholder.com/32x32/FFFFFF/0078D4?text=SB  
2. Save as `outline.png` in: `C:\Users\SwanandVaidya\TeamsPsChat\teams-app\`

**Or just use any 2 PNG images you have and rename them!**

---

## **Step 2: Create ZIP Package (1 min)**

1. Open File Explorer
2. Navigate to: `C:\Users\SwanandVaidya\TeamsPsChat\teams-app`
3. You should see:
   - ✅ manifest.json (I created this)
   - ✅ color.png (you just downloaded)
   - ✅ outline.png (you just downloaded)

4. **Select all 3 files** (Ctrl+Click each one)
5. Right-click on the selected files
6. Choose **"Send to"** → **"Compressed (zipped) folder"**
7. Name it: `SurveyBot.zip`

**IMPORTANT:** Make sure the 3 files are at the ROOT of the ZIP, not in a subfolder!

To verify:
- Open the ZIP file
- You should see the 3 files directly (not inside another folder)

---

## **Step 3: Upload to Work Teams (2 min)**

### **On Your Work PC:**

1. Open **Microsoft Teams** (your work Teams)
2. Click **"Apps"** icon in the left sidebar (looks like a grid)
3. At the bottom left, click **"Manage your apps"** or look for **"Upload a custom app"** option
4. Click **"Upload a custom app"** or **"Upload for..."**
5. Select **Upload for me** (or your team if you want to share)
6. Browse and select: `SurveyBot.zip`
7. Click **"Add"** or **"Open"**

**Teams will install your bot!**

---

## **Step 4: Open Your Bot (1 min)**

After upload:

1. Search for **"Survey Bot"** in Teams Apps
2. Click on it
3. Click **"Add"**
4. A chat window with your bot will open

---

## **Step 5: TEST IT! 🎉**

In the chat with your bot, type:

```
help
```

**Expected:** Bot shows list of commands

```
status 45104633
```

**Expected:** Bot shows survey status with progress bar

```
quotas 45104633
```

**Expected:** Bot shows detailed quota breakdown!

---

## ✅ **Once Working - Add to Channel**

1. Go to your test channel
2. Click the **"+"** tab at the top
3. Search for **"Survey Bot"**
4. Add it

Or just @mention it in the channel:
```
@Survey Bot help
```

---

## 🆘 **Can't Upload Custom Apps?**

If you see "Custom apps are blocked by your organization":

1. Ask your IT admin to enable custom apps, OR
2. Ask IT admin to upload the bot for you (give them the ZIP)

---

## 📋 **Quick Checklist**

- [ ] Downloaded color.png to teams-app folder
- [ ] Downloaded outline.png to teams-app folder
- [ ] Created SurveyBot.zip with 3 files
- [ ] Opened Teams → Apps → Manage your apps
- [ ] Uploaded SurveyBot.zip
- [ ] Bot installed successfully
- [ ] Tested with `help` command
- [ ] Tested with `status` command
- [ ] Tested with `quotas` command
- [ ] Added to test channel

---

**Start with Step 1 - download the icons!**

Then follow steps 2-5 and you'll have a working bot in 5 minutes! 🚀


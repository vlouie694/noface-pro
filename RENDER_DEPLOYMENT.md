# Deploying NoFace-Pro to Render

This guide walks you through deploying the CPN Profile Generator Bot to Render.

## Prerequisites

1. **GitHub Account** - Already have one ✅
2. **Render Account** - [Sign up at render.com](https://render.com)
3. **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather) on Telegram

## Step-by-Step Deployment

### Step 1: Connect GitHub to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** button (top right)
3. Select **"Web Service"**
4. Click **"Connect a repository"**
5. Authorize Render to access your GitHub account
6. Search for `vlouie694/noface-pro` repository
7. Click **"Connect"** next to the repository

### Step 2: Configure Web Service

Fill in the following details on the Render form:

| Field | Value |
|-------|-------|
| **Name** | `noface-pro-bot` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot_main.py` |
| **Instance Type** | `Free` (testing) or `Starter` (production) |
| **Region** | Choose your closest region |

### Step 3: Add Environment Variables

1. Scroll down to **Environment Variables** section
2. Click **"Add Environment Variable"** button
3. Add this variable:

```
KEY:   TELEGRAM_BOT_TOKEN
VALUE: [Your_Bot_Token_From_BotFather]
```

**How to get your bot token:**
- Open Telegram and message [@BotFather](https://t.me/botfather)
- Send `/newbot` command
- Follow the prompts and choose a name for your bot
- Copy the token provided (looks like: `123456789:ABCdefGHIjklmnoPQRstuvWXYZ`)
- Paste it in the VALUE field above

### Step 4: Deploy

1. Click **"Create Web Service"** button at the bottom
2. Render will automatically start the build process
3. Watch the **Logs** section for deployment progress
4. You should see messages like:
   - `Cloning repository...`
   - `Building...`
   - `Installing dependencies...`
5. Wait for the message: **"Your service is live"** ✅

### Step 5: Test Your Bot

1. Open Telegram
2. Search for your bot (by the name you gave it to BotFather)
3. Or click the link provided by BotFather
4. Send the `/start` command
5. If you get a welcome response, **deployment is successful!** 🎉

---

## File Structure

Your repository now has everything needed for Render deployment:

```
noface-pro/
├── bot_main.py              # Main entry point
├── bot_commands.py          # Bot commands implementation
├── validation_api.py        # CPN validation API (NEW)
├── profile_generator.py     # Profile generation logic
├── profile_storage.py       # Data storage management
├── luhn_algorithm.py        # Luhn validation algorithm
├── constants.py             # Constants
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Poetry configuration
├── Procfile                # Process definition (NEW)
├── render.yaml             # Render configuration (NEW)
├── RENDER_DEPLOYMENT.md    # This deployment guide (NEW)
└── data/                   # Data directory (created at runtime)
```

---

## ⚠️ Important Considerations

### Free Tier Limitations
- **Service spins down after 15 minutes of inactivity** - Your bot won't respond while dormant
- **750 hours/month limit** - Approximately 31 days
- **Data resets between deploys** - Use persistent disk or database for production

### Recommended Solutions

**Option 1: Upgrade to Paid Plan**
- No spin-down (bot always active)
- More resources and better performance
- Better for production use

**Option 2: Use Webhook Mode (Advanced)**
- Keeps bot active 24/7
- Better resource efficiency
- Requires modifying `bot_main.py`

**Option 3: Add Persistent Storage**
- Use Render's persistent disk feature
- Or integrate a database (PostgreSQL)
- Ensures data survives redeploys

---

## Your New CPN Validation API

The `validation_api.py` file you now have provides:

✅ **Format Validation**
- Checks if CPN is exactly 9 digits
- Verifies it contains only numbers
- Validates it's within the acceptable range

✅ **Luhn Check Digit Verification**
- Ensures CPN passes Luhn algorithm
- Detects invalid CPNs

✅ **Issuance Status Checking**
- Checks against existing profiles
- Returns USED or UNUSED status

✅ **Comprehensive Error Messages**
- Clear feedback on validation failures
- JSON-formatted responses

### Example API Response

```json
{
  "cpn": 123456789,
  "valid": true,
  "status": "VALID_UNUSED",
  "message": "CPN is valid and unused",
  "format_validation": {
    "format_valid": true,
    "format_message": "CPN format is valid"
  },
  "luhn_validation": {
    "luhn_valid": true,
    "luhn_message": "Luhn check digit is valid"
  },
  "issuance_check": {
    "is_issued": false,
    "issued_status": "UNUSED",
    "issued_message": "CPN 123456789 is unused and available"
  },
  "timestamp": "2026-07-15T02:39:46.123456"
}
```

---

## Troubleshooting

### 🔴 Bot doesn't respond

**Check these:**
- ✓ Is `TELEGRAM_BOT_TOKEN` set correctly? (Copy-paste from BotFather)
- ✓ Is the service showing "Your service is live"?
- ✓ Free tier? Service may have spun down (send message again to wake it)
- ✓ Check Render logs for error messages

**Solution:**
1. Go to Render dashboard
2. Click on your service
3. Check the "Logs" tab for errors
4. If token issue, update environment variable and redeploy

### 🔴 "Service not live" error

**Check these:**
- ✓ Python version is 3.10+
- ✓ `requirements.txt` is in root directory
- ✓ No syntax errors in Python files
- ✓ All imports are available

**Solution:**
1. Review build logs in detail
2. Ensure all dependencies are in `requirements.txt`
3. Click "Redeploy" to try again

### 🔴 Commands not found

**Solution:**
1. Send `/start` command first
2. If that works, try `/help`
3. Restart service in Render dashboard
4. Check `bot_commands.py` for command definitions

### 🔴 Data not persisting

**Cause:** Free tier doesn't persist data between deploys

**Solutions:**
1. Upgrade to paid plan ($7+/month)
2. Add persistent disk to Render service
3. Integrate a database (PostgreSQL recommended)

---

## Managing Your Deployment

### View Logs
```
Render Dashboard → Your Service → Logs tab
```
Shows real-time activity and errors

### Redeploy
```
Render Dashboard → Your Service → Redeploy button
```
Rebuilds and restarts the service

### Update Environment Variables
```
Render Dashboard → Your Service → Environment tab
```
Changes take effect on next deploy

### Update Code
```
Push changes to GitHub main branch
```
Auto-deploys if enabled in Render settings

---

## Next Steps

1. ✅ **Deploy the bot** (follow steps above)
2. 📝 **Test all commands** in Telegram
3. 👀 **Monitor logs** for issues
4. 💾 **Backup profiles** if using production
5. 🚀 **Consider paid plan** for production use

---

## Quick Reference Links

- 🌐 **Render Dashboard**: https://dashboard.render.com
- 🤖 **Telegram BotFather**: https://t.me/botfather
- 📚 **Python Telegram Bot**: https://python-telegram-bot.readthedocs.io
- 📖 **Render Documentation**: https://render.com/docs
- 🔐 **Your Repository**: https://github.com/vlouie694/noface-pro

---

## Environment Variables Summary

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | `123456789:ABC...` | From @BotFather |
| `PORT` | ❌ No | `8080` | Webhook port (auto-set) |
| `RENDER_EXTERNAL_URL` | ❌ No | `https://...` | Set by Render automatically |

---

**You're all set! Your bot is ready for deployment.** 🚀

If you encounter any issues:
1. Check the logs first
2. Review this guide's troubleshooting section
3. Verify environment variables are correct
4. Ensure all files are in the repository

**Happy Deploying!**

# VAPI Webhook Configuration Guide

## Quick Setup (For Testing Now)

### Step 1: Your Current ngrok URL

**Your webhook URL (active now):**
```
https://nonsuppressive-overplentifully-alberto.ngrok-free.dev/webhook/vapi
```

⚠️ **Important**: This URL only works while ngrok is running!

### Step 2: Configure in VAPI Dashboard

1. **Go to VAPI Dashboard**:
   ```
   https://dashboard.vapi.ai/assistants
   ```

2. **Find your assistant**:
   - Look for assistant ID: `678bd43a-a18c-49dc-b7a5-ab3ba48048ef`
   - Click on it to open

3. **Edit the assistant**:
   - Click the "Edit" button (usually top right)
   - Scroll to find "Server URL" or "Webhook URL" field

4. **Paste your webhook URL**:
   ```
   https://nonsuppressive-overplentifully-alberto.ngrok-free.dev/webhook/vapi
   ```

5. **Save** the assistant

### Step 3: Test It!

Now make a test call:
- Use VAPI's "Test" button in the dashboard, OR
- Call your VAPI phone number
- Have a conversation about creating an SOP
- The webhook will be triggered automatically!

### Step 4: Monitor the Request

While testing, watch in real-time:

**ngrok Inspector** (shows all incoming requests):
```
http://localhost:4040
```

**Server Logs** (your terminal running Flask):
- You'll see: "Processing voice to SOP for call..."
- "Generating SOP from transcript"
- "Sending SOP to Lindy"

---

## Production Setup

For production, you need a **permanent URL** (not ngrok). Here are your options:

### Option 1: Railway (Easiest, Free)

**Time**: 10 minutes | **Cost**: Free tier available

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   # OR
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login and deploy**:
   ```bash
   cd C:\Projects\voice_sop
   railway login
   railway init
   railway up
   ```

3. **Get your URL**:
   - Railway will give you: `https://yourapp.railway.app`
   - Your webhook: `https://yourapp.railway.app/webhook/vapi`

4. **Update VAPI** with the Railway URL

### Option 2: Heroku (Classic)

**Time**: 15 minutes | **Cost**: $5-7/month

1. **Install Heroku CLI**:
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile** (already done):
   ```
   web: gunicorn app:app
   ```

3. **Deploy**:
   ```bash
   cd C:\Projects\voice_sop
   heroku login
   heroku create your-sop-app
   git init
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

4. **Your URL**: `https://your-sop-app.herokuapp.com/webhook/vapi`

### Option 3: ngrok with Reserved Domain (Quick Production)

**Time**: 5 minutes | **Cost**: $8/month | **Best for**: Quick production without deployment

1. **Sign up for ngrok paid**:
   - Go to: https://dashboard.ngrok.com/billing
   - Subscribe ($8/month)

2. **Reserve a domain**:
   - Go to: https://dashboard.ngrok.com/cloud-edge/domains
   - Click "New Domain"
   - Get: `yourapp.ngrok.app` (permanent!)

3. **Start ngrok with your domain**:
   ```bash
   ngrok http 5000 --domain=yourapp.ngrok.app
   ```

4. **Webhook URL**: `https://yourapp.ngrok.app/webhook/vapi`
   - **This URL never changes!**

### Option 4: DigitalOcean Droplet

**Time**: 30 minutes | **Cost**: $6/month | **Best for**: Full control

1. **Create Droplet**:
   - Go to: https://cloud.digitalocean.com
   - Create Ubuntu 22.04 droplet ($6/month)

2. **SSH and setup**:
   ```bash
   ssh root@your-droplet-ip
   apt update && apt install python3-pip nginx
   ```

3. **Deploy with Docker**:
   ```bash
   # Copy your docker-compose.yml to server
   docker-compose up -d
   ```

4. **Get domain** (optional):
   - Use DigitalOcean DNS or Namecheap
   - Point to your droplet IP
   - **Webhook**: `https://yourdomain.com/webhook/vapi`

---

## Recommendation for You

**For Testing (Right Now)**:
- ✅ Use current ngrok URL
- ✅ Keep your terminal open
- ✅ Test with real VAPI calls

**For Production (This Week)**:
- 🌟 **Railway** (easiest, free to start)
- OR ngrok Reserved Domain ($8/month, zero deployment)

**For Scale (Later)**:
- DigitalOcean or AWS when you have 100+ calls/day

---

## Environment Variables for Production

When deploying, set these environment variables:

```bash
# Required
VAPI_API_KEY=your_vapi_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GHL_API_KEY=your_ghl_api_key_here
LINDY_WEBHOOK_URL=your_lindy_webhook_url_here

# Optional
GOOGLE_CREDENTIALS_PATH=./credentials/google_credentials.json
DATABASE_URL=sqlite:///voice_sop.db
```

For Railway/Heroku, paste these in their dashboard.

---

## Quick Deploy to Railway (Recommended)

```bash
# 1. Install Railway
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
cd C:\Projects\voice_sop
railway init
railway up

# 4. Add environment variables
railway variables set VAPI_API_KEY=your_key
railway variables set OPENAI_API_KEY=your_key
railway variables set GHL_API_KEY=your_key
railway variables set LINDY_WEBHOOK_URL=your_url

# 5. Get your URL
railway status
```

Your webhook will be: `https://voice-sop-production.up.railway.app/webhook/vapi`

---

## Testing Checklist

After configuring VAPI webhook:

- [ ] ngrok/server is running
- [ ] Webhook URL is set in VAPI dashboard
- [ ] Made a test call to VAPI assistant
- [ ] Checked ngrok inspector (http://localhost:4040)
- [ ] Saw "Processing voice to SOP" in server logs
- [ ] Lindy received the webhook
- [ ] SOP was generated successfully

---

## Troubleshooting

**VAPI says "webhook failed"?**
- Check ngrok is running: `http://localhost:4040`
- Test health endpoint: `curl https://your-ngrok-url.ngrok.io/health`
- Check server logs for errors

**No webhook received?**
- Verify URL in VAPI dashboard is correct
- Make sure URL ends with `/webhook/vapi`
- Check ngrok inspector for incoming requests

**Webhook received but error?**
- Check server logs in your terminal
- Look for Python errors
- Verify environment variables are set

---

## Need Help?

Check these logs:
1. **Server logs**: Your Flask terminal
2. **ngrok inspector**: http://localhost:4040
3. **VAPI logs**: VAPI dashboard > Calls > View logs

All working? You're live! 🚀

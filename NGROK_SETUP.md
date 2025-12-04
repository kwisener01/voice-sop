# ngrok Setup Guide

## Installing ngrok

### Option 1: Download from Website
1. Go to: https://ngrok.com/download
2. Download for Windows
3. Extract to a folder (e.g., `C:\ngrok\`)
4. Add to PATH or run from that folder

### Option 2: Using Chocolatey (if installed)
```bash
choco install ngrok
```

### Option 3: Using winget
```bash
winget install ngrok
```

## Setting Up ngrok

1. **Sign up for free account**: https://dashboard.ngrok.com/signup
2. **Get your auth token**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Add auth token**:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

## Running ngrok

### Option A: Using the provided script
```bash
start_ngrok.bat
```

### Option B: Manual command
```bash
ngrok http 5000
```

## What You'll See

When ngrok starts, you'll see something like:

```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Your public URL is**: `https://abc123.ngrok.io`

## Configure VAPI with ngrok URL

1. Copy your ngrok URL (e.g., `https://abc123.ngrok.io`)
2. Go to VAPI Dashboard: https://dashboard.vapi.ai
3. Find assistant: `678bd43a-a18c-49dc-b7a5-ab3ba48048ef`
4. Edit > Server URL
5. Set to: `https://abc123.ngrok.io/webhook/vapi`
6. Save

## Testing

1. **Check ngrok is working**:
   ```bash
   curl https://abc123.ngrok.io/health
   ```

2. **View requests in real-time**:
   - Open: http://localhost:4040
   - This shows all incoming requests to your tunnel

3. **Make a test call**:
   - Use VAPI's test feature
   - Or call your VAPI phone number
   - Watch requests come in at http://localhost:4040

## Keeping ngrok Running

**Important**: ngrok must stay running for VAPI to reach your server!

### Option 1: Keep terminal open
- Run `start_ngrok.bat`
- Keep that window open
- Don't close it!

### Option 2: Run in background (advanced)
```bash
# Windows - run in background
start /B ngrok http 5000
```

## Free vs Paid ngrok

**Free tier**:
- ✓ Random URL each time (e.g., `abc123.ngrok.io`)
- ✓ 40 connections/minute
- ✓ Perfect for development
- ⚠ URL changes when you restart

**Paid tier** ($8/month):
- ✓ Custom subdomain (e.g., `yourapp.ngrok.io`)
- ✓ Fixed URL - never changes
- ✓ More connections
- ✓ Better for production testing

## Troubleshooting

**Command not found?**
- Make sure ngrok is in your PATH
- Or run from ngrok.exe location directly

**Auth token error?**
- Run: `ngrok config add-authtoken YOUR_TOKEN`
- Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

**Tunnel not working?**
- Check if port 5000 is actually running: `curl http://localhost:5000/health`
- Restart ngrok
- Check firewall settings

**Want to see what's happening?**
- Open ngrok web interface: http://localhost:4040
- Shows all requests in real-time!

## Production Alternative

For production, instead of ngrok, deploy to:
- **Railway**: Easy, free tier, automatic HTTPS
- **Heroku**: Classic platform, free tier
- **DigitalOcean**: $5/month droplet
- **Fly.io**: Free tier, fast deployment
- **Google Cloud Run**: Pay per use

See `docker-compose.yml` for deployment configs.

# Voice SOP Generator - Complete Setup Guide

## Getting Your Phone Number for Customer Calls

### Option 1: Using VAPI Phone Number (Recommended)

1. **Get a VAPI Phone Number**:
   - Log into your VAPI dashboard: https://dashboard.vapi.ai
   - Go to "Phone Numbers" section
   - Click "Buy Phone Number"
   - Select a number (US, Canada, or international)
   - Purchase the number

2. **Assign Assistant to Number**:
   - In VAPI dashboard, click on your phone number
   - Under "Assistant", select the assistant you created
   - Save the configuration

3. **Test the Number**:
   - Call the phone number
   - The VAPI assistant will answer and start the conversation
   - After the call, VAPI will send the transcript to your webhook

### Option 2: Using GoHighLevel Phone Number

1. **Get GHL Phone Number**:
   - Log into GoHighLevel
   - Go to Settings > Phone Numbers
   - Purchase or port a phone number

2. **Forward to VAPI**:
   - In GHL, create a workflow/trigger for incoming calls
   - Use the "Make Phone Call" action
   - Configure it to transfer to VAPI assistant phone number
   - OR use GHL's API to trigger VAPI call

### Option 3: Using Lindy to Manage Calls

1. **Set up Lindy Workflow**:
   - Create a new Lindy agent
   - Add trigger: "When GHL receives a call" or "Incoming call"
   - Add action: "Start VAPI call"
   - Map customer information to VAPI

2. **Configure Lindy Integration**:
   - Your Lindy webhook URL is already in `.env`:
     ```
     LINDY_WEBHOOK_URL=https://public.lindy.ai/api/v1/webhooks/lindy/38537f6a-8894-4dc7-99d5-131bd5346b21
     ```

## Complete Integration Flow

### Step 1: Create VAPI Assistant

Using the admin panel (http://localhost:5000/):

1. Fill in the assistant form:
   - Name: "SOP Voice Assistant"
   - Model: "gpt-4"
   - Voice Provider: "11labs"
   - Voice ID: Get from ElevenLabs dashboard
   - System Prompt: (use the default SOP generation prompt)
   - First Message: "Hello! I'm here to help create your SOP..."
   - Webhook URL: Your public server URL + `/webhook/vapi`

2. Click "Create Assistant"
3. Note the Assistant ID returned

### Step 2: Set Up Your Server for Public Access

Since VAPI needs to send webhooks to your server:

#### Option A: Using ngrok (for testing)

```bash
# Install ngrok from https://ngrok.com
ngrok http 5000
```

This will give you a public URL like: `https://abc123.ngrok.io`

#### Option B: Using localhost.run (quick alternative)

```bash
ssh -R 80:localhost:5000 localhost.run
```

#### Option C: Deploy to production (recommended)

Deploy to:
- Heroku
- Railway
- DigitalOcean
- AWS EC2
- Google Cloud Run

### Step 3: Update VAPI Assistant Webhook

1. In VAPI dashboard, go to your assistant
2. Update the webhook URL to:
   ```
   https://your-public-url/webhook/vapi
   ```
3. Save changes

### Step 4: Configure Lindy Automation

1. **In Lindy Dashboard**:
   - Create new workflow
   - Name: "SOP Generation Flow"

2. **Add Trigger**:
   - Option 1: "When GHL contact is created"
   - Option 2: "When incoming call received"
   - Option 3: "Custom webhook"

3. **Add Actions**:
   ```
   Action 1: Initiate VAPI Call
   - Phone Number: {{contact.phone}}
   - Assistant ID: [Your VAPI Assistant ID]

   Action 2: Wait for VAPI Webhook
   - Listen for webhook from your server

   Action 3: Process SOP (optional)
   - Your server handles this automatically
   ```

4. **Configure Webhook Endpoints**:
   - Lindy → Your Server: `https://your-public-url/webhook/lindy`
   - Your Server → Lindy: Use `LINDY_WEBHOOK_URL` from `.env`

### Step 5: Test the Complete Flow

1. **Start Your Server**:
   ```bash
   python app.py
   ```

2. **Expose It Publicly** (if using ngrok):
   ```bash
   ngrok http 5000
   ```

3. **Test Call Flow**:
   - Call your VAPI/GHL phone number
   - Have a conversation about creating an SOP
   - End the call
   - Check your server logs for webhook receipt
   - Verify SOP document is created in Google Docs
   - Check GHL for SMS/Email delivery

## Finding Your Phone Number

### Where to Find Your Number:

1. **VAPI Dashboard**:
   - https://dashboard.vapi.ai
   - Click "Phone Numbers"
   - Your purchased numbers are listed here
   - Click to see details and configuration

2. **GoHighLevel**:
   - Settings > Phone Numbers
   - View all your GHL numbers
   - See which workflows are assigned

3. **Test with VAPI Playground**:
   - In VAPI dashboard, use the "Test" feature
   - Make a test call to verify your assistant works
   - Check webhook delivery

## Environment Variables Summary

Make sure these are set in your `.env`:

```bash
# VAPI
VAPI_API_KEY=your_vapi_key

# OpenAI
OPENAI_API_KEY=your_openai_key

# GoHighLevel
GHL_API_KEY=your_ghl_key

# Lindy
LINDY_WEBHOOK_SECRET=optional_secret
LINDY_WEBHOOK_URL=your_lindy_webhook_url

# Google
GOOGLE_CREDENTIALS_PATH=./credentials/google_credentials.json
GOOGLE_FOLDER_ID=your_folder_id
```

## Troubleshooting

### Problem: VAPI Not Sending Webhooks

**Solution**:
- Verify webhook URL is publicly accessible
- Check VAPI dashboard > Assistant > Webhook URL is correct
- Use ngrok or similar to expose local server
- Check server logs for incoming requests

### Problem: Don't Have a Phone Number Yet

**Solution**:
1. Buy number from VAPI dashboard ($2-5/month)
2. Or use existing GHL number
3. Or use VAPI's test call feature

### Problem: Can't Receive Calls

**Solution**:
- Verify assistant is assigned to phone number in VAPI
- Check GHL workflow is active
- Test with VAPI playground first
- Verify phone number is not blocked

## Quick Start Checklist

- [ ] VAPI account created
- [ ] Phone number purchased/configured
- [ ] VAPI assistant created with webhook URL
- [ ] Server running and publicly accessible
- [ ] Google credentials configured
- [ ] GHL API key added
- [ ] Lindy workflow created (optional)
- [ ] Test call completed successfully
- [ ] SOP document created in Google Docs
- [ ] Document delivered via GHL

## Support Resources

- **VAPI Documentation**: https://docs.vapi.ai
- **VAPI Discord**: Join for community support
- **GoHighLevel Support**: https://support.gohighlevel.com
- **Lindy Documentation**: https://www.lindy.ai/docs
- **Google Cloud Console**: https://console.cloud.google.com

## Next Steps

1. Get your VAPI phone number
2. Expose your server publicly (ngrok for testing)
3. Update VAPI assistant webhook URL
4. Make a test call
5. Verify SOP generation works end-to-end

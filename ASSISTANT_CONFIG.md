# Your VAPI Assistant Configuration

## Assistant Details

**Assistant ID**: `678bd43a-a18c-49dc-b7a5-ab3ba48048ef`

## Webhook Configuration

### For Local Testing (Current)
```
Webhook URL: http://localhost:5000/webhook/vapi
```

### For Production (After deploying)
```
Webhook URL: https://your-domain.com/webhook/vapi
```

Or with ngrok:
```
Webhook URL: https://abc123.ngrok.io/webhook/vapi
```

## How to Configure in VAPI Dashboard

1. **Login**: https://dashboard.vapi.ai
2. **Navigate to**: Assistants
3. **Find**: Assistant ID `678bd43a-a18c-49dc-b7a5-ab3ba48048ef`
4. **Click**: Edit or Settings
5. **Update**: Server URL / Webhook URL field
6. **Save**: Changes

## Testing Your Setup

### Option 1: Test Endpoint (No Real Call Needed)

Visit or POST to:
```
http://localhost:5000/test/vapi-webhook
```

This will simulate a complete VAPI call and:
- ✓ Generate an SOP using GPT-4
- ✓ Create a Google Doc
- ✓ Send via GoHighLevel (if contact exists)

### Option 2: VAPI Test Call

1. In VAPI dashboard, click "Test" on your assistant
2. VAPI will call you
3. Have a conversation about an SOP
4. Webhook will be triggered automatically

### Option 3: Real Phone Call

1. Assign your assistant to a phone number in VAPI
2. Call that number
3. Have the conversation
4. System processes it automatically

## Webhook Payload Example

When VAPI sends data to your webhook, it looks like:

```json
{
  "call": {
    "id": "call_abc123",
    "assistantId": "678bd43a-a18c-49dc-b7a5-ab3ba48048ef",
    "status": "ended"
  },
  "transcript": "Full conversation transcript...",
  "customer": {
    "name": "Customer Name",
    "phone": "+1234567890",
    "contact_id": "ghl_contact_id"
  }
}
```

## Making Your Server Publicly Accessible

### Using ngrok (Easiest for Testing)

```bash
# In a new terminal:
ngrok http 5000

# This gives you a URL like:
# https://abc123.ngrok.io

# Update VAPI webhook to:
# https://abc123.ngrok.io/webhook/vapi
```

### Using localhost.run

```bash
ssh -R 80:localhost:5000 localhost.run
```

### Deploy to Production

See `docker-compose.yml` for deployment options:
- Heroku
- Railway
- DigitalOcean
- AWS
- Google Cloud

## Flow Summary

```
1. Customer calls VAPI number
2. VAPI assistant (678bd43a...) answers
3. Conversation happens
4. VAPI sends transcript to your webhook
5. Your app generates SOP with GPT-4
6. Google Doc is created
7. Document sent via GHL SMS + Email
```

## Troubleshooting

**Webhook not receiving data?**
- Check VAPI dashboard webhook URL is correct
- Verify server is running: `http://localhost:5000/health`
- Test with: `http://localhost:5000/test/vapi-webhook`

**401 Errors?**
- You don't need to create assistants via API
- Just configure the existing one in VAPI dashboard
- The webhook will work regardless of API key issues

**Need to expose server?**
- Use ngrok: `ngrok http 5000`
- Update VAPI webhook URL accordingly

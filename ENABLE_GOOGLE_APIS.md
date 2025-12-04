# Enable Google APIs - Quick Guide

## The Issue
Google Docs API is not enabled for your project. You need to enable it to create documents.

## Solution (5 minutes)

### Step 1: Go to Google Cloud Console
Click this link (it will take you directly to enable the API):
```
https://console.developers.google.com/apis/api/docs.googleapis.com/overview?project=341497862364
```

Or manually:
1. Go to: https://console.cloud.google.com
2. Select project: `my-business-apps-464200`
3. Search for "Google Docs API" in the search bar
4. Click on it

### Step 2: Enable the API
1. Click the big blue **"ENABLE"** button
2. Wait 30-60 seconds for it to activate

### Step 3: Enable Google Drive API (Also Needed)
```
https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=341497862364
```

1. Click **"ENABLE"**
2. Wait for activation

### Step 4: Test Again
After enabling both APIs (wait 1-2 minutes), run:
```bash
curl http://localhost:5000/test/vapi-webhook
```

## What Gets Enabled

You need these 2 APIs:
- ✓ **Google Docs API** - Create and edit documents
- ✓ **Google Drive API** - Store and share documents

## Troubleshooting

**"API not enabled" error?**
- Make sure you enabled BOTH APIs
- Wait 2-3 minutes after enabling
- Refresh your credentials

**"Permission denied"?**
- Check service account has correct permissions
- Make sure credentials file is valid

**Still not working?**
- Verify you're in the correct project (341497862364)
- Check service account email has access to Google Drive
- Try creating a document manually in Google Docs first

## After Enabling

Once both APIs are enabled, your flow will work:
1. ✓ Receive VAPI webhook
2. ✓ Generate SOP with GPT-4
3. ✓ Create Google Doc ← (will work now!)
4. ✓ Send via GoHighLevel
5. ✓ Notify Lindy with document URL

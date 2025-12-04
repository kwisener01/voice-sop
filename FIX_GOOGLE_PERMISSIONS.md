# Fix Google Service Account Permissions

## The Issue
Your service account doesn't have permission to create Google Docs.

## Solution

### Option 1: Enable Domain-Wide Delegation (Recommended)

1. **Go to Google Cloud Console**:
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts?project=341497862364
   ```

2. **Find your service account**:
   - Email: `341497862364-compute@developer.gserviceaccount.com`
   - Click on it

3. **Enable Domain-Wide Delegation**:
   - Click "EDIT"
   - Check "Enable G Suite Domain-wide Delegation"
   - Save

4. **Grant Scopes** (if using G Suite):
   - Go to: https://admin.google.com (need admin access)
   - Security > API Controls > Domain-wide Delegation
   - Add client ID: `113149859732532192757`
   - Add scopes:
     ```
     https://www.googleapis.com/auth/documents
     https://www.googleapis.com/auth/drive
     ```

### Option 2: Share Drive Folder (Easier!)

This is the simplest fix if you don't have admin access:

1. **Create a folder in Google Drive**:
   - Go to: https://drive.google.com
   - Create a new folder (e.g., "SOPs Generated")
   - Right-click → Share

2. **Share with your service account**:
   - Add this email: `341497862364-compute@developer.gserviceaccount.com`
   - Give it "Editor" permissions
   - Click "Share"

3. **Get the folder ID**:
   - Open the folder in Google Drive
   - Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Copy the folder ID

4. **Update your .env file**:
   ```env
   GOOGLE_FOLDER_ID=paste_your_folder_id_here
   ```

5. **Restart the server**

### Option 3: Use a Different Service Account

Create a new service account with correct permissions:

1. **Go to Google Cloud Console**:
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts?project=341497862364
   ```

2. **Create Service Account**:
   - Click "+ CREATE SERVICE ACCOUNT"
   - Name: "Voice SOP Generator"
   - Click "CREATE AND CONTINUE"

3. **Grant Roles**:
   - Add role: "Service Account User"
   - Click "CONTINUE"

4. **Create Key**:
   - Click on the new service account
   - Go to "KEYS" tab
   - "ADD KEY" → "Create new key" → JSON
   - Download the JSON file

5. **Replace credentials**:
   ```bash
   # Save the new JSON to:
   C:\Projects\voice_sop\credentials\google_credentials.json
   ```

6. **Share a Drive folder** with the new service account email
   - Give it "Editor" permissions

7. **Restart server**

## Quick Test: Option 2 (Recommended)

This is the fastest fix:

1. Create folder in Google Drive: https://drive.google.com
2. Share folder with: `341497862364-compute@developer.gserviceaccount.com` (Editor access)
3. Copy folder ID from URL
4. Update `.env`:
   ```env
   GOOGLE_FOLDER_ID=your_folder_id_here
   ```
5. Restart server
6. Test again!

## Verify Permissions

After fixing, test with:
```bash
curl http://localhost:5000/test/vapi-webhook
```

You should see:
- ✅ "SOP generated"
- ✅ "Google Doc created"
- ✅ Document URL returned

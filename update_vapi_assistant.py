#!/usr/bin/env python
"""
Update VAPI assistant to send webhooks to our Flask app
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.vapi_service import VAPIService
from config import Config
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize VAPI service
vapi_service = VAPIService(Config.VAPI_API_KEY)

# Your assistant ID
ASSISTANT_ID = '678bd43a-a18c-49dc-b7a5-ab3ba48048ef'

# Your webhook URL (ngrok for now, Railway later)
WEBHOOK_URL = 'https://nonsuppressive-overplentifully-alberto.ngrok-free.dev/webhook/vapi'

print(f"\n{'='*60}")
print("VAPI Assistant Configuration Update")
print(f"{'='*60}\n")

# Step 1: Get current assistant configuration
print(f"1. Fetching current configuration for assistant: {ASSISTANT_ID}")
try:
    current_config = vapi_service.get_assistant(ASSISTANT_ID)
    print(f"\n   Current Assistant Name: {current_config.get('name')}")
    print(f"   Current Server URL: {current_config.get('serverUrl', 'NOT SET')}")
    print(f"\n   Current Configuration:")
    print(f"   {json.dumps(current_config, indent=2)}\n")
except Exception as e:
    print(f"   ERROR: {str(e)}")
    sys.exit(1)

# Step 2: Prepare update with webhook URL
print(f"2. Preparing update to set webhook URL: {WEBHOOK_URL}")

update_config = {
    'serverUrl': WEBHOOK_URL,
    'serverUrlSecret': None  # Optional: add a secret if you want
}

# Ask user if they want to update the system prompt too
print("\n3. Do you want to update the system prompt for SOP generation?")
print("   Current system prompt focuses on: ", end="")
if current_config.get('model', {}).get('messages'):
    current_prompt = current_config['model']['messages'][0].get('content', 'Not set')
    print(f"{current_prompt[:100]}..." if len(current_prompt) > 100 else current_prompt)
else:
    print("Not set")

response = input("\n   Update prompt? (y/n): ").lower()

if response == 'y':
    sop_prompt = """You are a professional SOP (Standard Operating Procedure) creation assistant.

Your role is to have a natural, conversational interview with the user to gather all necessary information to create a comprehensive SOP document.

IMPORTANT: Your ONLY job is to gather information through conversation. DO NOT write to Google Sheets or create any documents yourself. Just have a thorough conversation.

Ask questions about:
1. Process name and purpose - What is this SOP for?
2. Step-by-step procedures - Walk me through each step
3. Required tools, materials, or software - What do you need?
4. Safety considerations or prerequisites - Any warnings or requirements?
5. Expected outcomes and quality standards - What does success look like?
6. Common issues and troubleshooting - What typically goes wrong?
7. Responsible parties and escalation - Who does what?

Be thorough but conversational. Ask follow-up questions. Confirm understanding.

At the end of the conversation, summarize what you've learned to ensure accuracy, then thank them.

The system will automatically send the transcript to create the SOP document - you don't need to do anything else."""

    update_config['model'] = current_config.get('model', {})
    update_config['model']['messages'] = [{
        'role': 'system',
        'content': sop_prompt
    }]
    print("   ✓ System prompt will be updated")

# Step 3: Update the assistant
print(f"\n4. Updating assistant configuration...")
print(f"   Setting serverUrl to: {WEBHOOK_URL}")

try:
    updated_assistant = vapi_service.update_assistant(ASSISTANT_ID, update_config)
    print(f"   ✓ Assistant updated successfully!")
    print(f"\n   New Configuration:")
    print(f"   Server URL: {updated_assistant.get('serverUrl')}")
    if 'model' in update_config:
        print(f"   System Prompt: Updated ✓")
except Exception as e:
    print(f"   ERROR: {str(e)}")
    sys.exit(1)

print(f"\n{'='*60}")
print("✓ VAPI Assistant Successfully Configured!")
print(f"{'='*60}\n")
print("Next steps:")
print("1. Make a test call to your VAPI number")
print("2. Have a conversation about creating an SOP")
print("3. When the call ends, VAPI will send webhook to:")
print(f"   {WEBHOOK_URL}")
print("4. Check your Flask server logs to see the SOP being generated")
print("5. Check Lindy to see the SOP content being sent")
print(f"\n{'='*60}\n")

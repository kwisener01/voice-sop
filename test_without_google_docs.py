#!/usr/bin/env python
"""
Test the flow without Google Docs
This sends the SOP content directly to Lindy and GHL
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.sop_generator import SOPGenerator
from services.lindy_service import LindyService
from services.ghl_service import GHLService
from config import Config
from dotenv import load_dotenv

load_dotenv()

# Initialize services
sop_generator = SOPGenerator(Config.OPENAI_API_KEY)
ghl_service = GHLService(Config.GHL_API_KEY)

# Initialize Lindy if configured
lindy_service = None
if Config.LINDY_WEBHOOK_URL:
    lindy_service = LindyService(Config.LINDY_WEBHOOK_URL, Config.LINDY_WEBHOOK_SECRET)

# Test data
call_id = 'test_call_without_gdocs'
transcript = '''
Assistant: Hello! I'm here to help you create your Standard Operating Procedure. Let's get started! What process would you like to document today?

User: I need to create an SOP for onboarding new employees.
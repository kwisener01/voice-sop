from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from pythonjsonlogger import jsonlogger
from config import Config

# Import services
from services.vapi_service import VAPIService
from services.sop_generator import SOPGenerator
from services.google_docs_service import GoogleDocsService
from services.ghl_service import GHLService
from services.lindy_service import LindyService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Configure logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.INFO)

# Initialize services
vapi_service = VAPIService(app.config['VAPI_API_KEY'])
sop_generator = SOPGenerator(app.config['OPENAI_API_KEY'])
google_docs_service = GoogleDocsService(
    app.config['GOOGLE_CREDENTIALS_PATH'],
    app.config['GOOGLE_FOLDER_ID']
)
ghl_service = GHLService(app.config['GHL_API_KEY'])

# Initialize Lindy service if webhook URL is configured
lindy_service = None
if app.config.get('LINDY_WEBHOOK_URL'):
    lindy_service = LindyService(
        app.config['LINDY_WEBHOOK_URL'],
        app.config.get('LINDY_WEBHOOK_SECRET')
    )
    app.logger.info('Lindy service initialized with webhook URL')


@app.route('/', methods=['GET'])
def index():
    """Serve admin panel"""
    return app.send_static_file('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'voice-sop'}), 200


@app.route('/test/vapi-webhook', methods=['GET', 'POST'])
def test_vapi_webhook():
    """
    Test endpoint to simulate VAPI webhook
    Use this to test your SOP generation flow without making a real call
    """
    # Sample VAPI webhook data
    test_data = {
        'call': {
            'id': 'test_call_123',
            'status': 'ended',
            'assistantId': '678bd43a-a18c-49dc-b7a5-ab3ba48048ef'
        },
        'transcript': '''
        Assistant: Hello! I'm here to help you create your Standard Operating Procedure. Let's get started! What process would you like to document today?

        User: I need to create an SOP for onboarding new employees.

        Assistant: Great! Let's start with the onboarding process. Can you walk me through the main steps involved in onboarding a new employee at your company?

        User: Sure. First, we send them a welcome email with all the necessary paperwork. Then we set up their computer and accounts before their first day. On day one, we do orientation and introduce them to the team. The first week includes training on our systems and processes.

        Assistant: Excellent! What tools or materials are needed for this process?

        User: We need access to our HR system, IT equipment like laptop and phone, office access badge, and our training materials. Also the employee handbook.

        Assistant: Perfect! Are there any important safety or compliance considerations?

        User: Yes, they need to complete harassment training, sign the NDA, and review our security policies within the first week.

        Assistant: Great! What does successful onboarding look like? How do you measure it?

        User: The new employee should be able to work independently on basic tasks by end of week one, and they should have completed all required paperwork and training modules.

        Assistant: Wonderful! Any common issues or troubleshooting tips?

        User: Sometimes IT setup gets delayed, so we try to do that a week in advance. Also, make sure the team knows they're starting so everyone can prepare.

        Assistant: Perfect! I have all the information I need to create your SOP. Thank you!
        ''',
        'customer': {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'contact_id': 'test_contact_123',
            'company': 'Test Company'
        }
    }

    try:
        # Process the test webhook
        result = process_voice_to_sop(
            test_data['call']['id'],
            test_data['transcript'],
            test_data['customer']
        )

        return jsonify({
            'success': True,
            'message': 'Test webhook processed successfully!',
            'result': result
        }), 200

    except Exception as e:
        app.logger.error(f'Error in test webhook: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Check server logs for details'
        }), 500


@app.route('/webhook/vapi', methods=['POST'])
def vapi_webhook():
    """
    Webhook endpoint for VAPI to send conversation data
    VAPI sends multiple webhook types - we only process end-of-call-report
    """
    try:
        data = request.json

        # Check if this is an end-of-call-report
        message_type = data.get('message', {}).get('type')

        if message_type != 'end-of-call-report':
            # Ignore other webhook types (status-update, speech-update, etc.)
            app.logger.info(f'Ignoring VAPI webhook type: {message_type}')
            return jsonify({'status': 'ignored', 'type': message_type}), 200

        app.logger.info('Received VAPI end-of-call-report', extra={'data': data})

        # Extract conversation details from end-of-call-report
        call = data.get('message', {}).get('call', {})
        call_id = call.get('id')
        transcript = data.get('message', {}).get('transcript', '')
        customer = call.get('customer', {})

        # Build customer info
        customer_info = {
            'name': customer.get('name', ''),
            'email': customer.get('email', ''),
            'phone': customer.get('number', ''),
            'contact_id': customer.get('id', '')
        }

        # Validate webhook
        if not transcript:
            return jsonify({'error': 'No transcript in end-of-call-report'}), 400

        # Process the conversation and generate SOP
        result = process_voice_to_sop(call_id, transcript, customer_info)

        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f'Error processing VAPI webhook: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/webhook/lindy', methods=['POST'])
def lindy_webhook():
    """
    Webhook endpoint for Lindy automation
    This can be used for additional automation triggers
    """
    try:
        # Verify webhook secret (optional - Lindy can use URL-based auth)
        secret = request.headers.get('X-Webhook-Secret')
        if secret and secret != app.config['LINDY_WEBHOOK_SECRET']:
            return jsonify({'error': 'Invalid webhook secret'}), 401

        data = request.json
        app.logger.info('Received Lindy webhook', extra={'data': data})

        # Process based on action type
        action = data.get('action')

        if action == 'create_assistant':
            result = create_vapi_assistant(data)
        elif action == 'generate_sop':
            result = generate_sop_manual(data)
        else:
            return jsonify({'error': f'Unknown action: {action}'}), 400

        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f'Error processing Make.com webhook: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/assistant/create', methods=['POST'])
def create_assistant():
    """Create a new VAPI assistant"""
    try:
        data = request.json

        # Create assistant configuration
        assistant_config = {
            'name': data.get('name', 'SOP Voice Assistant'),
            'model': {
                'provider': 'openai',
                'model': data.get('model', 'gpt-4'),
                'messages': [{
                    'role': 'system',
                    'content': data.get('system_prompt', get_default_sop_prompt())
                }]
            },
            'voice': {
                'provider': data.get('voice_provider', '11labs'),
                'voiceId': data.get('voice_id')
            },
            'firstMessage': data.get('first_message', 'Hello! I\'m here to help you create your Standard Operating Procedure. Let\'s get started!'),
            'serverUrl': data.get('webhook_url', request.url_root + 'webhook/vapi')
        }

        # Create assistant via VAPI
        assistant = vapi_service.create_assistant(assistant_config)

        app.logger.info('Created VAPI assistant', extra={'assistant_id': assistant.get('id')})

        return jsonify(assistant), 201

    except Exception as e:
        app.logger.error(f'Error creating assistant: {str(e)}')
        return jsonify({'error': str(e)}), 500


def process_voice_to_sop(call_id, transcript, customer_info):
    """
    Main processing function: Voice → SOP → Lindy (creates Google Doc) → GHL
    This orchestrates the entire flow
    """
    app.logger.info(f'Processing voice to SOP for call {call_id}')

    try:
        # Notify Lindy that processing has started
        if lindy_service:
            lindy_service.notify_sop_started(call_id, customer_info)

        # Step 1: Generate SOP from transcript using GPT-4
        app.logger.info('Generating SOP from transcript')
        sop_content = sop_generator.generate_sop(transcript, customer_info)

        # Step 2: Send SOP content to Lindy (Lindy will create Google Doc)
        document_title = f"SOP - {customer_info.get('name', 'Customer')} - {call_id}"
        lindy_result = None

        if lindy_service:
            app.logger.info('Sending SOP to Lindy for Google Doc creation')
            lindy_result = lindy_service.notify_sop_completed(
                call_id,
                None,  # No document URL yet - Lindy will create it
                document_title,
                customer_info,
                sop_content  # Full SOP content for Lindy to create doc
            )

        # Step 3: Optionally send notification to GHL (Lindy will handle document delivery)
        ghl_result = None
        if customer_info.get('contact_id'):
            try:
                app.logger.info('Notifying GHL')
                # Just add a note that SOP is being generated
                ghl_result = ghl_service.add_note(
                    customer_info.get('contact_id'),
                    f"SOP '{document_title}' has been generated and is being processed by automation."
                )
            except Exception as e:
                app.logger.warning(f'GHL notification failed: {str(e)}')

        return {
            'success': True,
            'call_id': call_id,
            'sop_generated': True,
            'sop_length': len(sop_content),
            'document_title': document_title,
            'lindy_notified': lindy_result.get('success') if lindy_result else False,
            'message': 'SOP sent to Lindy for Google Doc creation'
        }

    except Exception as e:
        app.logger.error(f'Error in voice to SOP processing: {str(e)}')

        # Notify Lindy about the error
        if lindy_service:
            lindy_service.notify_error(call_id, str(e), customer_info)

        raise


def create_vapi_assistant(data):
    """Helper to create VAPI assistant from Lindy"""
    assistant_config = {
        'name': data.get('name'),
        'model': data.get('model_config'),
        'voice': data.get('voice_config'),
        'firstMessage': data.get('first_message'),
        'serverUrl': data.get('webhook_url')
    }
    return vapi_service.create_assistant(assistant_config)


def generate_sop_manual(data):
    """Manual SOP generation trigger"""
    transcript = data.get('transcript')
    customer_info = data.get('customer_info', {})

    sop_content = sop_generator.generate_sop(transcript, customer_info)

    return {
        'success': True,
        'sop_content': sop_content
    }


def get_default_sop_prompt():
    """Default system prompt for SOP generation assistant"""
    return """You are a professional SOP (Standard Operating Procedure) creation assistant.
Your role is to have a natural conversation with the user to gather all necessary information
to create a comprehensive, detailed SOP document.

Ask questions about:
1. The process name and purpose
2. Step-by-step procedures
3. Required tools, materials, or software
4. Safety considerations or prerequisites
5. Expected outcomes and quality standards
6. Common issues and troubleshooting steps
7. Responsible parties and escalation procedures

Be thorough but conversational. Confirm understanding and ask clarifying questions.
At the end, summarize what you've learned to ensure accuracy."""


if __name__ == '__main__':
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        app.logger.error(f'Configuration error: {str(e)}')
        exit(1)

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

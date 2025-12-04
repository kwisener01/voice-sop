# Voice SOP Generator

Automated Standard Operating Procedure (SOP) generation system powered by voice conversations.

## System Flow

```
GHL (Customer Flow)
  ↓
VAPI (Voice Engine)
  ↓
Lindy (AI Automation)
  ↓
GPT-4 via OpenAI API (SOP Generator)
  ↓
Google Docs (Document Creation)
  ↓
Back to GHL (Delivery)
```

## Features

- **Voice-Driven SOP Creation**: Customers call in and describe their processes
- **AI-Powered Generation**: GPT-4 converts conversations into professional SOPs
- **Automatic Documentation**: Creates formatted Google Docs automatically
- **CRM Integration**: Delivers documents back through GoHighLevel
- **Scalable Architecture**: Built with Flask, PostgreSQL, Redis, and Celery
- **Lindy Integration**: AI-powered automation workflow

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- API Keys:
  - VAPI API key
  - OpenAI API key
  - GoHighLevel API key
  - Google Cloud service account credentials

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd voice_sop
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate     # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Set up Google Cloud credentials:**
   ```bash
   mkdir credentials
   # Place your google_credentials.json in the credentials folder
   ```

6. **Initialize database:**
   ```bash
   python setup.py
   ```

### Running with Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Running Locally

```bash
# Start Flask app
python app.py

# In another terminal, start Celery worker
celery -A celery_tasks worker --loglevel=info

# Optional: Start Celery beat for periodic tasks
celery -A celery_tasks beat --loglevel=info
```

## API Endpoints

### Health Check
```
GET /health
```

### Create VAPI Assistant
```
POST /api/assistant/create
Content-Type: application/json

{
  "name": "SOP Voice Assistant",
  "model": "gpt-4",
  "voice_provider": "11labs",
  "voice_id": "your_voice_id",
  "system_prompt": "Your custom prompt",
  "first_message": "Hello! Let's create your SOP."
}
```

### VAPI Webhook (Receives call data)
```
POST /webhook/vapi
Content-Type: application/json

{
  "call": {
    "id": "call_123"
  },
  "transcript": "Full conversation transcript...",
  "customer": {
    "name": "John Doe",
    "contact_id": "ghl_contact_123"
  }
}
```

### Lindy Webhook
```
POST /webhook/lindy
X-Webhook-Secret: your_secret (optional)
Content-Type: application/json

{
  "action": "create_assistant",
  "name": "Custom Assistant",
  ...
}
```

## Configuration

All configuration is managed through environment variables in `.env`:

### Required Variables
- `VAPI_API_KEY` - Your VAPI API key
- `OPENAI_API_KEY` - Your OpenAI API key
- `GHL_API_KEY` - Your GoHighLevel API key
- `GOOGLE_CREDENTIALS_PATH` - Path to Google service account JSON
- `LINDY_WEBHOOK_SECRET` - Optional secret for Lindy webhook verification
- `LINDY_WEBHOOK_URL` - Your Lindy webhook URL for callbacks

### Optional Variables
- `GOOGLE_FOLDER_ID` - Google Drive folder ID for storing docs
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `PORT` - Server port (default: 5000)

## Architecture

### Services

1. **VAPI Service** (`services/vapi_service.py`)
   - Manages voice assistant creation and configuration
   - Handles VAPI API interactions

2. **SOP Generator** (`services/sop_generator.py`)
   - Uses GPT-4 to generate SOPs from transcripts
   - Supports refinement and structured generation

3. **Google Docs Service** (`services/google_docs_service.py`)
   - Creates and manages Google Documents
   - Handles permissions and sharing

4. **GHL Service** (`services/ghl_service.py`)
   - Sends documents via SMS and email
   - Creates tasks and adds notes to contacts
   - Integrates with GoHighLevel CRM

### Database Models

- **Conversation** - Tracks VAPI call conversations
- **SOPDocument** - Tracks generated documents
- **VAPIAssistant** - Tracks configured assistants
- **WebhookLog** - Logs all webhook calls for debugging

### Async Tasks

Celery tasks for background processing:
- `process_transcript_async` - Generate SOP without blocking webhook
- `send_reminder_async` - Send follow-up reminders
- `cleanup_old_logs` - Clean up old webhook logs

## Workflow

1. **Customer calls** via GoHighLevel phone number
2. **VAPI handles** the voice conversation using configured assistant
3. **Transcript is sent** to webhook after call completes
4. **SOP is generated** using GPT-4 based on conversation
5. **Google Doc is created** with formatted SOP content
6. **Document is delivered** to customer via GHL (SMS + Email)
7. **Follow-up task** created in GHL for team review

## Lindy Integration

Set up automation workflows in Lindy:

1. **Trigger**: GHL contact created or call initiated
2. **Action**: Create or select VAPI assistant
3. **Action**: VAPI conducts voice conversation
4. **Trigger**: Your webhook receives VAPI transcript
5. **Action**: GPT-4 generates SOP document
6. **Action**: Create Google Doc
7. **Action**: Deliver to customer via GHL (SMS + Email)

### Setting up Lindy Workflow

1. In Lindy, create a new workflow
2. Set trigger: Incoming webhook or GHL event
3. Add action: Call your `/webhook/lindy` endpoint
4. Configure data mapping for customer info and transcript
5. Optional: Add Lindy webhook URL to `.env` as `LINDY_WEBHOOK_URL`

## Development

### Project Structure
```
voice_sop/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── models.py              # Database models
├── utils.py               # Utility functions
├── celery_tasks.py        # Background tasks
├── requirements.txt       # Python dependencies
├── services/
│   ├── vapi_service.py    # VAPI integration
│   ├── sop_generator.py   # GPT-4 SOP generation
│   ├── google_docs_service.py  # Google Docs
│   └── ghl_service.py     # GoHighLevel integration
├── credentials/           # Google credentials (gitignored)
├── Dockerfile            # Container definition
└── docker-compose.yml    # Multi-container setup
```

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=services
```

### Logging

All services include structured logging:
- API requests/responses
- SOP generation steps
- Document creation
- Webhook calls

Logs are output in JSON format for easy parsing.

## Deployment

### Production Checklist

- [ ] Set all environment variables in `.env`
- [ ] Configure Google Cloud credentials
- [ ] Set up PostgreSQL database
- [ ] Set up Redis instance
- [ ] Configure VAPI webhooks to point to your server
- [ ] Set up Make.com scenarios
- [ ] Enable SSL/TLS (recommended: use nginx reverse proxy)
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy for database

### Scaling

For high volume:
- Increase Celery workers: `docker-compose up --scale celery=4`
- Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Use managed Redis (AWS ElastiCache, Google Memorystore)
- Deploy multiple app instances behind load balancer

## Troubleshooting

### Common Issues

1. **VAPI webhook not receiving data**
   - Check webhook URL is publicly accessible
   - Verify VAPI assistant configuration includes correct `serverUrl`

2. **Google Docs creation fails**
   - Verify service account credentials are correct
   - Ensure Google Docs API is enabled in Google Cloud Console
   - Check service account has necessary permissions

3. **SOP generation slow**
   - Use async processing (Celery tasks)
   - Consider using gpt-4-turbo for faster responses

4. **Database connection errors**
   - Verify DATABASE_URL is correct
   - Ensure PostgreSQL is running
   - Check network connectivity

## Support

For issues and questions:
- Check webhook logs in database
- Review application logs
- Verify API credentials and quotas

## License

MIT License - See LICENSE file for details

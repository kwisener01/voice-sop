from celery import Celery
from config import Config
import logging

# Initialize Celery
celery_app = Celery(
    'voice_sop',
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

logger = logging.getLogger(__name__)


@celery_app.task(name='tasks.process_transcript')
def process_transcript_async(call_id, transcript, customer_info):
    """
    Async task to process transcript and generate SOP
    This allows long-running SOP generation without blocking the webhook response
    """
    try:
        logger.info(f'Processing transcript async for call: {call_id}')

        # Import here to avoid circular imports
        from services.sop_generator import SOPGenerator
        from services.google_docs_service import GoogleDocsService
        from services.ghl_service import GHLService
        from models import Database, save_conversation, save_sop_document

        # Initialize services
        sop_generator = SOPGenerator(Config.OPENAI_API_KEY)
        google_docs_service = GoogleDocsService(
            Config.GOOGLE_CREDENTIALS_PATH,
            Config.GOOGLE_FOLDER_ID
        )
        ghl_service = GHLService(Config.GHL_API_KEY)

        # Save conversation to database
        db = Database(Config.DATABASE_URL)
        session = db.get_session()

        try:
            save_conversation(session, call_id, transcript, customer_info)

            # Generate SOP
            sop_content = sop_generator.generate_sop(transcript, customer_info)

            # Create Google Doc
            doc_info = google_docs_service.create_document(
                title=f"SOP - {customer_info.get('name', 'Customer')} - {call_id}",
                content=sop_content
            )

            # Save document
            save_sop_document(
                session,
                doc_info['id'],
                doc_info['url'],
                doc_info['title'],
                sop_content,
                call_id,
                customer_info.get('contact_id')
            )

            # Send to GHL
            ghl_result = ghl_service.send_document(
                customer_info.get('contact_id'),
                doc_info['url'],
                doc_info['title']
            )

            logger.info(f'Successfully processed transcript for call: {call_id}')

            return {
                'success': True,
                'call_id': call_id,
                'document_url': doc_info['url']
            }

        finally:
            session.close()

    except Exception as e:
        logger.error(f'Error processing transcript async: {str(e)}')
        raise


@celery_app.task(name='tasks.send_reminder')
def send_reminder_async(contact_id, document_url, document_title):
    """
    Send reminder about SOP document
    Can be scheduled to run after X days
    """
    try:
        from services.ghl_service import GHLService

        ghl_service = GHLService(Config.GHL_API_KEY)

        ghl_service._send_sms(
            contact_id,
            f"Reminder: Your SOP document '{document_title}' is available at: {document_url}"
        )

        logger.info(f'Sent reminder to contact: {contact_id}')
        return {'success': True}

    except Exception as e:
        logger.error(f'Error sending reminder: {str(e)}')
        raise


@celery_app.task(name='tasks.cleanup_old_logs')
def cleanup_old_logs():
    """
    Periodic task to cleanup old webhook logs
    Run this daily or weekly
    """
    try:
        from models import Database, WebhookLog
        from datetime import datetime, timedelta

        db = Database(Config.DATABASE_URL)
        session = db.get_session()

        try:
            # Delete logs older than 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            deleted = session.query(WebhookLog).filter(
                WebhookLog.created_at < cutoff_date
            ).delete()

            session.commit()

            logger.info(f'Cleaned up {deleted} old webhook logs')
            return {'success': True, 'deleted': deleted}

        finally:
            session.close()

    except Exception as e:
        logger.error(f'Error cleaning up logs: {str(e)}')
        raise


# Periodic task schedule
celery_app.conf.beat_schedule = {
    'cleanup-logs-daily': {
        'task': 'tasks.cleanup_old_logs',
        'schedule': 86400.0,  # Run every 24 hours
    },
}

from sqlalchemy import create_engine, Column, String, DateTime, Text, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class Conversation(Base):
    """Track VAPI conversations"""
    __tablename__ = 'conversations'

    id = Column(String(100), primary_key=True)
    call_id = Column(String(100), unique=True, nullable=False)
    contact_id = Column(String(100))
    assistant_id = Column(String(100))
    transcript = Column(Text)
    customer_info = Column(JSON)
    status = Column(String(50), default='processing')  # processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SOPDocument(Base):
    """Track generated SOP documents"""
    __tablename__ = 'sop_documents'

    id = Column(String(100), primary_key=True)
    conversation_id = Column(String(100))
    google_doc_id = Column(String(100))
    google_doc_url = Column(String(500))
    title = Column(String(500))
    content = Column(Text)
    contact_id = Column(String(100))
    status = Column(String(50), default='created')  # created, sent, viewed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VAPIAssistant(Base):
    """Track VAPI assistants"""
    __tablename__ = 'vapi_assistants'

    id = Column(String(100), primary_key=True)
    vapi_id = Column(String(100), unique=True)
    name = Column(String(200))
    configuration = Column(JSON)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WebhookLog(Base):
    """Log all webhook calls for debugging"""
    __tablename__ = 'webhook_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50))  # vapi, make, etc.
    endpoint = Column(String(200))
    payload = Column(JSON)
    response_status = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Database:
    """Database manager"""

    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info('Database initialized')

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info('Database tables created')

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)
        logger.warning('All database tables dropped')


# Utility functions for common database operations

def save_conversation(session, call_id, transcript, customer_info, assistant_id=None):
    """Save conversation to database"""
    try:
        conversation = Conversation(
            id=call_id,
            call_id=call_id,
            transcript=transcript,
            customer_info=customer_info,
            assistant_id=assistant_id,
            status='processing'
        )
        session.add(conversation)
        session.commit()
        logger.info(f'Conversation saved: {call_id}')
        return conversation

    except Exception as e:
        session.rollback()
        logger.error(f'Failed to save conversation: {str(e)}')
        raise


def save_sop_document(session, doc_id, doc_url, title, content, conversation_id=None, contact_id=None):
    """Save SOP document to database"""
    try:
        document = SOPDocument(
            id=doc_id,
            google_doc_id=doc_id,
            google_doc_url=doc_url,
            title=title,
            content=content,
            conversation_id=conversation_id,
            contact_id=contact_id,
            status='created'
        )
        session.add(document)
        session.commit()
        logger.info(f'SOP document saved: {doc_id}')
        return document

    except Exception as e:
        session.rollback()
        logger.error(f'Failed to save SOP document: {str(e)}')
        raise


def log_webhook(session, source, endpoint, payload, status, error=None):
    """Log webhook call"""
    try:
        log = WebhookLog(
            source=source,
            endpoint=endpoint,
            payload=payload,
            response_status=status,
            error_message=error
        )
        session.add(log)
        session.commit()

    except Exception as e:
        logger.error(f'Failed to log webhook: {str(e)}')

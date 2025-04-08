from .celery_config import celery_app
from celery import shared_task
import time
from functools import wraps
from prometheus_client import Counter, Histogram

# Metrics setup
TASK_COUNTER = Counter('task_count', 'Number of tasks executed', ['task_name'])
TASK_LATENCY = Histogram('task_latency_seconds', 'Task processing latency', ['task_name'])

def track_metrics(task_name):
    """Decorator to track task metrics"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            TASK_COUNTER.labels(task_name).inc()
            try:
                result = f(*args, **kwargs)
                TASK_LATENCY.labels(task_name).observe(time.time() - start_time)
                return result
            except Exception as e:
                TASK_COUNTER.labels(f"{task_name}_failed").inc()
                raise e
        return wrapper
    return decorator

@shared_task(bind=True)
@track_metrics('summarize_text')
def summarize_text_task(self, text):
    """Background task for text summarization"""
    from summarizer import summarize  # Import locally to avoid circular imports
    return summarize(text)

@shared_task(bind=True)
@track_metrics('generate_pdf')
def generate_pdf_task(self, content):
    """Background task for PDF generation"""
    from pdf_generator import generate_pdf  # Import locally to avoid circular imports
    return generate_pdf(content)

@shared_task(bind=True)
@track_metrics('transcribe_audio')
def transcribe_audio_task(self, audio_path):
    """Background task for audio transcription"""
    from transcriber import transcribe  # Import locally to avoid circular imports
    return transcribe(audio_path)

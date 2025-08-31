# Weekly CRM Report

## Setup

1. Install Redis and project dependencies:
   pip install -r requirements.txt

2. Run Django migrations:
   python manage.py migrate

3. Start Celery worker:
   celery -A crm worker -l info

4. Start Celery Beat:
   celery -A crm beat -l info

5. Verify weekly report logs in:
   /tmp/crm_report_log.txt

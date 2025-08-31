#!/bin/bash

# Navigate to project root (adjust path if needed)
cd "$(dirname "$0")/../.."

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(
    orders__order_date__lt=one_year_ago
).distinct()

count = qs.count()
qs.delete()
print(count)
")

# Log results with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt

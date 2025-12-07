import os
from django.core.wsgi import get_wsgi_application

# CORRECTED: Changed 'e_commerce' to 'ecommerce_proj'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_proj.settings')

application = get_wsgi_application()
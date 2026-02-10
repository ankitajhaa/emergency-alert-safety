from django.contrib import admin
from alerts.models import Alert, Acknowledgement

# Register your models here.
admin.site.register(Alert)
admin.site.register(Acknowledgement)
from django.contrib import admin
from .models import Department, Doctor_details, doctors_image, appointment

# Register your models here.
admin.site.register(Department)

admin.site.register(Doctor_details)

admin.site.register(doctors_image)

admin.site.register(appointment)

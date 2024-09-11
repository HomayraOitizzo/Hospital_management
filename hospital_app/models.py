from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class Hospital(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class Department(Hospital):
    dep_name = models.CharField(max_length=50)
   

    def __str__(self) -> str:
        return self.dep_name
   
       
class Doctor_details(Hospital):
    doctors_name = models.CharField(max_length=50)
    doctors_visit = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.Doctor_details
  


class doctors_image(Hospital):
    doctor = models.ForeignKey(Doctor_details, related_name='images', on_delete= models.CASCADE)
    images = models.ImageField()


class appointment(Hospital):
    doctor = models.ForeignKey(Doctor_details, related_name='doctor_booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_booking', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(auto_now_add=True)
    appoinment_type = models.CharField(max_length=50, choices=(('pre paid','pre paid'), ('post paid', 'post paid')))

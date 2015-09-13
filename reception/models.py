from django.db import models
from django.utils import timezone

# Model of Patient
class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    reg_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.patronymic)

# Model of Doctor
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return Doctor.objects.all().order_by('name')

# Model of reception record
class Record(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    accept_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.finish_time = self.accept_time + timezone.timedelta(hours=1)
        super(Record, self).save(*args, **kwargs)  # Call the save()

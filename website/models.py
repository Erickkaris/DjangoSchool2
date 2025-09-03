from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=30)
    course = models.CharField(max_length=30)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    def __str__(self):
        return self.name

class Payment(models.Model):
    phone = models.CharField(max_length=10)
    amount = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    response_code = models.CharField(max_length=20, blank=True, null=True)
    customer_message_id = models.CharField(max_length=200, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.phone} - {self.amount} - {self.status}'
from django.db import models

from django.contrib.auth.models import AbstractUser 
# Import AbstractUser for custom user model

from django.utils import timezone 
# Import Timezone for date fields
from django.conf import settings 
# Import settings to access AUTH_USER_MODEL

class User(AbstractUser): # username, email, passowrd, first_name, last_name are inherited from AbstractUser
    #custom user model extending AbstractUser
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField() #e.g., 1, 3, 6, 9, 12, months
    fee = models.DecimalField(max_digits=6, decimal_places=2) #e.g., 500, 1000 php
    description = models.TextField(blank=True)

    def __str__(self):        
        return f"{self.name} - {self.duration_months} months - ${self.fee}"
    
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    # mobile = models.BigIntegerField()
    specialization = models.CharField(max_length=200)
    shift_timings = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

# 11 fields
class MemberProfile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, #Delete profile if user is deleted
        related_name='member_profile' # Acces profile via user.member
        )
    
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    age = models.PositiveBigIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(default=timezone.now)
    plan = models.ForeignKey(
        MembershipPlan, 
            on_delete=models.SET_NULL, # if plan is deleted, set to null
              null=True, blank=True,
              related_name='members' # access via plan.members
              )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL, # if trainer is deleted, set to null
        null=True, blank=True,
        related_name='members' # Access members via trainer.members
    )
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank =True)
    
    def __str__(self):
        return f"{self.full_name} - {self.user.username}"
    
# 5 fields
class Equipment(models.Model):
    name = models.CharField(max_length=100) #e.g., dumbbells
    units = models.PositiveIntegerField(default=1) #e.g., 10 dumbells
    price = models.DecimalField(max_digits=8, decimal_places=2) #e.g., 1500.00
    purchase_date = models.DateField(default=timezone.now) # date of equipment purchase
    is_active = models.BooleanField(default=True) # if removed/sold or inactive   

def __str__(self):
    return f"{self.name} (Units: {self.units})"

# 7 fields
class Payment(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),

    )
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE, # if member is deleted, delete payments
        related_name='payments' # Access payments via member.payments
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.SET_NULL, # if plan is deleted, delete payments
        null=True, blank=True,
        related_name='payments' # Access payments via plan.payments
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2) # eg., 4500.00
    payment_date = models.DateField(default=timezone.now) # e.g., payment date
    mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES) #e.g., cash or credit
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)
    notes = models.TextField(blank=True) # optional field for additional notes
    
    def __str__(self):
        return f"Payment of ${self.amount} by {self.member.full_name} on {self.payment_date}"
    
# 3 fields
class Attendance(models.Model):
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE, 
        related_name='attendances'
        )
    date = models.DateField(default=timezone.now) #date attendance
    time_in = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('member', 'date') # ENSURE one attendance record only

    def __str__(self):
        return f"{self.member.full_name} - {self.date} - {self.time_in}"


# 6 fields
class Enquiry(models.Model):
    ENQUIRY_STATUS_CHOICE = (
        ('NEW', 'New'),
        ('SEEN', 'Seen'),
        ('RESOLVED', 'Resolved'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ENQUIRY_STATUS_CHOICE, default ='NEW')

    def __str__(self):
        return f"Enquiry from {self.name} - {self.email} - Status: {self.status}"
    
#5 fields
class WorkoutPlan(models.Model):
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
        related_name='workout_plans'
    )
    title = models.CharField(max_length=100) #title workoutplan
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title} - Created at: {self.created_at}"


class Feedback(models.Model):
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.member.full_name} - Created at: {self.created_at}"
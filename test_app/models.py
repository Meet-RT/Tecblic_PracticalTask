from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Custom_User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('solution_provider', 'Solution_Provider'),
        ('solution_seeker', 'Solution_Seeker'),
    )
    role = models.CharField(max_length=100, choices=ROLES)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    class Meta:
        ordering = ('pk',)

    @property
    def is_admin(self):
        return self.is_group_member('admin')

    @property
    def is_solution_provider_user(self):
        return self.is_group_member('solution_provider')

    @property
    def is_solution_seeker_user(self):
        return self.is_group_member('solution_seeker')
    
    def is_group_member(self, group_name):
        return self.groups.filter(name=group_name).exists()
    
PHONE_NUMBER_REGEX = RegexValidator(
    r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Invalid phone number, Please enter proper details')

class Personal_Profile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    user_bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True)
    mobile_number = models.TextField(max_length=20, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])

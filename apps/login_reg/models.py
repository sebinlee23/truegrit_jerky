from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form_data):
        errors = {}
        if len(form_data['fname']) == 0 or len(form_data['lname']) == 0 or len(form_data['email']) == 0 or len(form_data['password']) == 0:
            errors['no_value'] = 'All fields are required'
        if len(form_data['fname']) < 2 and len(form_data['fname']) != 0:
            errors['short_fname'] = 'First name should be at least 2 charactes long'
        if len(form_data['lname']) < 2 and len(form_data['lname']) != 0:
            errors['short_lname'] = 'Last name should be at least 2 charactes long'
        if form_data['password'] != form_data['confirm_password']:
            errors['match_pwd'] = "Your passwords don't match"
        return errors
    def login_validate(self, form_data):
        errors_2 = {}
        if len(self.filter(email = form_data['login_email'])) == 0:
            errors_2['no_exist'] = 'Login information invalid'
        if len(form_data['login_password']) == 0:
            errors_2['no_pw'] = 'Please enter your password'
        return errors_2


class Programs(models.Model):
    name = models.CharField(max_length = 255)

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    program = models.ForeignKey(Programs, related_name="subscriber", null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Flavors(models.Model):
    name = models.CharField(max_length = 255)
    favorite = models.ManyToManyField(User, related_name="prefer_flavor")
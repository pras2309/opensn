from django.db import models
from django.db import connection

# Create your models here.
from django.contrib.auth.models import User, UserManager

class CustomUser(models.Model):
    """User with app settings."""
    user_id = models.IntegerField()
    timezone = models.CharField(max_length=100, null=True)
    profile_image = models.ImageField(upload_to='userprofile')
    f_name = models.CharField(max_length=100, null=True)
    l_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.CharField(max_length=200)
    sex = models.CharField(max_length=200) 
    profile_image = models.ImageField(upload_to = 'profile_images/', default = 'pic_folder/None/no-img.jpg')


def userProfile(user_id):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM auth_user a LEFT JOIN customuser_customuser b ON a.id=b.user_id WHERE a.id = %s ", [user_id])
        return dictfetchall(cursor)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
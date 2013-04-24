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


    def __unicode__(self):
        return self.f_name

class Wall(models.Model):
    "User wall"
    user_id = models.IntegerField()
    wall_content = models.TextField()

    def wallContent(self, user_id):
        cursor = connection.cursor()
        sql = """
        SELECT * FROM customuser_wall a
        LEFT JOIN customuser_customuser b  ON a.user_id = b.user_id
        WHERE a.user_id = %s ORDER BY a.id DESC;
        """
        cursor.execute(sql, [user_id])
        return dictfetchall(cursor)

def userProfile(user_id):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM auth_user a LEFT JOIN customuser_customuser b ON a.id=b.user_id WHERE a.id = %s ", [user_id])
        return dictfetchall(cursor)

def searchQuery(q):
        q = '%' + q + '%'
        cursor = connection.cursor()
        sql = """SELECT * FROM auth_user a LEFT JOIN customuser_customuser b \
        ON a.id=b.user_id WHERE 1 AND b.f_name LIKE '%%%s%%' OR b.l_name LIKE '%%%s%%' """ %(q, q)
        cursor.execute(sql)
        result = dictfetchall(cursor)
        return result



def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
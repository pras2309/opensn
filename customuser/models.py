from django.db import models
from django.db import connection,transaction

class CustomUser(models.Model):
    """User with app settings."""
    user_id = models.IntegerField()
    timezone = models.CharField(max_length=100, null=True)
    profile_image = models.ImageField(upload_to='userprofile')
    enable_email = models.BooleanField(default=0)
    f_name = models.CharField(max_length=100, null=True)
    l_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.CharField(max_length=200)
    enable_dob = models.BooleanField(default=0)
    sex = models.CharField(max_length=200) 
    enable_sex = models.BooleanField(default=0)
    profile_image = models.ImageField(upload_to = 'profile_images/', default = 'pic_folder/None/no-img.jpg')

    def __unicode__(self):
        return self.f_name

class Wall(models.Model):
    "User wall"
    user_id = models.IntegerField()
    wall_content = models.TextField()
    date_time = models.DateTimeField()
    vote_up = models.IntegerField()
    vote_down = models.IntegerField()

    def __unicode__(self):
        return self.pk
    
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

def updateSettings(user_id, enable_email, enable_dob, enable_sex):
    sql = """UPDATE customuser_customuser 
        SET enable_email = '%s', 
        enable_dob = '%s', 
        enable_sex = '%s' 
        WHERE user_id='%s' """ 
    
    cursor = connection.cursor()
    cursor.execute(sql,  
            [enable_email, enable_dob, enable_sex, user_id])
    transaction.commit_unless_managed()

    row = cursor.fetchone()
    return row

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
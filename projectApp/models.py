from django.db import models

"""
This  model will contain Student information
"""
class Student(models.Model):
    class Meta:
        db_table = 'student'

    stud_id = models.IntegerField()
    fname = models.CharField(max_length=50, null=True)
    lname = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=10, null=True)
    age = models.IntegerField()

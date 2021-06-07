from django.db import models
from jsonfield import JSONField

class Search_history(models.Model):
    member_id = models.CharField(max_length=128)
    product_id = models.CharField(max_length=128)
    grade = models.IntegerField()
    def __str__(self):
        return self.member_id


class Member_info(models.Model):
    member_id = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    birth = models.CharField(max_length=128)
    def __str__(self):
        return self.member_id



class Product_info(models.Model):
    product_id = models.CharField(max_length=128)
    product_nm = models.CharField(max_length=128)
    img_dir = models.CharField(max_length=128)


from django.db import models
from jsonfield import JSONField

class Search_history(models.Model):
    seq = models.BigIntegerField(primary_key=True)
    member_id = models.CharField(max_length=128)
    search_hst = models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=128)
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
    product = models.CharField(max_length=128)
    img_dir = models.CharField(max_length=128)
    rank = models.BigIntegerField()

    def __str__(self):
        return self.member_id

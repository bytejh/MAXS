from django.db import models

class MenuGroup(models.Model):
    name = models.CharField(max_length=50)
    sta_type = models.CharField(max_length=1, default='0')  # '0': 정상, '9': 삭제
    update_date_time = models.DateTimeField(auto_now=True)

class Menu(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    group = models.ForeignKey(MenuGroup, on_delete=models.CASCADE)
    order = models.IntegerField()
    sta_type = models.CharField(max_length=1, default='0')  # '0': 정상, '9': 삭제
    update_date_time = models.DateTimeField(auto_now=True)


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=40) #제목
    username = models.ForeignKey(User,on_delete=models.CASCADE) #이메일
    price = models.TextField(max_length=20) #가격
    content = models.TextField() # 본문
    created_at = models.DateTimeField('작성일', default=timezone.now) #작성 시간
    photo = models.FileField(blank=True, upload_to="photo_%Y_%m_%d",null=True) #이미지

class Reply(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE) #이메일
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True) #댓글 단 사람의 id
    content = models.TextField() #본문
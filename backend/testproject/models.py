from django.db import models
from account.models import User
# Create your models here.
class TestData(models.Model):
    #순수 게시물 관련 데이터
    id= models.AutoField(primary_key=True, null=False, blank=False)
    image=models.ImageField(upload_to="images",null=True, blank=True)#이미지
    user= models.ForeignKey(User, 
        on_delete = models.CASCADE,
        related_name="testdata",
        verbose_name="테스트 데이터",
        null=True,
    )

    #알고리즘에 영향을 주는 요소
    views_cnt=models.PositiveIntegerField(null=True,blank=True,default=1)#조회수  
    exposure=models.PositiveIntegerField(null=True,blank=True,default=1)#총 노출수
    impressions_cnt=models.IntegerField(default=1)#노출되었지만 클릭 안된수. 현재 테스트 케이스의 문제로 음수 허용, 이후 수정 필요.
    text_length=models.PositiveIntegerField(null=True,blank=True,default=1)#글자 길이
    image_cnt=models.PositiveIntegerField(null=True,blank=True,default=1)#이미지 갯수

    #알고리즘에 영향을 주는 요소이며 개인적인 레코드가 기록되는 요소, 모델을 이후 따로 만들어야 할듯.
    residence_time=models.FloatField(null=True,blank=True,default=0)#사람들의 누적 체류시간(ms), 평균적인 체류시간은 조회수로 나누면 될 듯.
    like=models.PositiveIntegerField(null=True,blank=True,default=0)#좋아요

    importance=models.FloatField(null=True,blank=True,default=0)#중요도
    

class Comment(models.Model):
    created_date=models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE) #글 쓴 유저
    post = models.ForeignKey(TestData, null=True, blank=True, on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)# like 한 유저
    post = models.ForeignKey(TestData, null=True, blank=True, on_delete=models.CASCADE)
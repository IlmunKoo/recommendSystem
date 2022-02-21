from turtle import pos
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from testproject.models import TestData,Comment,Like
from account.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from . import serializer as post_serializer
from rest_framework.response import Response
from rest_framework import status
from . import pagination as post_paginations
from scipy.stats import beta
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

from testproject.ai.algorithm import beginRecommend

import math
import time


startT=0
detail_page_id=0
cnt = 0 

def initData():
    print('데이터를 초기화합니다.')
    ratings_data = pd.read_csv('/Users/ilmunkoo/Desktop/archive/ratings.csv')
    viewCnt = ratings_data['view_cnt']
    exposureCnt = ratings_data['exposure_cnt']
    
    post_list=TestData.objects.prefetch_related("user").all()
    for idx, post in enumerate(post_list):
        post.views_cnt = viewCnt[idx]
        post.exposure_cnt = exposureCnt[idx]
        post.impressions_cnt = exposureCnt[idx] - viewCnt[idx]
        post.save()


def post_list(request):
    global cnt 
    global startT
    global detail_page_id

    # 데이터 초기화 
    if cnt == 0 :
        initData()

    post_list=TestData.objects.prefetch_related("user").all()
    comment_list=Comment.objects.all().order_by('-created_date')

    #유저의 로그인 여부에 따라 추천 알고리즘을 다르게 적용.
    print("user:    " ,request.user)
    #로그인이 안되었을 시 ,전체 추천
    if not request.user.is_authenticated:

        for post in post_list:
            score=beta.rvs(post.views_cnt, abs(post.impressions_cnt))
            post.importance = score
            post.save()

        post_list = TestData.objects.prefetch_related("user").order_by("-importance").all()
    #로그인이 되었을 시, 개별 유저에 특화하여 추천.
    else:
        #개별 유저들의 추천 알고리즘
        #post_list = TestData.objects.prefetch_related("user").order_by("-importance").all()

        posts= TestData.objects.all()#전체 게시글들
        user_likes= Like.objects.filter(user=request.user)#유저가 좋아요 누른 전체 정보들
        print(user_likes)
        svdRecList, sequentialRecList =beginRecommend(request.user.id, 5) # 10 개 기본추천 
        
        for post in post_list:
            score=beta.rvs(post.views_cnt, abs(post.impressions_cnt))
            post.importance = score
            post.save()

        # 추천리스트 정리 
        recommendList = []
        for i in range(len(svdRecList)):
            recommendList.append(svdRecList[i])
            recommendList.append(sequentialRecList[i])
        recommendList = list(set(recommendList)) # 중복제거

        #추천 리스트에 속한 게시물들은 상위권으로 
        for i in range(len(recommendList)):
            post = TestData.objects.get(id = recommendList[i])
            post.importance = 1- (0.000001*i)
            post.save()





        for post in posts:
            cnt= user_likes.filter(post=post).count()#유저가 좋아요 누른 갯수를 각 개시글에 저장
            post.user_like_cnt=cnt
            post.save()#특정 유저가 특정 게시물에 좋아요한 갯수.


    paginator= Paginator(post_list, 1)
    page_num= request.GET.get('page')   
    try:
        posts=paginator.get_page(page_num)

        for post in posts:
            post.exposure+=1
            post.impressions_cnt=post.exposure-post.views_cnt
            post.save()


    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
        
    #방문 시간을 체크하는 부분    
    #만약 직전에 방문한 페이지가 있다면
    if detail_page_id:
        #방문한 시간을 체크해 기록합니다.
        if not request.user:
            data=get_object_or_404(TestData, pk = detail_page_id)
            data.residence_time+=time.time() - startT
            data.save()
        else:
            data=get_object_or_404(TestData, pk = detail_page_id)
            data.residence_time+=time.time() - startT
            data.user_residence_time+=time.time() - startT
            data.save()

        #저장이 완료되면 시작시간과 페이지 정보를 초기화 해줍니다. 이렇게 하지 않을 시, 실제보다 많은 시간이 찍히게 됩니다.    
        startT = 0
        detail_page_id=0
    
    print(f'function time: {time.time() - startT}ms')
    cnt += 1

    return render(request, "post_list.html",{'posts':posts, 'comments':comment_list})


def click(request, id):
    global startT
    global detail_page_id

    startT = time.time()
    detail_page_id=id

    post=get_object_or_404(TestData, pk = id)
    comment_list=Comment.objects.all().order_by('-created_date')

    
    if not request.user:

        post.impressions_cnt-=1

        post.views_cnt+=1
        post.save()
    else:
        print('user like cnt : ',post.user_like_cnt)

        post.impressions_cnt+=1
        post.views_cnt+=1
        
        #유저가 방문한 페이지 +1
        post.user_views_cnt+=1
        post.save()


    return render(request, 'click.html',{"data":post, 'comments':comment_list})

def like(request, id):
    print(id)
    detail_id=id

    post=get_object_or_404(TestData, pk = detail_id)
    post.like_cnt+=1
    post.save()

    if request.user:
        like=Like(user=request.user, post=post) 
        like.save()  
    return redirect('testproject:post_list')

@login_required(login_url='account:login')
def comment_create(request, id):
    detail_id=id
    post = get_object_or_404(TestData, pk=id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            print('created date: ',comment.created_date)

            return redirect('testproject:click',id=detail_id)
    return redirect('testproject:post_list')

import numpy as np
import pandas as pd
import random
from numpy.random.mtrand import RandomState


# # 페이지네이션 커스텀 버전
# class PostPagination(PageNumberPagination):
#     page_size = 1


# class PostListView(APIView, post_paginations.PaginationHandlerMixin):
#     pagination_class = PostPagination
#     serializer_class = post_serializer.PostSerializer

#     def get(self, request):
#         posts = testData.objects.all()

#         page = self.paginate_queryset(posts)

#         if page is not None:
#             serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
#             print("데이터 ", serializer)
#         else:
#             serializer = self.serializer_class(posts, many=True)
#             print("데이터 ", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
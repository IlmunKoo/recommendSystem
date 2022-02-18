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

import math
import time

from django.contrib.auth.decorators import login_required
from .forms import CommentForm

startT=0
detail_page_id=0


        
def post_list(request):

    global startT
    global detail_page_id
    
    post_list=TestData.objects.prefetch_related("user").all()
    comment_list=Comment.objects.all().order_by('-created_date')

    #유저의 로그인 여부에 따라 추천 알고리즘을 다르게 적용.
    print("user:    " ,request.user)
    if not request.user:

        for post in post_list:
            score=beta.rvs(post.views_cnt, abs(post.impressions_cnt))
            post.importance = score
            post.save()

        post_list = TestData.objects.prefetch_related("user").order_by("-importance").all()
    else:
        #개별 유저들의 추천 알고리즘
        #post_list = TestData.objects.prefetch_related("user").order_by("-importance").all()
        pass

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
        data=get_object_or_404(TestData, pk = detail_page_id)
        data.residence_time+=time.time() - startT
        data.save()
        #저장이 완료되면 시작시간과 페이지 정보를 초기화 해줍니다. 이렇게 하지 않을 시, 실제보다 많은 시간이 찍히게 됩니다.    
        startT = 0
        detail_page_id=0
    
    print(f'function time: {time.time() - startT}ms')

    return render(request, "post_list.html",{'posts':posts, 'comments':comment_list})


def click(request, id):
    global startT
    global detail_page_id

    startT = time.time()
    detail_page_id=id

    data=get_object_or_404(TestData, pk = id)
    comment_list=Comment.objects.all().order_by('-created_date')

    if not request.user:

        data.impressions_cnt+=1
        data.views_cnt+=1
        data.save()
    else:
        data.impressions_cnt+=1
        data.views_cnt+=1
        data.save()

        #유저가 방문한 페이지 +1
        #


        
   
    return render(request, 'click.html',{"data":data, 'comments':comment_list})

def like(request, id):
    detail_id=id
    post=get_object_or_404(TestData, pk = id)
    post.like+=1
    post.save()

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

def make_data():
    # 데이터 랜덤추출 
    seed = 12
    random.seed(seed)
    rng = RandomState(seed)
    np.random.seed(seed)

    # Total posts
    total_arms  = 10

    # probs of posts : 각 게시물이 선택될 확률
    arms = [random.betavariate(1.4, 5.4) for i in range(total_arms)] # 왜 1.4 대 5.4? 

    # Rouns test
    rounds  = 100

    clicks = []
    for i, a in enumerate(arms):
        i_rounds = np.array([i+1 for i in range(rounds)])
        values   = np.random.binomial(1, arms[i], rounds) #+ decay
        clicks.append(np.sum(values))
    clicks = pd.DataFrame(clicks)
    clicks = clicks.T
    # a = 10 # 게시물 개수
    # # 랭크 
    # ranks = [] # ['인덱스', '클릭률']
    # for i in range(len(ones)):
    #     one = ones[i]
    #     zero = zeros[i]
    #     ranks.append([i, one/zero]) 

    # # 클릭률 순서로 정렬 합니다.
    # ranks = sorted(ranks, key=lambda x: x[1])
    

    return clicks

def thompson_sampling():
    N = 10000 # 10.000 users
    a = 100  # there are 10 ads type in total
    # Ni⁰(n) -> the number of times '1' arrives so far
    # Ni¹(n) -> the number of times '1' arrives so far
    total_reward = 0 # sum of rewards
    chosen_ads = []  # an empty list created for choosed ads
    ones = [0] * a   # '1' as a reward from each ad
    zeros = [0] * a  # '0' as a reward from each ad

    for n in range(1,N): # Outer loop that allows us to navigate rows
        chosen_ad = 0 
        max_beta = 0
        for i in range(0,a): # Inner loop that allows us to navigate columns
            random_beta = random.betavariate (ones[i] +1 , zeros[i] +1) # Creating random beta by giving α(alpha) and β values
            if random_beta > max_beta:
                max_beta = random_beta # Max_beta is constantly updated, if a value greater than itself, it changes.
                chosen_ad = i  # We add which ad we clicked for each line to the selected ads
        chosen_ads.append(chosen_ad) # We add whichever ad we choose in each row to the selected ads list
        reward = df.values[n,chosen_ad] # If n. chosed ad data in row=1, reward=1. otherwise 0
        if reward == 1:
            ones[chosen_ad] = ones[chosen_ad]+1 # When the reward is 1, increase the reward of the corresponding ad by 1.
        else :
            zeros[chosen_ad] = zeros[chosen_ad] + 1 # When the reward is 1, increase the value of the corresponding ad in the ones list by 1.
        total_reward = total_reward + reward  # Add the reward resulting from the operation performed on each row of the dataset to the total reward.
    ranks  = []
    for i in range(100): # ranking 과정
        ratio = ones[i] / zeros[i]
        ranks.append([i, ratio])

    return ranks

# def toHome(request):
    
#     start=request.start
#     end = time.time()
#     print( end - start,"sec")

#     post_list=testData.objects.all()
#     for post in post_list:
#         score=post.views_cnt//post.impressions_cnt
#         post.importance=score
#         post.save()
#     post_list=testData.objects.all().order_by('-importance')

#     paginator= Paginator(post_list, 1)
#     page_num= request.GET.get('page')
    
#     try:
#         posts=paginator.get_page(page_num)
#     except PageNotAnInteger:
#         posts=paginator.page(1)
#     except EmptyPage:
#         posts=paginator.page(paginator.num_pages)

#     for post in posts:
#         post.impressions_cnt+=1
#         post.save()
#         print(post.impressions_cnt)

#     return render(request, "post_list.html",{'posts':posts})

   

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
import numpy as np
from scipy.stats import beta
import random
import pandas as pd
from matplotlib import pyplot as plt 
from sklearn.decomposition import TruncatedSVD
# from recommendSimilar import recByItem
# from recByUser import recByUser
from testproject.ai.spotlightRecsys import svdRecsys, sequentialRecsys







def beginRecommend(userId, recNum):
    sequentialRecList = sequentialRecsys(userId, recNum)
    svdRecList = svdRecsys(userId, recNum)
    # 비슷한 아이템 추천 (특정 게시물과 유사한 게시물) 
    # user_ratings, ratings_data = getData(ctr)
    # recByItemList= recByItem(user_ratings)
    # print(recByItemList)
    

    # # 유저 기반 추천
    # userNum= 237
    # recNum = 10
    # userHistory, recByUserList = recByUser(user_ratings,ratings_data, userNum, recNum)

    # print(f'아이템기반 추천 리스트: {recByItemList}')
    # print(f'사용자 히스토리 기반 추천 리스트: {recByUserList}')
    # print(f'유저 히스토리: {userHistory}')

    return svdRecList, sequentialRecList



# def main():
#     # initUser()
#     svdRecList, sequentialRecList  =  BeginRecommend(5) # userId
#     print(svdRecList, sequentialRecList)

# if __name__ == '__main__':
#     main()
#     # init()
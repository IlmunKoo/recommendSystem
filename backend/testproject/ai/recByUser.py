from scipy.sparse.linalg import svds
from scipy.sparse import diags
import numpy as np
import pandas as pd

# 사용자 개인에게 맞춤을 영화를 추천해주는 개인화 추천 시스템 구현 
# 개인 영화 히스토리 기반 

# 데이터 전처리
# 먼저, 사용자-영화 평점 데이터를 pivot table 형식으로 바꿔준다.
# N명의 사용자가 매긴 각각의 평균 평점은 어떻게 되는지 구한다.
# 그 값을 사용자-영화 평점 값에서 빼도록 한다. 

def recByUser(user_ratings, ratings_data, userNum , recNum):
    # pivotTable -> numpy matrix
    matrix = user_ratings.values

    # user_ratings_mean은 사용자의 평균 평점
    userRatingsMean = np.mean(matrix, axis = 1) # 각 row별 평균을 구하라

    # R_user_mean : 0~101까지 존재하던 rating 분포가 각 사용자의 rating 평균을 뺀다.
    matrixUserMean = matrix - userRatingsMean.reshape(-1, 1)
    # 두 개를 빼려면 이렇게 해 줘야 하나? 

    # 아까와 같은 게시물-사용자 평점 데이터이다.
    # N명의 사용자가 매긴 각각의 평균을 사용자 별로 빼주었기 때문에 값이 조금 변경되었을 뿐이다. 
    pd.DataFrame(matrixUserMean, columns= user_ratings.columns)
    # SVD(특이값 분해)를 통해 latent factor matrix factorization을 진행한다.
    # Scipy 제공 svds는 TruncatedSVD 개념을 사용하므로 이를 사용한다. 


    # U 행렬, sigma 행렬, V 전치 행렬을 각각 반환하여 준다.
    U, sigma, Vt = svds(matrixUserMean, k = 12) # k =latent factor 

    # 위와 같이 진행하면 현재 Sigma 행렬은 0이 아닌 값만 1차원 행렬로 표현된 상태이다. 
    # 0이 포함된 대칭행렬로 변환할 때는 numpy의 diag(대각행렬)를 이용한다. 
    sigma = diags(sigma, 0).toarray()


    # U, Sigma, Vt의 내적 수행시 다시 원본 행렬로 복원된다.
    # 거기에 아까 빼주었던 사용자 평균 rating를 더해준다. 
    svdUserPredictedRatings = np.dot(np.dot(U, sigma),Vt) + userRatingsMean.reshape(-1,1)

    dfSvdPreds = pd.DataFrame(svdUserPredictedRatings, columns = user_ratings.columns)
    print(dfSvdPreds)
    # 원본 데이터 만들어주기 
    userRating =  ratings_data.copy()
    postRating =  ratings_data.copy()

    userRating.drop(['postId', 'timestamp'], axis='columns', inplace=True)
    postRating.drop(['userId','timestamp'], axis='columns', inplace=True)

    # 330번 user가 Matrix Factorization 기반의 추천 시스템에게 받은 게시물 추천 목록이다.

    userHistory, predictions = recommendPosts(dfSvdPreds, userNum,postRating, userRating, recNum )

    return userHistory, predictions




# 함수를 하나 만든다. 
# 인자로 사용자 아이디, 게시물 정보 테이블, 평점 테이블 등을 받음
# 사용자 아이디에 SVD로 나온 결과와 영화 평점이 가장 높은 데이터 순으로 정렬
# 사용자가 본 데이터는 제외
# 사용자가 안 본 게시물 중에서 평점이 높은 것을 추천

# 사용자 히스토리 기반으로 가장 연관성이 높은 영화를 추천해주어야 한다.
# 그래서 이미 사용자의 평균 평점 데이터를 넣어 놓았다. 여기에서는 사용자가 본 영화는 제외하고 영화를 추천해준다.

def recommendPosts(dfSvdPreds, userId, oriPostsDf, oriRatingsDf, numRecommendations = 5):
    # 현재는 index로 적용되어 있으므로 user_id -1 을 해야 한다
    userRowNum = userId -1 
    
    # 최종적으로 만든 pred_df에서 사용자 index에 따라 게시물 데이터 정렬(row선택)-> 게시물 평가 높은 순서대로 정렬
    sortedUserPredictions = dfSvdPreds.iloc[userRowNum].sort_values(ascending = False) 
    
    # 원본 평점 데이터에서 userId에 해당하는 데이터를 뽑아낸다.(데이터프레임에 조건 삽입)
    userData = oriRatingsDf[oriRatingsDf.userId == userId]
#     userData = userRating[userRating.userId == 30]
    
    # 위에서 뽑은 userData와 원본 게시물 데이터를 합친다.
#     userHistory = userData.merge(oriPostsDf, on = 'postId').sort_values(['rating'], ascending = False)
    userHistory = userData.merge(oriPostsDf, left_index=True, right_index=True)
    userHistory.drop(['rating_x'], axis = 'columns', inplace =True)
    userHistory = userHistory.rename(columns={'rating_y': 'rating'}).sort_values(['rating'], ascending = False)
    
    
    # 원본 게시물 데이터에서 사용자가 본 게시물 데이터를 제외한 데이터 추출(제외가 맨 마지막에 오는듯)
    recommendations = oriPostsDf[~oriPostsDf['postId'].isin(userHistory['postId'])]
    
    # 사용자의 게시물 평점이 높은 순으로 정렬된 데이터와 위 recommendations를 합친다. (합친 후 인덱스를 다시 설정한다. )
    recommendations = recommendations.merge(pd.DataFrame(sortedUserPredictions).reset_index(), on='postId')
    
    
    return userHistory, recommendations




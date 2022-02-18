from sklearn.decomposition import TruncatedSVD
import numpy as np
import pandas as pd

def recByItem(user_ratings):
    # 특정영화와 비슷한 영화를 추천해주는 컨셉으로 간다. 
    post_ratings = user_ratings.values.T

    SVD = TruncatedSVD(n_components = 12) # 잠재요소인 latent = 12
    matrix= SVD.fit_transform(post_ratings)

    # 이렇게 나온 데이터끼리 피어슨 상관계수를 통해 구해준다.
    # numpy의 corrcoef를 이용하면 된다. 
    corr = np.corrcoef(matrix) # 각 게시물 사이의 피어슨 상관계수 
    post_ratings = pd.DataFrame(post_ratings)

    # 특정 영화와 관련하여 상관계수가 높은 영화를 보여준다. 

    postId = user_ratings.columns # 개수가 9066개로 맞아야 한다. 
    postIdList = list(postId)
    coeffHands = postIdList.index(10) 

    corrCoeffHands = corr[coeffHands]

    recList = list(postId[(corrCoeffHands>= 0.9)])[:50] # 개수가 각각 9066개로 맞아야 비교 가능

    return recList

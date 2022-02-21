import numpy as np
import pandas as pd
from spotlight.interactions import Interactions
from spotlight.cross_validation import random_train_test_split
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
import torch
from keras.models import load_model

#Training a Matrix Factorization Model
def getRatings():
    ratings_data = pd.read_csv('/Users/ilmunkoo/Desktop/archive/ratings.csv')
    ratings_data.rename(columns={'movieId': 'postId'}, inplace=True)
    return ratings_data
    
def trainMFmodel(dataset):
    train, test = random_train_test_split(dataset)
    model = ExplicitFactorizationModel(n_iter=10)
    model.fit(train, verbose=True)
    rmse = rmse_score(model, test)
    print('RMSE = ', rmse)
    torch.save(model, '/Users/ilmunkoo/Desktop/archive/svdmodel.pt')

    return model

def getSVDModel():
    model = torch.load('/Users/ilmunkoo/Desktop/archive/svdmodel.pt')
    # model.eval()

    return model

def getData():
    ratings_data = pd.read_csv('/Users/ilmunkoo/Desktop/archive/ratings.csv')
    ratings_data.rename(columns={'movieId': 'postId'}, inplace=True)


    d = dict.fromkeys(ratings_data.select_dtypes(np.int64).columns, np.int32)
    ratings_data = ratings_data.astype(d)

    dataset = Interactions(user_ids=ratings_data['userId'].values,
                       item_ids=ratings_data['postId'].values,
                       ratings=ratings_data['rating'].values,
                       timestamps=ratings_data['timestamp'].values)

    return dataset


def recommend_movies(user_id, model, n_posts=5):
    """
    Recommends movies for user using a matrix factorization model.
    """ 
    pred = model.predict(user_ids=user_id)
    indices = np.argpartition(pred, -n_posts)[-n_posts:]
    best_posts_ids = indices[np.argsort(pred[indices])]
    
    return [ post_id for post_id in best_posts_ids]

def svdRecsys(userId,recNum):
    # dataset = getData()
    # model = trainMFmodel(dataset)
    model = getSVDModel()
    recList = recommend_movies(userId, model, recNum)

    return recList



# Training a Sequence Model
# 유저 히스토리 기반 
from spotlight.sequence.implicit import ImplicitSequenceModel
from spotlight.cross_validation import user_based_train_test_split
from keras.models import load_model


def getPosts():
    posts = pd.read_csv('/Users/ilmunkoo/Desktop/archive/postRatings.csv') # userId=9 의 movieId 데이터 추출하여 movieId=42 데이터가 있는지 확인. 
    return posts

def recommend_next_posts(posts, model, n_posts):
    
    """
    Recommends the top n next movies that a user is likely to watch 
    based on a list of previously watched movies.
    """
    
#     post_ids = np.array([post for post in posts]).astype(float).astype(int)
    pred = model.predict(sequences=np.array(posts))
    indices = np.argpartition(pred, -n_posts)[-n_posts:]
    best_post_ids = indices[np.argsort(pred[indices])]
    return [post_id for post_id in best_post_ids]


def trainSqtialModel(dataset):
    train, test = user_based_train_test_split(dataset)
    train = train.to_sequence()
    test = test.to_sequence()
    model = ImplicitSequenceModel(n_iter=10,
                                representation='cnn',
                                loss='bpr')
    model.fit(train)
    torch.save(model, '/Users/ilmunkoo/Desktop/archive/SqtiaModel.pt')

    return model

def getSqtialModel():
    model = torch.load('/Users/ilmunkoo/Desktop/archive/SqtiaModel.pt')
    return model


def sequentialRecsys(userId, recNum):
    # dataset = getData()
    # model = trainSqtialModel(dataset)
    model = getSqtialModel()

    posts = getPosts()

    recList = recommend_next_posts(posts, model, recNum)
    return recList







    

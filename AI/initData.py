import numpy as np
from scipy.stats import beta
import random
import pandas as pd

def initData():
        print("init starts")
        # '0' as a reward from each ad
        # 데이터 랜덤추출 

        rounds  = 1000
        # Total posts
        total_arms  = 10004
        ones = np.full(total_arms, 0)
        zeros = np.full(total_arms, 0)
        ctr = np.full(total_arms, 0)
        
        # Rouns test
        clicks = []
        arms = beta.rvs(1.4, 5.4, size= total_arms)

        for i in range(len(arms)):
            ones[i] = int(round(arms[i],2)*100)
            zeros[i] = 100 - int(round(arms[i],2)*100)
            ctr[i] = (ones[i] / zeros[i])* 10
        ones = ones.astype(int)
        zeros = zeros.astype(int)
        print(ones, zeros, ctr)
        print("init ends")
        return ones, zeros, ctr
        


import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from account import models as user_models
from testproject import models as post_models
import random
import numpy as np
from scipy.stats import beta



"""
commend: python3 manage.py seed testproject --number=100
"""

class Command(BaseCommand):
    
    help = "This command creates posts"

    def __init__(self):
        print("initiation")
        self.random_cnt = 0
        self.ones = []
        self.zeros = []
        # self.init_data()

    def init_data(self):
        print("init starts")
        # '0' as a reward from each ad
        # 데이터 랜덤추출 

        # Total posts
        total_arms  = 100
        
        # Rouns test
        rounds  = 100
        clicks = []

        self.ones = np.full(total_arms, 0)
        self.zeros = np.full(total_arms, 0)

        arms = beta.rvs(1.4, 5.4, size= total_arms)

        for i in range(len(arms)):
            self.ones[i] = int(round(arms[i]*100,2))
            self.zeros[i] = 100 - int(round(arms[i],2)*100)
        self.ones = self.ones.astype(int)
        self.zeros = self.zeros.astype(int)
        print(self.ones, self.zeros)

        print("init ends")
        
    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many posts do you want")

    def handle(self, *args, **options):
        if self.random_cnt == 0:
            self.init_data()
            print('init data on')

        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()

        random_idx=list(i for i in range(100))

        seeder.add_entity(post_models.TestData, number, {
            "user": lambda x: random.choice(all_user),
            "image": lambda x:  f"images/insta{random.choice(random_idx)}.jpg",
            "views_cnt": lambda x: self.ones[self.random_cnt],
            "exposure": lambda x: self.zeros[self.random_cnt],
            "text_length": lambda x: random.randint(1,10000),
            "image_cnt": lambda x: random.randint(1,10000),
            "like": lambda x:  random.randint(1,10000),
        })
        created_room = seeder.execute()

        self.random_cnt += 1

        created_clean = flatten(list(created_room.values()))
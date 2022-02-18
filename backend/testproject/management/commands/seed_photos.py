import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from account import models as user_models
from testproject import models as post_models
import random
import numpy as np

"""
commend: python3 manage.py seed testproject --number=100
"""

class Command(BaseCommand):
    
    help = "This command creates posts"

    def __init__(self):
        self.random_cnt = 0
        self.ones = []
        self.zeros = []

    def init_data(self):
        print("init starts")
        # '0' as a reward from each ad
        # 데이터 랜덤추출 
        seed = 12
        random.seed(seed)
        rng = np.random.RandomState(seed)
        np.random.seed(seed)

        # Total posts
        total_arms  = 10

        # probs of posts : 각 게시물이 선택될 확률
        arms = [random.betavariate(1.4, 5.4) for i in range(total_arms)] 
    
        # Rouns test
        rounds  = 100
        clicks = []

        self.ones = np.full(rounds, 0)
        self.zeros = np.full(rounds, 0)

        # 알파, 베타값의 배열 초기화 
        for _ in range(rounds):
            value = np.random.choice(2, len(arms), arms) # 매 라운드마다 확률에 따라  0 or 1 값 다시 생성 
            for i in range(len(value)):  # 랜덤추출 
                print(f" idx : {i}")
                if value[i] == 1: 
                    self.ones[i] += 1
                else:
                    self.zeros[i] += 1
        print("init ends")
        
    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many posts do you want")

    def handle(self, *args, **options):

        if self.random_cnt == 0:
            self.init_data()

        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()

        random_idx=list(i for i in range(100))

        seeder.add_entity(post_models.testData, number, {
            "user": lambda x: random.choice(all_user),
            "image": lambda x:  f"images/insta{random.choice(random_idx)}.jpg",
            "views_cnt": lambda x: self.ones[self.random_cnt],
            "impressions_cnt": lambda x: self.zeros[self.random_cnt],
            "text_length": lambda x: random.randint(1,10000),
            "image_cnt": lambda x: random.randint(1,10000),
            "like": lambda x:  random.randint(1,10000),
            "importance":lambda x: random.randint(1,10000),
        })
        created_room = seeder.execute()

        self.random_cnt += 1

        created_clean = flatten(list(created_room.values()))
import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from account import models as user_models
from testproject import models as post_models
import random
import numpy as np



class Command(BaseCommand):
    
    help = "This command creates posts"

    def init_data(self):
        print("init starts")
        # '0' as a reward from each ad
        ones = [] # '1' as a reward from each ad
        zeros = []
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

        # 알파, 베타값의 배열 초기화 
        for _ in range(rounds):
            for i, a in enumerate(arms):  # 랜덤추출 
                value = np.random.binomial(1, a, rounds) # arms의 확률대로 초기화:  0 or 1 
                if value == 1: 
                    self.ones[i] += 1
                else:
                    self.zeros[i]+= 1
        
        post_list = post_models.testData.objects.all()

        for i, post in enumerate(post_list):
            post.views_cnt =  ones[i]
            print(f"views_cnt : {post.views_cnt}")
            post.impressions_cnt=  zeros[i]
            post.save()
        print("init ends")
        
    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many posts do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()

        random_idx=list(i for i in range(100))

        seeder.add_entity(post_models.testData, number, {
            "user": lambda x: random.choice(all_user),
            "image": lambda x:  f"images/insta{random.choice(random_idx)}.jpg",

            "views_cnt": lambda x: random.randint(1,10000),
            "impressions_cnt": lambda x: random.randint(100000,10000000),
            "text_length": lambda x: random.randint(1,10000),
            "image_cnt": lambda x: random.randint(1,10000),
            "like": lambda x:  random.randint(1,10000),
            "importance":lambda x: random.randint(1,10000),
        })
        created_room = seeder.execute()
        created_clean = flatten(list(created_room.values()))

        self.stdout.write(self.style.SUCCESS(f"{number} of lists Created"))
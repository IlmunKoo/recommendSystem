from .models import TestData
from rest_framework import serializers
from . import models as post_models

class TestDataSerializer(serializers.ModelSerializer):

    class Meta:
        model= TestData
        fields= "__all__"


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = post_models.TestData
        fields = "__all__"
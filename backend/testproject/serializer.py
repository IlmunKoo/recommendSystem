from .models import testData
from rest_framework import serializers
from . import models as post_models

class testDataSerializer(serializers.ModelSerializer):

    class Meta:
        model= testData
        fields= "__all__"


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = post_models.testData
        fields = "__all__"
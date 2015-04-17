from django.forms import widgets
from rest_framework import serializers
from api.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')
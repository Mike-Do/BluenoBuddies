# Serialize our models to JSON
from rest_framework.serializers import ModelSerializer
from base.models import Room

# pass in ModelSerializer into class
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        # takes all fields from Room model and
        # serializes it to be used as JSON
        fields = '__all__'
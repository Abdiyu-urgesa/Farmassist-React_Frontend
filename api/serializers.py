from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import StringRelatedField ,SlugRelatedField
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(ModelSerializer):
    groups = SlugRelatedField(many=True, read_only=True, slug_field="name")
    userprofile=UserProfileSerializer(many=False, read_only=True)
    user= StringRelatedField(many=False)
    class Meta:
        model = User
        fields = ['id','email','username','is_active','groups','userprofile','user']
  
class FederalSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Federal
        fields = '__all__'

class RegionSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = Region
        fields = '__all__'
        # exclude = ('id', )

class ZoneSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = Zone
        fields = '__all__'

class WoredaSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = Woreda
        fields = '__all__'

class KebeleAdminSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = KebeleAdmin
        fields = '__all__'

class KebeleBusinessSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = KebeleBusiness
        fields = '__all__'

class FarmerSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = Farmer
        fields = '__all__'

class PrivateSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    created_by= StringRelatedField(many=False)
    class Meta:
        model = PrivateSector
        fields = '__all__'

class PostSerializer(ModelSerializer):
    posted_by = UserSerializer(many=False)
    class Meta:
        model = Post
        fields = '__all__'

class AnnouncementSerializer(ModelSerializer):
    to = UserSerializer(many=False)
    class Meta:
        model = Announcement
        fields = '__all__'

class DiseaseSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Disease
        fields = '__all__'

class ResourceSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Resource
        fields = '__all__'

class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
class SentResourceSerializer(ModelSerializer):
    class Meta:
        model = SentResource
        fields = '__all__'


class BarSerializer(serializers.Serializer):
    region = serializers.CharField()
    zones = serializers.IntegerField()
    zonescolor = serializers.CharField()
    woredas = serializers.IntegerField()
    woredascolor = serializers.CharField()
    kebeleAdmin = serializers.IntegerField()
    kebeleAdmincolor = serializers.CharField()







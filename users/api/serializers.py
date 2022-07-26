from rest_framework import serializers
from users.models import Review, UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class UserEmailField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['password','email']
    
    def getModel(self):
        return self.Meta.model.object.email


class UserReturnSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['id','username','email','name','avatar','address','age','subscribed_date','subscription','is_admin','related_admin']
        read_only_fields = ('is_active', 'is_staff', 'subscribed_date', 'subscription', 'related_admin', 'is_admin')

    def get_validation_exclusions(self):
        exclusions = super(UserReturnSerializer, self).get_validation_exclusions()
        return exclusions + ['email']

class UserRegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True,write_only=True)
    username=serializers.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = ['email','password','username','address','age','first_name','last_name','is_admin']



class ReviewSerializer(serializers.ModelSerializer):
    user = UserEmailField(read_only=True)

    class Meta:
        model = Review
        fields=['id','title','description','rating','user','created_at']
        read_only_fields = ['id','title','description','rating','user','created_at']


class ReviewInSerializer(serializers.ModelSerializer):
    title=serializers.CharField(required=True)
    rating=serializers.IntegerField(required=True,validators=[MinValueValidator(0), MaxValueValidator(5)] )
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),required=False)
    class Meta:
        model = Review
        fields=['id','title','description','rating','user','created_at']


class ResetPasswordSerializer(serializers.Serializer):
    new_password=serializers.CharField(required=True,write_only=True)
    confirm_password=serializers.CharField(required=True,write_only=True)
    class Meta:
        fields=['new_password','confirm_password']


class UserActivityReturnSerializer(serializers.Serializer):
    created_at = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)
    device = serializers.CharField(read_only=True)
    device_count = serializers.IntegerField(read_only=True)

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
    
#     class Meta:
#         model = Profile
#         fields = '__all__'

#     def create(self, validated_data):

#         print(validated_data)
#         user_data = validated_data.pop('user')
        
#         # For Creating user manager is used
#         user_obj = UserProfile.objects.create_user(**user_data)
#         my_group = Group.objects.get(name='customer')
#         my_group.user_set.add(user_obj)

#         # for user_da in user_data:
#         profile = Profile.objects.create(user=user_obj, **validated_data)

#         return profile


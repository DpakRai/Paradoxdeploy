from rest_framework import serializers
from AI.models import BaseDevice, MediaFile
from users.api.serializers import ReviewSerializer, UserEmailField

class MediaSerailizer(serializers.ModelSerializer):  
    class Meta:
        model = MediaFile
        fields = '__all__'


class GetDeviceSerializer(serializers.ModelSerializer):

    screenshots = MediaSerailizer(many=True)
    reviews = ReviewSerializer(many=True)
    user = UserEmailField(read_only=True)
    type = serializers.CharField(source='get_type_display')

    class Meta:
       
        model = BaseDevice
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):

    screenshots = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=MediaFile.objects.all())
    
    def get_fields(self, *args, **kwargs):
        fields = super(DeviceSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['user'].required = False
            fields['title'].required = False
            fields['screenshots'].required = False
        return fields

    def create(self, validated_data):
        screenshots = validated_data.pop('screenshots')
        device = BaseDevice.objects.create(**validated_data)

        for screenshot in screenshots:
            device.screenshots.add(screenshot)
    
        device.save()
        return device


    def update(self, instance, validated_data):
        screenshots = validated_data.pop('screenshots')

        if screenshots:
            instance.screenshots.clear()
            for screenshot in screenshots:
                instance.screenshots.add(screenshot)
        
        return super(DeviceSerializer, self).update(instance, validated_data)

    class Meta:
        model = BaseDevice
        fields = '__all__'
        read_only_fields = ('id' ,'created_at', 'published_date', 'is_published', 'average_rating', 'reviews')
    

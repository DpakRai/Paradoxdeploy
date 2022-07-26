from rest_framework import serializers
from extensions.models import Extension
from AI.models import MediaFile
from AI.serializers import MediaSerailizer
from users.api.serializers import UserEmailField, ReviewSerializer


class GetExtensionSerializer(serializers.ModelSerializer): 
    screenshots = MediaSerailizer(many=True)
    reviews = ReviewSerializer(many=True)
    user = UserEmailField(read_only=True)

    class Meta:
        model = Extension
        fields = '__all__'
        read_only_fields = ('id', 'average_rating', 'reviews', 'download')

class ExtentionSerializer(serializers.ModelSerializer):
    screenshots = serializers.PrimaryKeyRelatedField(many=True, queryset=MediaFile.objects.all())

    class Meta:
        
        model = Extension
        fields = '__all__'

    def create(self, validated_data):
        screenshots = validated_data.pop('screenshots')
        extension = Extension.objects.create(**validated_data)

        for screenshot in screenshots:
            extension.screenshots.add(screenshot)

        extension.save()
        return extension


    def update(self, instance, validated_data):

        screenshots = validated_data.pop('screenshots')
        if screenshots:
            instance.screenshots.clear()
            for screenshot in screenshots:
                instance.screenshots.add(screenshot)
        
        return super(ExtentionSerializer, self).update(instance, validated_data)
    
    

    
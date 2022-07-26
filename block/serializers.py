from rest_framework import serializers
from AI.serializers import  MediaSerailizer
from users.models import Review
from AI.models import MediaFile
from block.models import Block
from django.contrib.auth import get_user_model
from users.api.serializers import ReviewSerializer, UserEmailField


User = get_user_model()


class GetBlockSerializer(serializers.ModelSerializer):
    screenshots = MediaSerailizer(many=True)
    reviews = ReviewSerializer(many=True)
    user = UserEmailField(read_only=True)

    class Meta:
        model = Block
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    screenshots = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=MediaFile.objects.all())

    class Meta:
        model = Block
        fields = '__all__'
        read_only_fields = ('id', 'average_rating', 'reviews')

    def get_fields(self, *args, **kwargs):
        fields = super(BlockSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['user'].required = False
            fields['title'].required = False
            fields['screenshots'].required = False
        return fields

    def create(self, validated_data):
        screenshots = validated_data.pop('screenshots')

        block = Block.objects.create(**validated_data)
        for screenshot in screenshots:
            block.screenshots.add(screenshot)
        
        block.save()
        return block


    def update(self, instance, validated_data):
        screenshots = validated_data.pop('screenshots')
        
        if screenshots:
            instance.screenshots.clear()
            for screenshot in screenshots:
                instance.screenshots.add(screenshot)
        
        return super(BlockSerializer, self).update(instance, validated_data)

    
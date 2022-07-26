from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from django.utils.decorators import method_decorator
from Appstore.decorator import check_token

from users.api.serializers import ReviewInSerializer, ReviewSerializer
from AI.models import BaseDevice, MediaFile
from AI.serializers import DeviceSerializer, GetDeviceSerializer, MediaSerailizer
from rest_framework.views import APIView
from users.models import UserProfile, Review
from rest_framework import status


class BaseDeviceView(ModelViewSet):
    '''
    ViewSet for Device model which provides CRUD operations.
    '''
    queryset = BaseDevice.objects.all()
    serializer_class = DeviceSerializer
    list_serializer_class = GetDeviceSerializer
    parser_classes = [FormParser, MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class
        return super(BaseDeviceView, self).get_serializer_class()

    

    @method_decorator(check_token)
    def create(self, request, *args, **kwargs):
        """
        Create a new device
        """
        data = request.data
        data._mutable = True

        screenshots = data.getlist("screenshots")
        if screenshots:
            screenshots_obj = []  # create a list to store screenshots objects
            for screenshot in screenshots:  # for each screenshot
                if not isinstance(screenshot, str):  # if screenshot is not a integer
                    screenshots_obj.append(MediaFile.objects.create(
                            file=screenshot, title=data.get('title')
                        ).id)
                    
            request.data.setlist("screenshots", screenshots_obj)   # assigning list to screenshots

        user = data.get("user")
        user_obj = UserProfile.objects.get(email=user).id if user else request.user.id
        request.data["user"] = user_obj

        return super().create(request, *args, **kwargs)

    @method_decorator(check_token)
    def update(self, request, *args, **kwargs):
        '''
        Update a device
        '''
        data = request.data
        data._mutable = True # make data mutable

        screenshots = data.getlist("screenshots")
        if screenshots:
            screenshots_obj = []  # create a list to store screenshots objects
            for screenshot in screenshots:  # for each screenshot
                if isinstance(screenshot, str):  # if screenshot is a integer
                    if all(i.isdigit() for i in screenshot):
                        screenshots_obj.append(screenshot)
                else:
                    screenshots_obj.append(MediaFile.objects.create(
                            file=screenshot, title=data.get('title')
                        ).id)
                    
            request.data.setlist("screenshots", screenshots_obj) 

        user = data.get("user")
        if user:
            user_obj = UserProfile.objects.get(email=user).id
            request.data["user"] = user_obj

        return super().update(request, *args, **kwargs)

    @method_decorator(check_token, name="dispatch")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AIReview(APIView):
    '''
    ViewSet for Review model which provides CRUD operations.
    '''
    serialzier_class = ReviewSerializer
    performer_class = ReviewInSerializer
    queryset = Review.objects.all()
    
    @method_decorator(check_token)
    def post(self, request, id, *args, **kwargs):
        try:
            ai_object = BaseDevice.objects.get(id=id)
        except BaseDevice.DoesNotExist:
            return Response({"message": "AI does not exist"}, status=status.HTTP_404_NOT_FOUND)

        review_objects = Review.objects.filter(user=request.user)
        all_reviews = ai_object.reviews.all()
        if review_objects.intersection(all_reviews):
            return Response({"message": "You have already reviewed this AI"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.performer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        review = serializer.save()
        ai_object.reviews.add(review)
        ai_object.save()
        return Response({"message": "Review created successfully"}, status=status.HTTP_200_OK)
    
    @method_decorator(check_token)
    def patch(self, request, id,*args, **kwargs):
        try:
            review_object = Review.objects.get(id=id, user=request.user.id)
            if review_object:
                ai_obj = review_object.device_reviews.all()[0]
        except Review.DoesNotExist:
            return Response({"message": "Review does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.performer_class(
            review_object, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ai_obj.save()
        return Response({"message": "Review updated successfully"}, status=status.HTTP_200_OK)

    @method_decorator(check_token)
    def delete(self, request, id,*args, **kwargs):
        try:
            review_object = Review.objects.get(id=id)
            if review_object:
                ai_obj = review_object.device_reviews.all()[0]
        except Review.DoesNotExist:
            return Response({"message": "Review does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if not review_object.user == request.user:
            return Response("You are not allowed to delete others review", status=status.HTTP_403_FORBIDDEN)
        review_object.delete()
        ai_obj.save()
        return Response("Deleted successfully", status=status.HTTP_204_NO_CONTENT)


class PublishAI(APIView):
    '''
    ViewSet for PublishAI model which provides CRUD operations.
    '''
    def post(self, request, id, *args, **kwargs):
        try:
            ai_object = BaseDevice.objects.get(id=id)
        except BaseDevice.DoesNotExist:
            return Response({"message": "AI does not exist"}, status=404)

        related_admin = ai_object.user.related_admin

        if related_admin == request.user:
            ai_object.is_published = True
            ai_object.save()
            return Response({"message": "AI published successfully"}, status=200)
        else:
            return Response({"message": "You are not authorized to publish this AI"}, status=400)


class GetMediaView(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaSerailizer

    
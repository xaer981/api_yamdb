from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status

from api_yamdb.users.models import User

from .filters import TitleFilters
from .mixins import CreateListDestroyViewSet
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGETSerializer, TitleSerializer,
                          UserSerializer, AdminSerializer,
                          SignupSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.prefetch_related('genre', 'category')
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':

            return TitleGETSerializer

        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    search_fields = ('username',)
    # permission_classes =

    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = AdminSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.is_admin:
            serializer = AdminSerializer(
                user, data=request.data, partial=True
            )
        else:
            serializer = UserSerializer(
                user, data=request.data, partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


def signup(request):
    if request.user.is_authenticated:
        raise ValidationError('Вы уже зарегистрированы!')
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Добро пожаловать на проект YaMDb!',
        from_email='e-mail.com',
        recipient_list=(user.email,),
        message=confirmation_code
    )

    return Response(serializer.data, status=status.HTTP_200_OK)

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status

from api_yamdb.users.models import User

from .filters import TitleFilters
from .mixins import CreateListDestroyViewSet
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import (AdminSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          TitleGETSerializer, TitleSerializer,
                          ReviewSerializer, SignupSerializer,
                          UserSerializer)
from users.models import User


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


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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

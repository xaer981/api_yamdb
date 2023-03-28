from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilters
from .mixins import CreateListDestroyViewSet
from .permissions import CreateOrIsAuthorOrReadOnly, IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleGETSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)
from .utils import create_code_and_send_email
from reviews.models import Category, Genre, Review, Title
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.prefetch_related('genre', 'category')
                .annotate(rating=Avg('reviews__score')))
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':

            return TitleGETSerializer

        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (CreateOrIsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer = ReviewSerializer(
            data=request.data,
            context={'request': request, 'title_id': self.kwargs['title_id']})

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title_id=title.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (CreateOrIsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.is_admin:
            serializer = UserSerializer(
                user, data=request.data, partial=True
            )
        else:
            data = request.data
            if isinstance(data, QueryDict):
                data = (request.data).dict()
            if data.get('role'):
                del data['role']
            serializer = UserSerializer(
                user, data=data, partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if isinstance(data, QueryDict):
            data = (request.data).dict()

        if User.objects.filter(**data).exists():
            user = User.objects.get(**data)
            create_code_and_send_email(user)

            return Response(serializer.initial_data,
                            status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        create_code_and_send_email(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if not default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)},
        status=status.HTTP_200_OK
    )

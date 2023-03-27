from django.db.models import Avg
from rest_framework import serializers
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')

    def get_rating(self, obj):
        if avg_score := obj.reviews.aggregate(
                (Avg('score')))['score__avg']:

            return round(avg_score)

        return None


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    def validate_title_exists(self):
        if not Title.objects.filter(
           title_id=self.request.data['title_id']).exists():

            return Response({"Ошибка": "Title_id не найден"})

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Допускается оценка только от 1 до 10!')
        return value

    def validate_duplicate(self, request, data):
        if Review.objects.get(
           author=request.user, title=self.data['title'].exists):
            raise serializers.ValidationError('Уже существует')

    class Meta:
        model = Review
        fields = ('id',
                  'title',
                  'author',
                  'text',
                  'score',
                  'pub_date')
        read_only_fields = ('author', 'title')
        extra_kwargs = {'title': {'required': True},
                        'author': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'review')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        required_fields = ('username', 'email',)
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICE, default='user')

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        required_fields = ('username', 'email',)


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('недопустимое имя')

        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code',)

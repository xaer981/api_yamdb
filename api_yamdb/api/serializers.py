from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.constants import MAX_SCORE, MIN_SCORE
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH
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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


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

    def validate_title(self, value):
        if not Title.objects.filter(
           title_id=self.request.data['title_id']).exists():
            raise serializers.ValidationError('title_id не найден')

        return value

    def validate_score(self, value):
        if MIN_SCORE > value > MAX_SCORE:
            raise serializers.ValidationError(
                'Допускается оценка только от 1 до 10!')
        return value

    def validate_duplicate(self, request, data):
        if Review.objects.filter(
           author=request.user, title=self.data['title']).exists():
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


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=NAME_MAX_LENGTH)

    def create(self, validated_data):

        return User.objects.create(**validated_data)

    def validate_username(self, value):
        regex_validatior = RegexValidator(r'^[\w.@+-]+$')
        if value == 'me':
            raise serializers.ValidationError('недопустимое имя')
        regex_validatior(value)

        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким никнеймом уже существует.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.')

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code',)

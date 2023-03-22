from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title
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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role',
        )
        required_fields = ('username', 'email',)
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICE, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role',
        )
        required_fields = ('username', 'email',)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            EmailValidator()
        ),
        required=True
    )
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code',)

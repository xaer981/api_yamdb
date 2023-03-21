from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):

        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):

        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название',
                            unique=True)
    year = models.PositiveSmallIntegerField(verbose_name='год создания')
    description = models.TextField(verbose_name='описание')
    genre = models.ManyToManyField(Genre,
                                   through='TitleGenre',
                                   related_name='titles',
                                   verbose_name='жанр')
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):

        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_title_genre')
        ]

    def __str__(self):

        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='one_review_by_title_for_user')
        ]

    def __str__(self):

        return self.name


class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    def __str__(self):

        return self.name

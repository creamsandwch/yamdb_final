from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug', 'name')


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'rating',
            'year',
            'category',
            'genre',
            'description'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'pub_date', 'author')

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            author = self.context.get('request').user
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Оставлять отзыв дважды на одно произведение запрещено'
                )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me".'
            )
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

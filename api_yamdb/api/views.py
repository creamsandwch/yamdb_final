from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleGetSerializer,
                          TitlePostSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          SignUpSerializer,
                          TokenSerializer,
                          UserSerializer)
from .permissions import (IsAdminUser,
                          IsAuthorAdminModerSuperuserOrReadOnly,
                          IsAdminSuperuserOrReadOnly)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Viewset для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminSuperuserOrReadOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    """Viewset для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminSuperuserOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для произведений."""
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg('reviews__score'))
        .order_by('-year', 'name')
    )
    serializer_class = TitlePostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminSuperuserOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModerSuperuserOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModerSuperuserOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


def send_confirmation_code(username):
    """Функция для отправки email на почту."""
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    yamdb_email = 'yamdb@gmail.com'
    send_mail(
        'Код для регистрации',
        f'Код: {confirmation_code}',
        yamdb_email,
        [user.email],
        fail_silently=False,
    )
    user.save()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """ApiView-функция для регистрации."""
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        user = get_object_or_404(User, username=username)
        serializer = SignUpSerializer(user, data=request.data)
        if serializer.is_valid():
            send_confirmation_code(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        send_confirmation_code(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """ApiView-функция для получения токена."""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, str(confirmation_code)):
        token_data = {'token': str(AccessToken.for_user(user))}
        return Response(token_data,
                        status=status.HTTP_200_OK)
    return Response('Код подтверждения неверный',
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset для пользователей и Get, Patch запросов на эндпоин 'me'."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'delete', 'patch')
    permission_classes = (IsAdminUser,)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthView, TokenView, UserViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

extra_patterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', AuthView.as_view()),
    path('auth/token/', TokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(extra_patterns))
]

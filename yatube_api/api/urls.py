from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet, api_root

# Создаем отдельный роутер для v1
router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')

# Регистрируем комментарии с вложенным роутером
router_v1.register(
    r'posts/(?P<post_pk>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

# Маршруты для аутентификации v1
auth_urls_v1 = [
    path(
        'api-token-auth/',
        views.obtain_auth_token,
        name='api_token_auth'
    ),
]

# Группируем все маршруты v1
v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(auth_urls_v1)),
]

# Корневой маршрут API
api_root_url = [
    path('', api_root, name='api-root'),
]

urlpatterns = api_root_url + [
    path('v1/', include(v1_urlpatterns)),
]

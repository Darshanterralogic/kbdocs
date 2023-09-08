from django.urls import path
from django.views.decorators.cache import never_cache

from rest_framework.routers import DefaultRouter

from core import views

app_name = 'core'

urlpatterns = [
    path('', never_cache(views.IndexView.as_view()), name='index-view'),
    path('<slug:template>/', views.DynamicTemplateView.as_view(), name='view-template'),
    path('<slug:template>/<int:kbdocid>/', views.DynamicTemplateView.as_view(), name='view-template'),
    path('api/core/user/login/', never_cache(views.UserLoginApi.as_view()), name='api-user-auth'),
    path('api/core/user/logout/', never_cache(views.UserLogoutApi.as_view()), name='api-user-logout'),
    path('api/core/user/create/', never_cache(views.UserCreateApi.as_view()), name='api-user-signup'),
    path('api/core/kbdocs/', views.KBDocsApi.as_view(), name='api-kbdocs-create'),
    path('api/core/kbdocs/<int:pk>/', views.KBDocsApi.as_view(), name='api-kbdocs-update'),
]

# router = DefaultRouter()

# urlpatterns += router.urls
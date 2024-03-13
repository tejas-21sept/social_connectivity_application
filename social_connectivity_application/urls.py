from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainSlidingView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshSlidingView.as_view(), name="token_refresh"),
    path("api/users/", include("users.urls")),
    # path("api/posts/", include("posts.urls")),
]

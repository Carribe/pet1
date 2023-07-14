from django.urls import path, include, re_path
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from pet import settings
from .views import *

# router = routers.DefaultRouter()
# router.register(r"pages", PagesViewSet)
# print(router.urls)

urlpatterns = [
    path('', IndexView.as_view(), name='HomeForRedirect'),
    path("api/v1/drf-auth/", include("rest_framework.urls")),
    path('show_page/<slug:page_slug>/', ShowPageView.as_view(), name='show_page'),
    path('category/<int:cat_id>/', ShowCategoryView.as_view(), name='category'),
    path('about/', about, name="about"),
    path('add_page/', AddPageView.as_view(), name='add_page'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('regiser/', RegisterUser.as_view(), name='register'),
    path("api/v1/pageslist/", PagesAPIList.as_view()),
    path("api/v1/pageslist/<slug:slug>/", PagesAPIUpdate.as_view()),
    path("api/v1/pageslistdetail/<slug:slug>/", PagesAPIDetailView.as_view()),
    path("api/v1/pageslistdelete/<slug:slug>/", WomenAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

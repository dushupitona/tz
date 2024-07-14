from django.contrib import admin
from django.urls import path

from manager.views import IndexView, UserCreateView, CustomLoginView, ProfilesView, ProfileView, ProfileCreateView, delete_user, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='base'),
    path('reg/', UserCreateView.as_view(), name='reg'),
    path('log/', CustomLoginView.as_view(), name='log'),
    path('logout/', logout_view, name='logout'),
    path('profiles/', ProfilesView.as_view(), name='profiles'),
    path('profile/<int:profile_id>/', ProfileView.as_view(), name='profile'),
    path('profile/delete/<int:profile_id>/', delete_user, name='profile_delete'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
]

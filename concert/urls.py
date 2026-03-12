from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("songs/", views.songs, name="songs"),            # Exercise 3
    path("photos/", views.photos, name="photos"),          # Exercise 4
    path("login/", views.login_view, name="login"),        # Exercise 6
    path("logout/", views.logout_view, name="logout"),      # Exercise 6
    path("signup/", views.signup, name="signup"),          # Exercise 5
    path("concert/", views.concerts, name="concerts"),      # Exercise 7
    path("concert-detail/<int:id>", views.concert_detail, name="concert_detail"),
    path("concert_attendee/", views.concert_attendee, name="concert_attendee"),
]
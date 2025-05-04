from django.urls import path
from . import views
from .views import (
    home_view,
    groovepad,
    serve_audio,
    LoginView,
    SignupView,
    logout,
    play_beat
)

urlpatterns = [
    path("", home_view, name='home'),
    path('audio/groovepad/', groovepad, name='groovepad'),
    path('static/audio/<str:filename>/', serve_audio, name='serve_audio'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', logout, name='logout'),
    path('play_beat/', views.play_beat, name='play_beat'),
    path('get-flask/', views.get_flask_data, name='get_flask_data'),
]

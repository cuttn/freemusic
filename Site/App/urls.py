from django.urls import path, include
from . import views
    # path('members/spotify_callback', views.tokenn, name="getdatoken"),
urlpatterns = [
    path('', views.login, name="login"),
    path('token', views.landing, name="redirect"),
    path('App/spotify_callback', views.tokenn, name="getdatoken"),
    path('home/', views.home, name="homepage"),    
    path('browser/<str:reqType>/<str:selected>', views.browser, name="browser"),
    path('download/<str:reqType>/<str:ids>', views.download, name="magicshit"),
]
from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^players/$', views.PlayerList.as_view()),
    url(r'^players/(?P<pk>[0-9]+)/$', views.PlayerDetail.as_view()),
    url(r'^players/(?P<pk>[0-9]+)/rating/(?P<game_type>mcr|riichi)/$', views.RatingEntriesList.as_view()),
    url(r'^games/(?P<game_type>mcr|riichi)/$', views.GamesOfTypeList.as_view()),
    url(r'^games/$', views.AllGamesList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/$', views.GameDetail.as_view()),
    url(r'^ratinglist/(?P<game_type>mcr|riichi)/$', views.RatingList.as_view()),

    #User defined auth
    url(r'^auth/login$', views.LoginView.as_view()),
    url(r'^auth/logout$', views.LogoutView.as_view()),
)

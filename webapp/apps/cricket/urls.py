from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	path('team/create/list/', views.TeamCreateList.as_view(), name='team-create-list'),
	path('team/detail/<int:pk>/', views.TeamRetrieveUpdateDelete.as_view(), name='team-retrieve-update-delete'),
	path('player/create/list/', views.PlayerCreateList.as_view(), name='player-create-list'),
	path('player/detail/<int:pk>/', views.PlayerRetrieveUpdateDelete.as_view(), name='player-retrieve-update-delete'),
	path('series/create/list/', views.SeriesCreateList.as_view(), name='series-teams-list'),
	path('series/detail/<int:pk>/', views.SeriesRetrieveUpdateDelete.as_view(), name='series-retrieve-update-delete'),
	path('matches/create/list/', views.MatchesBwTeamsCreateList.as_view(), name='matches-teams-list'),
	path('matches/detail/<int:pk>/', views.MatchesBwTeamsRetrieveUpdateDelete.as_view(), name='matches-teams-list-retrieve-update-delete'),
	path('matches-results/create/list/', views.MatchResultCreateList.as_view(), name='matches-results-list'),
	path('matches-results/detail/<int:pk>/', views.MatchResultRetrieveUpdateDelete.as_view(), name='matches-results-list-retrieve-update-delete'),
	path('points-table/create/list/<int:pk>/', views.PointsTableList.as_view(), name='points-table-list'),
	path('country/list/', views.GetCountryList.as_view(), name='country-list'),
	path('team/dd/list/', views.GetTeamDDList.as_view(), name='team-dd-list'),
	]

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)



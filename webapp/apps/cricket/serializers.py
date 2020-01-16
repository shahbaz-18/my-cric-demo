from rest_framework import serializers
from . import models
from django.conf import settings
from django.db import transaction
import json
from django.db.models import Q, F



class CountrySerializer(serializers.ModelSerializer):
	"""
	Serializer to return List of Countries
	"""
	class Meta(object):
		model = models.Country
		fields = '__all__'


class TeamGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return list of Teams
	"""
	class Meta(object):
		model = models.Team
		fields = '__all__'


class TeamPostSerializer(serializers.ModelSerializer):
	"""
	Serializer to create a new Team
	"""
	class Meta(object):
		model = models.Team
		fields = '__all__'


class TeamDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of a particular Team
	"""
	class Meta(object):
		model = models.Team
		fields = '__all__'



class BattingHistorySerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of particular player batting history
	"""
	class Meta(object):
		model = models.BattingHistory
		fields = '__all__'


class BowlingHistorySerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of particular player bowling history
	"""
	class Meta(object):
		model = models.BowlingHistory
		fields = '__all__'


class PlayerGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return list of players
	"""
	class Meta(object):
		model = models.Player
		fields = '__all__'



class PlayerPostSerializer(serializers.ModelSerializer):
	"""
	Serializer to create and update new player as well as his batting and bowling history
	"""
	class Meta(object):
		model = models.Player
		fields = ('first_name', 'last_name', 'profile_image', 'jersey_num', 'country', 'is_active', 'team', 'batting_history', 'bowling_history')

	@transaction.atomic
	def create(self, validated_data):

		player_master = models.Player.objects.create(**validated_data)
		
		batting_history_data = validated_data.pop('batting_history')
		bowling_history_data = validated_data.pop('bowling_history')

		if batting_history_data:
			batting_history_data = json.loads(batting_history_data)
			models.BattingHistory.objects.create(   player = player_master,
													bt_match_played = int(batting_history_data['bt_match_played']),
													ball_faced = int(batting_history_data['ball_faced']),
													bt_run = int(batting_history_data['bt_run']),
													highest_score = int(batting_history_data['highest_score']),
													fifties = int(batting_history_data['fifties']),
													hundreds = (batting_history_data['hundreds']),
													bt_strike_rate = float(batting_history_data['bt_strike_rate']),
													bt_avgs = float(batting_history_data['bt_avgs'])
												)
		if bowling_history_data:
			bowling_history_data = json.loads(bowling_history_data[0])
			models.BowlingHistory.objects.create(
													player = player_master,
													bl_match_played = int(bowling_history_data['bl_match_played']),
													ball = int(bowling_history_data['ball']),
													bl_run = int(bowling_history_data['bl_run']),
													wicket = int(bowling_history_data['wicket']),
													best_bowling = str(bowling_history_data['best_bowling']),
													economy = float(bowling_history_data['economy']),
													bl_strike_rate = float(bowling_history_data['bl_strike_rate']),
													bl_avgs = float(bowling_history_data['bl_avgs'])
												)            
		return player_master

	@transaction.atomic
	def update(self, instance, validated_data):
		player_master, created = models.Player.objects.update_or_create(id=instance.id, defaults=validated_data)
		
		models.BattingHistory.objects.filter(player=player_master).delete()
		models.BowlingHistory.objects.filter(player=player_master).delete()

		batting_history_data = json.loads(validated_data.pop('batting_history'))
		bowling_history_data = json.loads(validated_data.pop('bowling_history'))

		if batting_history_data:
			models.BattingHistory.objects.create(   player = player_master,
													bt_match_played = int(batting_history_data['bt_match_played']),
													ball_faced = int(batting_history_data['ball_faced']),
													bt_run = int(batting_history_data['bt_run']),
													highest_score = int(batting_history_data['highest_score']),
													fifties = int(batting_history_data['fifties']),
													hundreds = int(batting_history_data['hundreds']),
													bt_strike_rate = float(batting_history_data['bt_strike_rate']),
													bt_avgs = float(batting_history_data['bt_avgs'])
												)
		if bowling_history_data:
			models.BowlingHistory.objects.create(
													player = player_master,
													bl_match_played = int(bowling_history_data['bl_match_played']),
													ball = int(bowling_history_data['ball']),
													bl_run = int(bowling_history_data['bl_run']),
													wicket = int(bowling_history_data['wicket']),
													best_bowling = str(bowling_history_data['best_bowling']),
													economy = float(bowling_history_data['economy']),
													bl_strike_rate = float(bowling_history_data['bl_strike_rate']),
													bl_avgs = float(bowling_history_data['bl_avgs'])
												)  
		return player_master


class PlayerDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of a particular Player with batting and bowling history
	"""
	country_list = serializers.SerializerMethodField()
	team_name = serializers.ReadOnlyField(source='team.name', allow_null=True, required=False) 

	class Meta(object):
		model = models.Player
		fields = ('first_name', 'last_name', 'profile_image', 'jersey_num', 'country', 'is_active', 'team', 'team_name', 'country_list', 'batting_history', 'bowling_history')

	def get_country_list(self, obj):
		country_data = []
		country_list = models.Country.objects.values('id', 'name').all()
		for data in country_list:
			country_data.append({'id':data['id'],
								'name':data['name']
								})
		return country_data



class SeriesGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of a particular Series
	"""
	team_list_per_series = serializers.SerializerMethodField()

	class Meta(object):
		model = models.Series
		fields = ('id', 'series_name', 'start_date', 'end_date', 'team_list_per_series')

	def get_team_list_per_series(self, obj):
		team_list = []
		team_list = models.TeamsPerSeries.objects.filter(series=obj).values_list('team_id__name', flat=True)
		return team_list


class SeriesPostSerializers(serializers.ModelSerializer):
	"""
	Serializer to save Series with team list of upcoming series
	"""
	team_list_for_series = serializers.CharField(write_only=True)
	
	class Meta(object):
		model = models.Series
		fields = ('series_name', 'start_date', 'end_date', 'team_list_for_series')

	@transaction.atomic
	def create(self, validated_data):
		team_list_data = validated_data.pop('team_list_for_series')

		series_master = models.Series.objects.create(**validated_data)
		
		if team_list_data:
			teams = team_list_data.rstrip('|').split('|')
			for team_id in teams:
				models.TeamsPerSeries.objects.create(   series = series_master,
														team_id = team_id
													)
		return series_master

	@transaction.atomic
	def update(self, instance, validated_data):
		team_list_data = validated_data.pop('team_list_for_series')
		series_master, created = models.Series.objects.update_or_create(id=instance.id, defaults=validated_data)
		
		models.TeamsPerSeries.objects.filter(series=series_master).delete()
		if team_list_data:
			teams = team_list_data.rstrip('|').split('|')
			for team_id in teams:
				models.TeamsPerSeries.objects.create(   
														series = series_master,
														team_id = team_id
													)
		return series_master



class MatchesBetweenTeamsGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return list or information of played matches
	"""
	class Meta(object):
		model = models.MatchesBetweenTeams
		fields = '__all__'


class MatchesBetweenTeamsPostSerializer(serializers.ModelSerializer):
	"""
	Serializer to save  a new Team
	"""
	class Meta(object):
		model = models.MatchesBetweenTeams
		fields = ('series', 'date_of_match', 'match_no', 'team1', 'team2', 'venue')


class MatchResultGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return list or information of a particular match result
	"""
	class Meta(object):
		model = models.MatchResult
		fields = '__all__'



class MatchResultPostSerializers(serializers.ModelSerializer):
	"""
	Serializer to save and update records after match results
	"""		
	class Meta(object):
		model = models.MatchResult
		fields = ('series', 'match', 'toss_winner', 'elected_to', 'match_winner', 'man_of_the_match')

	@transaction.atomic
	def create(self, validated_data):
		result_master = models.MatchResult.objects.create(**validated_data)
		
		if result_master:
			team_list = models.TeamsPerSeries.objects.filter(series=result_master.series)
			for team in team_list:
				models.PointsTable.objects.create(  series = result_master.series,
													team_id = team.id,
													match_played = models.MatchResult.objects.filter(Q(series=result_master.series), Q(match=result_master.match.team1) | Q(match=result_master.match.team2)).count(),
													match_won = models.MatchResult.objects.filter(Q(series=result_master.series), match_winner=team).count(),
													match_lost = F('match_played') - F('match_won'),													
													points = F('match_won') * 2,
													net_runrate = 1.00
												)
		return result_master

	@transaction.atomic
	def update(self, instance, validated_data):
		result_master, created = models.MatchResult.objects.update_or_create(id=instance.id, defaults=validated_data)
		
		models.PointsTable.objects.filter(series=result_master.series).delete()
		if result_master:
			team_list = models.TeamsPerSeries.objects.filter(series=result_master.series)
			for team in team_list:
				models.PointsTable.objects.create(  series = result_master.series,
													team_id = team.id,
													match_played = models.MatchResult.objects.filter(Q(series=result_master.series), Q(match=result_master.match.team1) | Q(match=result_master.match.team2)).count(),
													match_won = models.MatchResult.objects.filter(Q(series=result_master.series), match_winner=team).count(),
													match_lost = F('match_played') - F('match_won'),													
													points = F('match_won') * 2,
													net_runrate = 1.00
												)
		return result_master


class PointsTableGetSerializer(serializers.ModelSerializer):
	"""
	Serializer to return information of points table of a particular Series
	"""
	class Meta(object):
		model = models.PointsTable
		fields = '__all__'
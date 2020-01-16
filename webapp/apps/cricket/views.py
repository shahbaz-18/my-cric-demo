from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from . import models, serializers, utils, constants
from rest_framework.response import Response
from django.conf import settings
import requests
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt


class TeamCreateList(APIView):
	"""
	API to create Team and get Team list
	GET method is passed to get list of Teams
	POST method is passed to create a new Team
	"""
	def get(self, request):
		try:
			team_list = models.Team.objects.all()
		except models.Team.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.TeamGetSerializer(team_list, many=True)
		return render(request, 'cricket/team_list.html',{"data":serializer.data, "media_path":settings.BASE_URL}) 

	def post(self, request):
		try:
			team = models.Team.objects.get(name__iexact=request.data.get('name'))
			return utils.response({"error": constants.RECORD_ALREADY_EXISTS, "message": "error"}, status.HTTP_400_BAD_REQUEST)
		except models.Team.DoesNotExist:
			serializer = serializers.TeamPostSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return utils.response({"message": "success"}, status.HTTP_201_CREATED)
			return utils.response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


class TeamRetrieveUpdateDelete(APIView):
	"""
	API to retrieve, update or delete any Team
	:request param: id
	GET method is passed to retrieve Team information
	PUT method is passed to update Team information
	DELETE method is passed to delete a Team
	"""
	def get_object(self, pk):
		try:
			return models.Team.objects.get(pk=pk)
		except models.Team.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		team_data = self.get_object(pk)
		serializer = serializers.TeamDetailSerializer(team_data)
		return render(request, "cricket/edit_team.html", {"data":serializer.data, "media_path":settings.BASE_URL})

	@csrf_exempt
	def put(self, request, pk, format=None):
		team_data = self.get_object(pk)
		serializer = serializers.TeamPostSerializer(team_data, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return utils.response({" ": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		team_data = self.get_object(pk)
		team_data.delete()
		return utils.response({"message": "success"}, status.HTTP_204_NO_CONTENT)



class PlayerCreateList(APIView):
	"""
	API to create Player and get Player list
	GET method is passed to get list of Players
	POST method is passed to create a new Player
	"""
	def get(self, request):
		try:
			player_list = models.Player.objects.all()
		except models.Player.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.PlayerGetSerializer(player_list, many=True)
		# return Response({'result':serializer.data})
		return render(request, 'cricket/player_list.html',{"data":serializer.data, "media_path":settings.BASE_URL})

	def post(self, request):
		try:
			player = models.Player.objects.get(first_name__iexact=request.data.get('first_name'), last_name__iexact=request.data.get('last_name'))
			return Response({"error": constants.RECORD_ALREADY_EXISTS, "message": "error"}, status.HTTP_400_BAD_REQUEST)
		except models.Player.DoesNotExist:
			print(request.data['batting_history'])
			serializer = serializers.PlayerPostSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return utils.response({"message": "success"}, status.HTTP_201_CREATED)
			return utils.response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


class PlayerRetrieveUpdateDelete(APIView):
	"""
	API to retrieve, update or delete any Player
	:request param: id
	GET method is passed to retrieve Player information
	PUT method is passed to update Player information
	DELETE method is passed to delete a Player
	"""
	def get_object(self, pk):
		try:
			return models.Player.objects.get(pk=pk)
		except models.Player.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		player_data = self.get_object(pk)
		serializer = serializers.PlayerDetailSerializer(player_data)
		# return Response({'result': serializer.data, 'media_path': settings.BASE_URL})
		return render(request, "cricket/edit_player.html", {"data":serializer.data, "media_path":settings.BASE_URL})

	@csrf_exempt
	def put(self, request, pk, format=None):
		player_data = self.get_object(pk)
		serializer = serializers.PlayerPostSerializer(player_data, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return utils.response({"message": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		player_data = self.get_object(pk)
		serializer = serializers.PlayerPostSerializer(player_data, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return utils.response({" ": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		player_data = self.get_object(pk)
		player_data.delete()
		return utils.response({"message": "success"}, status.HTTP_204_NO_CONTENT)




class SeriesCreateList(APIView):
	"""
	API to create Series and get Series list
	GET method is passed to get list of Series
	POST method is passed to create a new Series
	"""
	def get(self, request):
		try:
			series_list = models.Series.objects.all()
		except models.Series.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.SeriesGetSerializer(series_list, many=True)
		return Response({'result':serializer.data})

	def post(self, request):
		try:
			series = models.Series.objects.get(series_name__iexact=request.data.get('series_name'))
			return Response({"error": constants.RECORD_ALREADY_EXISTS, "message": "error"}, status.HTTP_400_BAD_REQUEST)
		except models.Series.DoesNotExist:
			serializer = serializers.SeriesPostSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return utils.response({"message": "success"}, status.HTTP_201_CREATED)
			return utils.response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


class SeriesRetrieveUpdateDelete(APIView):
	"""
	API to retrieve, update or delete any Series
	:request param: id
	GET method is passed to retrieve Series information
	PUT method is passed to update Series information
	DELETE method is passed to delete a Series
	"""
	def get_object(self, pk):
		try:
			return models.Series.objects.get(pk=pk)
		except models.Series.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		series_data = self.get_object(pk)
		serializer = serializers.SeriesGetSerializerz(series_data)
		return Response({'result': serializer.data, 'media_path': settings.BASE_URL})

	def put(self, request, pk, format=None):
		series_data = self.get_object(pk)
		serializer = serializers.SeriesPostSerializer(series_data, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return utils.response({"message": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		series_data = self.get_object(pk)
		serializer = serializers.SeriesPostSerializer(series_data, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return utils.response({" ": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		series_data = self.get_object(pk)
		series_data.delete()
		return utils.response({"message": "success"}, status.HTTP_204_NO_CONTENT)


class MatchesBwTeamsCreateList(APIView):
	"""
	API to create Series and get Matches list
	GET method is passed to get list of Matches
	POST method is passed to create a new Matches
	"""
	def get(self, request):
		try:
			mbt_list = models.MatchesBetweenTeams.objects.all()
		except models.MatchesBetweenTeams.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.MatchesBetweenTeamsGetSerializer(mbt_list, many=True)
		return Response({'result':serializer.data})

	def post(self, request):
		try:
			series = models.MatchesBetweenTeams.objects.get(series_id=request.data.get('series_id'), match_no=int(request.data.get('series_id')))
			return Response({"error": constants.RECORD_ALREADY_EXISTS, "message": "error"}, status.HTTP_400_BAD_REQUEST)
		except models.MatchesBetweenTeams.DoesNotExist:
			serializer = serializers.MatchesBetweenTeamsPostSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return utils.response({"message": "success"}, status.HTTP_201_CREATED)
			return utils.response({"message": "error"}, status.HTTP_400_BAD_REQUEST)



class MatchesBwTeamsRetrieveUpdateDelete(APIView):
	"""
	API to retrieve, update or delete any Series
	:request param: id
	GET method is passed to retrieve Series information
	PUT method is passed to update Series information
	DELETE method is passed to delete a Series
	"""
	def get_object(self, pk):
		try:
			return models.MatchesBetweenTeams.objects.get(pk=pk)
		except models.MatchesBetweenTeams.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		mbt_data = self.get_object(pk)
		serializer = serializers.MatchesBetweenTeamsGetSerializer(mbt_data)
		return Response({'result': serializer.data, 'media_path': settings.BASE_URL})

	def put(self, request, pk, format=None):
		mbt_data = self.get_object(pk)
		serializer = serializers.MatchesBetweenTeamsPostSerializer(mbt_data, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return utils.response({"message": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		mbt_data = self.get_object(pk)
		serializer = serializers.MatchesBetweenTeamsPostSerializer(mbt_data, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return utils.response({" ": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		mbt_data = self.get_object(pk)
		mbt_data.delete()
		return utils.response({"message": "success"}, status.HTTP_204_NO_CONTENT)



class MatchResultCreateList(APIView):
	"""
	API to create Series and get Matches resultlist
	GET method is passed to get list of Matches results
	POST method is passed to save a new Matche result
	"""
	def get(self, request):
		try:
			mr_list = models.MatchResult.objects.all()
		except models.MatchResult.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.MatchResultGetSerializer(mr_list, many=True)
		return Response({'result':serializer.data})

	def post(self, request):
		try:
			series = models.MatchResult.objects.get(series_id=request.data.get('series_id'), match_id=int(request.data.get('match_id')))
			return Response({"error": constants.RECORD_ALREADY_EXISTS, "message": "error"}, status.HTTP_400_BAD_REQUEST)
		except models.MatchResult.DoesNotExist:
			serializer = serializers.MatchResultPostSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return utils.response({"message": "success"}, status.HTTP_201_CREATED)
			return utils.response({"message": "error"}, status.HTTP_400_BAD_REQUEST)



class MatchResultRetrieveUpdateDelete(APIView):
	"""
	API to retrieve, update or delete any Match Result
	:request param: id
	GET method is passed to retrieve Match Result information
	PUT method is passed to update Match Result information
	DELETE method is passed to delete a Match Result information
	"""
	def get_object(self, pk):
		try:
			return models.MatchResult.objects.get(pk=pk)
		except models.MatchResult.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		mr_data = self.get_object(pk)
		serializer = serializers.MatchResultGetSerializer(mr_data)
		return Response({'result': serializer.data, 'media_path': settings.BASE_URL})

	def put(self, request, pk, format=None):
		mr_data = self.get_object(pk)
		serializer = serializers.MatchResultPostSerializer(mr_data, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return utils.response({"message": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		mr_data = self.get_object(pk)
		serializer = serializers.MatchResultPostSerializer(mr_data, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return utils.response({" ": "success"}, status.HTTP_200_OK)
		return utils.response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		mr_data = self.get_object(pk)
		mr_data.delete()
		return utils.response({"message": "success"}, status.HTTP_204_NO_CONTENT)


class PointsTableList(APIView):
	"""
	API to get Points table of a Series
	"""
	def get(self, request, pk):
		try:
			pt_list = models.PointsTable.objects.filter(series_id=pk).all()
		except models.PointsTable.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.PointsTableGetSerializer(pt_list, many=True)
		return Response({'result':serializer.data})



class GetCountryList(APIView):
	"""
	API to get Country list
	"""
	def get(self, request):
		try:
			country_list = models.Country.objects.all()
		except models.Country.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.CountrySerializer(country_list, many=True)
		country_html = '<option value="">Select</option>'
		for item in serializer.data:
			country_id = item['id']
			name = item['name']
			country_html+='<option value="'+str(country_id)+'">'+str(name)+'</option>'
		return Response(country_html)


class GetTeamDDList(APIView):
	"""
	API to get Team list tp populate dropdown
	"""
	def get(self, request):
		try:
			team_list = models.Team.objects.all()
		except models.Team.DoesNotExist:
			return Response({'result':'No Record Found'})
		serializer = serializers.TeamGetSerializer(team_list, many=True)
		team_html = '<option value="">Select</option>'
		for item in serializer.data:
			team_id = item['id']
			name = item['name']
			team_html+='<option value="'+str(team_id)+'">'+str(name)+'</option>'
		return Response(team_html)

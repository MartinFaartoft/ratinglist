from api.models import *
from api.serializers import *
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

class PlayerList(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PlayerDetail(APIView):
    def get_object(self, pk):
        try:
            return Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        player = self.get_object(pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    def put(self, request, pk):
        player = self.get_object(pk)
        serializer = PlayerSerializer(player, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        game_players = GamePlayer.objects.filter(player_id=pk)
        if len(game_players) > 0:
            return Response(dict(detail='Cannot delete, player has played one or more games.'), status = status.HTTP_409_CONFLICT)

        player = self.get_object(pk)
        player.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class AllGamesList(APIView):
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request):
        games = Game.objects.all()
        serializer = GameViewSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameCreateSerializer(data = request.data)
        if serializer.is_valid():
            game = serializer.save()
            return Response(GameViewSerializer(game).data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class GamesOfTypeList(APIView):
    def get(self, request, game_type):
        games = Game.objects.filter(game_type = game_type)
        serializer = GameViewSerializer(games, many=True)
        return Response(serializer.data)

class RatingEntriesList(APIView):
    def get(self, request, pk, game_type):
        rating_entries = RatingEntry.objects.filter(player_id = pk).filter(game__game_type = game_type)
        for r in rating_entries:
            print(r.game)
        serializer = RatingEntrySerializer(rating_entries, many=True)
        return Response(serializer.data)

class RatingList(APIView):
    def get(self, request, game_type):
        ratinglist = RatingRepository().get_rating_list(game_type)
        serializer = RatingListSerializer(ratinglist, many=True)
        return Response(serializer.data)

class GameDetail(APIView):
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        game = self.get_object(pk)
        serializer = GameViewSerializer(game)
        return Response(serializer.data)

    def delete(self, request, pk):
        game = self.get_object(pk)
        r = RatingRepository()
        r.clear_rating_for_games_after(game)
        game.delete()
        r.rate_unrated_games()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        game = self.get_object(pk)
        serializer = GameCreateSerializer(instance=game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

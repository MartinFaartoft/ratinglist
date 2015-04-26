from api.models import *
from api.serializers import *
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

class PlayerList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
            return Response(status = status.HTTP_409_CONFLICT)

        player = self.get_object(pk)
        player.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.DATA['username']
        password = request.DATA['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(status = status.HTTP_302_FOUND)
        else:
            return Response("Invalid login", status = 401)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_200_OK)
        return response

class GamesList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
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
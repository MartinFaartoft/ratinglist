from api.models import Player, Game
from api.serializers import PlayerSerializer, GameSerializer
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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
        player = self.get_object(pk)
        player.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.DATA['username']
        password = request.DATA['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(status = status.HTTP_302_FOUND)
        else:
            return Response("Invalid login", status = 401)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_200_OK)
        return response

class GamesList(APIView):
    def get(self, request):        
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = GameSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
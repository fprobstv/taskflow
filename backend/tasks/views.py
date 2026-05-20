from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Board, Column, Task
from .serializers import BoardSerializer, ColumnSerializer, TaskSerializer
from django.db.models import Q
from django.contrib.auth.models import User

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(shared_with=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        board = self.get_object() 
        username = request.data.get('username')

        if not username:
            return Response({"error": "Digite um nome de usuário."}, status=status.HTTP_400_BAD_REQUEST)
        
        if username == request.user.username:
            return Response({"error": "Você já é o dono deste quadro!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            guest = User.objects.get(username=username)
            board.shared_with.add(guest)
            return Response({"message": f"Quadro compartilhado com {guest.username} com sucesso!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado. Verifique o nome digitado."}, status=status.HTTP_404_NOT_FOUND)

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
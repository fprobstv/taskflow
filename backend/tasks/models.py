from django.db import models
from django.contrib.auth.models import User
import redis
import json

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Column(models.Model):
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.Case)
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.board.name} - {self.title}"
    
class Task(models.Model):
    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        message = {
            "type": "task_update",
            "task_id": self.id,
            "column_id": self.column.id,
            "title": self.title
        }

        try:
            redis_client.publish('board_updates', json.dumps(message))
            print(f"Aviso enviado pro Redis: Tarefa {self.id} movida/criada!")
        except Exception as e:
            print(f"Erro ao concetar no Redis: {e}")
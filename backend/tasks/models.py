from django.db import models, transaction
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
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.board.name})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        message = {
            "type": "column_updated",
            "column_id": "column_id",
            "title": self.title
        }

        def send_to_redis():
            try:
                redis_client.publish('board_updates', json.dumps(message))
                print(f"Aviso enviado para o Redis: coluna {self.id} atualizada/criada!")
            except Exception as e:
                print(f"Erro ao conectar ao redis: {e}")
        
        transaction.on_commit(send_to_redis)

    def delete(self, *args, **kwargs):
        column_id = self.id
        super().delete(*args, **kwargs)
        
        message = {
            "type": "column_deleted",
            "column_id": column_id
        }
        
        def send_to_redis():
            try:
                redis_client.publish('board_updates', json.dumps(message))
                print(f"Aviso enviado pro Redis: Coluna {column_id} DELETADA!")
            except Exception as e:
                print(f"Erro ao conectar no Redis (Coluna Delete): {e}")

        transaction.on_commit(send_to_redis)


class Task(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        message = {
            "type": "task_updated",
            "task_id": self.id,
            "column_id": self.column.id,
            "title": self.title
        }
        
        def send_to_redis():
            try:
                redis_client.publish('board_updates', json.dumps(message))
                print(f"Aviso enviado pro Redis: Tarefa {self.id} movida/criada!")
            except Exception as e:
                print(f"Erro ao conectar no Redis (Tarefa Save): {e}")

        transaction.on_commit(send_to_redis)

    def delete(self, *args, **kwargs):
        task_id = self.id
        super().delete(*args, **kwargs)
        
        message = {
            "type": "task_deleted",
            "task_id": task_id
        }
        
        def send_to_redis():
            try:
                redis_client.publish('board_updates', json.dumps(message))
                print(f"Aviso enviado pro Redis: Tarefa {task_id} DELETADA!")
            except Exception as e:
                print(f"Erro ao conectar no Redis (Tarefa Delete): {e}")

        transaction.on_commit(send_to_redis)
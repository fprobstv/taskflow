package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true 
	},
}

var clients = make(map[*websocket.Conn]bool)

func main() {
	// 1. Conecta no Redis
	rdb := redis.NewClient(&redis.Options{
		Addr: "127.0.0.1:6379",
	})

	pubsub := rdb.Subscribe(ctx, "board_updates")
	defer pubsub.Close()

	go func() {
		ch := pubsub.Channel()
		for msg := range ch {
			fmt.Println("📢 Recebido do Redis:", msg.Payload)
			
			for client := range clients {
				err := client.WriteMessage(websocket.TextMessage, []byte(msg.Payload))
				if err != nil {
					client.Close()
					delete(clients, client)
				}
			}
		}
	}()

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println("Erro no upgrade do WebSocket:", err)
			return
		}
		clients[conn] = true
		fmt.Println("🟢 Novo cliente Vue conectado!")
	})

	fmt.Println("🚀 Servidor Golang rodando na porta 8081...")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
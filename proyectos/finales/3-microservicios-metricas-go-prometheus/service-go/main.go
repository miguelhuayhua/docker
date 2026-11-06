package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

type StatusResponse struct {
	Service   string    `json:"service"`
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
	UptimeSec int64     `json:"uptime_seconds"`
}

var startTime = time.Now()

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		resp := StatusResponse{
			Service:   "Go Microservice Engine",
			Status:    "Healthy",
			Timestamp: time.Now(),
			UptimeSec: int64(time.Since(startTime).Seconds()),
		}
		json.NewEncoder(w).Encode(resp)
	})

	// Endpoint de métricas estándar OpenMetrics/Prometheus
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprintf(w, "# HELP go_service_uptime_seconds Seconds since startup\n")
		fmt.Fprintf(w, "# TYPE go_service_uptime_seconds counter\n")
		fmt.Fprintf(w, "go_service_uptime_seconds %d\n", int64(time.Since(startTime).Seconds()))
		fmt.Fprintf(w, "# HELP go_service_requests_total Total requests served\n")
		fmt.Fprintf(w, "# TYPE go_service_requests_total counter\n")
		fmt.Fprintf(w, "go_service_requests_total 42\n")
	})

	log.Printf("Microservicio Go escuchando en :%s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Error en servidor: %v", err)
	}
}

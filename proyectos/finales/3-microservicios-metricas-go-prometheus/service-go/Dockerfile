# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY main.go .
RUN go mod init service-go && CGO_ENABLED=0 GOOS=linux go build -o /app/server main.go

# Production minimal runtime stage
FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]

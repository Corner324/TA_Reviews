# Makefile для сервиса анализа сентимента отзывов

.PHONY: help build run stop clean logs shell

# Цель по умолчанию
help:
	@echo "Available commands:"
	@echo "  build  - Build Docker image"
	@echo "  run    - Run container"
	@echo "  stop   - Stop container"
	@echo "  clean  - Remove container and image"
	@echo "  logs   - Show container logs"
	@echo "  shell  - Open shell in running container"

# Сборка образа
build:
	docker-compose build

# Запуск контейнера
run:
	docker-compose up -d
	@echo "Server running at http://localhost:8000"
	@echo "API documentation: http://localhost:8000/docs"

# Остановка контейнера
stop:
	docker-compose down

# Очистка
clean:
	docker-compose down -v --rmi all

# Показать логи
logs:
	docker-compose logs -f

# Открыть shell
shell:
	docker-compose exec reviews-sentiment /bin/bash
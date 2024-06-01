Dockerfile: докерфайл для app сервиса

docker-compose: init - celery + redis + app + postgres

.env: переменные по типу логин \ пароль

1. Ограничивать ресурсы можно с помощью mem_limit, cpus, resources
2. Например, командой docker compose up db для поднятия постгреса в моем случае 
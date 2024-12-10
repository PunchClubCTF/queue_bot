FROM postgres:15

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /docker-entrypoint-initdb.d/

# Копируем SQL файл для инициализации базы данных
COPY tables.sql /docker-entrypoint-initdb.d/tables.sql

# Устанавливаем стандартный порт PostgreSQL
EXPOSE 5432

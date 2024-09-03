# Бот @chelonco174_bot

## Как запустить сборку на сервере:  
В папке должны находиться: requirements.txt, .env, docker-compose.yml, Dockerfile.  
Команды для запуска (находясь в директории с docker-compose.yml)


## Команды (находясь в папке с docker-compose файлом)
1. #### Создание и запуск контейнеров:
   ```bash
   sudo docker-compose up
   ```
2. #### Остановка и удаление контейнеров:
   ```bash
   sudo docker-compose down
   ```
3. #### Сборка образов без запуска:
   ```bash
   sudo docker-compose build
   ```
4. #### Запуск созданных контейнеров:
   ```bash
   sudo docker-compose start
   ```
5. #### Остановка контейнеров без удаления:
   ```bash
   sudo docker-compose stop
   ```
6. ### Остановка и удаление контейнеров вместе с образами
   ```bash
   docker-compose down --rmi all
   ```
7. ### Остановка и удаление контейнеров вместе с образами и связными томами
   ```bash
   docker-compose down -v --rmi all
   ```
8. #### Перезапуск контейнеров:
   ```bash
   sudo docker-compose restart
   ```
9. #### Запуск команды внутри контейнера:
   ```bash
   sudo docker-compose exec
   ```
10. #### Просмотр логов всех или определенных контейнеров:
   ```bash
   sudo docker-compose logs
   ```
## Как обновить контейнер при изменениях в master

1. ### Заходим в контейнер и спуливаем изменения
   ``` bash
    sudo docker exec -it telegram_bot bash
   ```
   ``` bash
    git pull
   ```
2. ### Выходим из контейнера
   Ctrl+P+Q
3. ### Ребутаем контейнер
   ``` bash
    sudo docker restart telegram_bot
   ```
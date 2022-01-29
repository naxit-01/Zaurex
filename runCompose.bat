set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p Zaurex up -d --build
pause
docker-compose -p Zaurex down
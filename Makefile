.PHONY: up
up:
	    docker compose up --build

.PHONY: down
down:
		docker-compose down --rmi all

.PHONY: deploy
deploy:
		git push heroku main

.PHONY: log
log:
		heroku logs --tail
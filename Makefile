.PHONY: up
up:
	    docker compose up --build

.PHONY: down
down:
		docker-compose down --rmi all

.PHONY: exec
exec:
	    docker compose exec web bash

.PHONY: deploy
deploy:
		git push heroku main

.PHONY: log
log:
		heroku logs --tail

#git push heroku <現在いるブランチ名>:master
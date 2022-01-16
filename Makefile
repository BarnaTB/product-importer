build:
	docker-compose build
up:
	docker-compose up
down:
	docker-compose down
migrate:
	docker-compose run app python manage.py migrate
migrations:
	docker-compose run app python manage.py makemigrations
test:
	docker-compose run app python manage.py test $(APP)

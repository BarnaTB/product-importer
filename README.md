[![BarnaTB](https://circleci.com/gh/BarnaTB/product-importer.svg?style=shield)](https://circleci.com/gh/BarnaTB/product-importer)  [![Maintainability](https://api.codeclimate.com/v1/badges/15df0093a42d8012885a/maintainability)](https://codeclimate.com/github/BarnaTB/product-importer/maintainability)  [![Coverage Status](https://coveralls.io/repos/github/BarnaTB/product-importer/badge.svg?branch=main)](https://coveralls.io/github/BarnaTB/product-importer?branch=main)

# product-importer
This is the backend service that enables a user to add a product to the database by filling a form, or uploading a csv file to upload a batch of products.

## Getting Started
The product is built on the following stack:

* Python 3.8
* Celery
* RabbitMQ
* PostgreSQL
* Virtualenv

Ensure you have Docker and Make installed and running prior to the steps that follow.

## Installing

Run the commands below in your terminal to clone and setup the project

```shell
# clone the project
$ git clone https://github.com/BarnaTB/product-importer.git

# open the project directory
$ cd product-importer

# checkout to this branch
$ git checkout dockerize-backend-service

# build the project and all its dependencies
$ make build

# run the application
$ make up
```

The project should be ready to run now so run `python manage.py runserver` and hit the endpoints according to the [documentation here](https://fulfilproductimporter.herokuapp.com/api/v1/docs/).

## Running the tests
Run the tests by running `make test` or `make test APP=<insert-app-name>` to run app specific tests

## Deployment

The backend is deployed on Heroku [here](https://fulfilproductimporter.herokuapp.com) while the frontend project is deployed [here](https://fulfillproductimporter.herokuapp.com).

## Acknowledgements

Kudos to the team at [Fulfil.io](https://fulfil.io) for their unmatched support during the development of this project.

# RidingCoachApp 
_Web application for motorcycle riders to organize maintenance, spare parts, and bike setups._

![RidingCoach Logo](/frontend/public/favicon.svg "RidingCoach Logo")

## Demo (dev)

[Live Demo](https://riding-coach-demo.herokuapp.com/)

## Application Structure

### Rest Api

The Api is served by a Flask blueprint at `/api/` using Flask RestPlus class-based resource routing and documented by Swagger.

### Client Application

A Flask view is used to serve the `index.html` as an entry point into the Vue app at the endpoint `/`.

The Vue instance is configured with Vue-router to map the instances, Vuex to store variables used globally, and the material design component framework Vuetify.

### Important Files

| Location                 |  Content                                   |
|--------------------------|--------------------------------------------|
| `/backend`               | Flask Application                          |
| `/backend/api`           | Flask Rest Api                             |
| `/backend/wsgi.py`       | Flask WSGI                                 |
| `/frontend/src`          | Vue App .                                  |
| `/frontend/src/main.js`  | JS Application Entry Point                 |

## Requirements
* npm - [instructions](https://www.npmjs.com/get-npm)
* Vue Cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
* Python 3 - [instructions](https://www.python.org/downloads/)
* Pipenv (optional)
* Heroku Cli (if deploying to Heroku)

Installation and deployment guide will be provided with alpha release.

## Acknowledgments

* Flask and Vue template by [@gtalarico](https://github.com/gtalarico) - [template](https://github.com/gtalarico/flask-vuejs-template)
* RestPlus template by [@postrational](https://github.com/postrational) - [template](https://github.com/postrational/rest_api_demo)

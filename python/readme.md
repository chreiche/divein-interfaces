# Build Docker images

# docker login
You might need to login to docker (since in the Deloitte net there are too many requests)

create an account at https://hub.docker.com and then login with

    docker login

## python

### python dev
    docker build --target dev . -t divein-python-dev

    docker run -it -v ${PWD}:/work divein-python-dev

#### run application in dev container
    gunicorn --reload src.app

### python app
    docker build --target runtime . -t divein-python

    docker run --rm -p 8000:8000 divein-python


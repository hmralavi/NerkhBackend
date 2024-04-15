# NerkhBackend
- Backend for Nerkh application

- python 3.9.19

- Redis database indexes considered for this project:\
    0: main\
    1: development\
    2: testing

## Instruction to run on your local machine (Ubuntu)
 
 1. install redis on ubuntu:

    follow instructions to install redis server:

    https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/

    start redis server:

    ```bash
    sudo systemctl start redis
    ```
2. Navigate into repo's root folder:
    ```bash
    cd path/to/NerkhBackend
    ```
3. create a file named ".env" and insert contents to it similar to the ".env-template".

4. create a python virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source ./.venv/bin/activate
    ```
5. upgrade pip & install dependencies:
    ```bash
    python3 -m pip install pip --upgrade
    python3 -m pip install -r requirements.txt
    ```

6. navigate to src folder and run the app via uvicorn:
    ```bash
    cd src
    uvicorn app:app --host="0.0.0.0" --port="10000" --reload
    ```
7. the app should be running on the following address:

    `http://0.0.0.0:10000`


## Instruction to run with Docker

- instead of installing redis and python to run the app on your system, you can just use docker.

- navigate to NerkhBackend folder and create a file named `.env` and insert contents to it similar to the `.env-template`.

- then run:
    ```bash
    sudo docker compose up
    ```

- the app should be running on the following address:

    `http://0.0.0.0:10000`

## Deploy to Liara

- I have considered twp apps on liara: nerkh-api, nerkh-api-dev.\
we deploy main branch to the first one and the development branch to the second one.

- the deployment workflow `.github/workflows/test-deploy.yaml` is handled by github actions.\
However, you must add environmental variables as described in `.env-template` file into liara's panel manually.

- in order to deploy using github actions, you need to create a liara token and store it in the repository secret keys with this name:`LIARA_API_TOKEN`

## Submit data to the server (mainly for the "bonbast" data)

- Since bonbast is not reachable by liara server, We can use github actions as a cronjob to submit bonbast's data into our database.

- the workflow `.github/workflows/cronjob.yaml` will run every 15 minutes and gets bonbast's data and submits them into our server.

- the workflow runs `data_submitter/main.py` to get and submit data.

- this solution is mainly made for bonbast data but it can be used for other sources too.


**Important**: 

You need a token to be able to submit prices to the server.

1. How to get the token?

    - go to NerkhBackend's cmd line from liara panel.

    - run:
        ```bash
        python authencitation_tools.py
        ``` 
    - enter a name and hit enter. you'll get a token. copy it.

    - if no token generated, maybe it's because you have not defined the `SECRET_KEY` environmental variable in the liara's panel. make sure you have defined this variable.

2. where to save the token?

    - you should save the received token into a repository_secret variable at this current github repository with name: `NERKH_TOKEN`.

    - As a result, the github action can read the token and submit the prices to the server.

# shore-app-demo
This is a test project - 
 - service to manage alerts for products prices on Ebay.com, the service will allow a user
to create an alert so he can receive updates about specific products search phrases delivered to
his email address.
- Let user know the product insights according to search results.

## Configuration 
By default it will have the [DefaultConfig](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L20-L53) and for test runner it will use [TestConfig](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L56-L63)
  - For Email Setup, `username` and `password` is required. You can use your gmail credentials but you need to change your Gmail [security settings](https://kb.synology.com/en-global/SRM/tutorial/How_to_use_Gmail_SMTP_server_to_send_emails_for_SRM)
  - If you want to test the app without using the [Email notification](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L27), set `SENT_EMAIL=False`
  - We used `Celery` for task runner with multiple queue. To change the schedule time, here is the [options](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L38-L39)
  - [Ebay APP](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L51) Id is required, but use mine for test purpose.   

## Docker-Configuration
  - To run the project from docker, run command - `docker-compose up --build` for the first time
  - For later use only - `docker-compose up`
  - For details check [docker-compose](https://github.com/pranto157/shore-app-demo/blob/main/docker-compose.yaml) and [DockerFile](https://github.com/pranto157/shore-app-demo/blob/main/Dockerfile)

## Test Runner
  - To check tests - `docker exec  -it shore-app pytest`
## Run Project

  - `docker-compose up --build` or `docker-compose up`
    #### Single Page WebApp
  - `http://127.0.0.1:5000/` 
    #### API
      - Use postman or any other client to test the API
      - Resources - 
        - `/api/users` [GET, POST]
        - `/api/user/:id` [EDIT, PUT, DELETE]
        - `/api/subscriptions` [GET, POST]
        - `/api/subscription/:id` [GET, PUT, DELETE]  

## Debug
  - Turn on [debug mode](https://github.com/pranto157/shore-app-demo/blob/main/shore_app/config.py#L22), set `DEBUG=True` 
  - docker logs - `docker logs -f [container-name]`
  - Log file in `/var/log/shore_app` directory, using LogRotation. 

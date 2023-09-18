# Chatflow

Chatflow offers a chat interface for users to interact with any system using natural language.
Our engine understands the user's intent and executes the required
commands for the given task.

Users can easily navigate and utilize complex websites/products with multiple pages and
functionalities through a chat interface rather than using a point-and-click
approach.

This leads to decreased training expenses, enhanced user experience, and improved
productivity.

You can try it out [here](http://apps.newaisolutions.com/)

Watch [this video](https://youtu.be/S_-6Oi1Zq1o?si=7TwD9pZq47uFMf1) to learn more.

<img src="declarative-imperative.png">

## Running the App
Before running the app, please install Docker first

## Set up the environment(Windows only)

### Automatic Setup:
- `cd scripts`
- `.\windows-utils.ps1 -action setup -apiKey [OpenAI API Key]`

### Starting the App
- `.\windows-utils.ps1 -action on`

### Stopping the App
- `.\windows-utils.ps1 -action off`


## Manual setup:

### React UI
- `cd chat-ui`
- `npm install`
- `npm run build`
- `npm start`

### Backend

- Start the databases
    ```bash
    $ docker-compose up -d redis postgres
    ```
- Install the dependencies
    ```bash
    $ pip install -r requirements-dev.txt
    ```
- Navigate to the backend src cod 
    ```bash
    $ cd server/src
    ```
  
- Create a .env file and set all required variables
    ```bash
    cp .env.template .env
    ```
- Replace the OpenAI API key with your own key in the .env file
  
- Start the backend service locally
    ```bash
   $ python load_data.py
   $ python server.py
    ```
  
- Log into the app http://localhost:3000/assets#/login with the following credentials
    ```bash
    username: admin@gmail.com
    password: 123
    ```
- Visit http://localhost:8880/api/docs to see the API docs
- Access the Redis Vector DB UI on http://localhost:8001/redis-stack/browser

## Local Development with Docker
- Build the docker image `docker build -t apssouza/chatux:latest .`
- Set OPENAI_API_KEY_GPT4 and OPENAI_API_KEY_GPT3 environment variables
- Run `docker-compose up` to start the app
- Visit http://localhost:8880/api/docs to see the API docs


## Backlog
Please look at the issues for the backlog

## Leave a star if you like the project

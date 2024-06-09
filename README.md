# Chatflow

Chatflow offers a chat interface for users to interact with any system using natural language.
Our engine understands the user's intent and executes the required
commands for the given task.

Users can easily navigate and utilize complex websites/products with multiple pages and
functionalities through a chat interface rather than using a point-and-click
approach.

You can try it out [here](http://apps.newaisolutions.com/)

Watch [this video](https://youtu.be/S_-6Oi1Zq1o?si=7TwD9pZq47uFMf1) to learn more.

Join our Discord to know what's going on in development and to ask questions to the maintainers about the project and how to contribute: https://discord.gg/fJ5ecMmsSf

<img src="assets/declarative-imperative.png" width="500">

## RAG architecture
<img src="assets/rag-flow.png" width="800">

## Running the App
Before running the app, please install Docker first

## Set up the environment

### Backend

- Start the databases
    ```bash
    docker-compose up -d redis
    ```
- Install the dependencies
    ```bash
    pip install -r requirements-dev.txt
    ```
- Navigate to the backend src cod 
    ```bash
    cd server/src
    ```
  
- Create a .env file and set all required variables
    ```bash
    cp server/src/.env.template server/src/.env
    ```
- Replace the OpenAI API key with your own key in the .env file
  
- Start the backend service locally
    ```bash
  # Load the initial data
   python load_data.py
  # Start the server
   python server.py
    ```
  
- Log into the app http://localhost:3000/assets#/login with the following credentials
    ```bash
    username: admin@gmail.com
    password: 123
    ```
- Visit http://localhost:8880/api/docs to see the API docs
- Access the Redis Vector DB UI on http://localhost:8001/redis-stack/browser


## Github demo
- Go to Github and create a new classic token https://github.com/settings/tokens
- Set the Github Token in the local storage of the browser
```
localStorage.setItem("external-token", "github-token")
localStorage.setItem("external-url", "github.com")
```
- Prompt the Github related actions. Ex List Github repositories and display as a chart with the fields: full_name and forks_count



## Backlog
Please look at the issues for the backlog

## Leave a star if you like the project

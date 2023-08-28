# Chatflow

You can ask anything about our project and our github repo directly in our user interface: 

http://apps.newaisolutions.com/

It will teach you how to run the app locally, answer any questions about our codebase and guide you in contributing to the repo. 
It can be a great tool for onboarding new developers.

Chatflow is a tool to help the integration of natural language capabilities in any web system,
making them more accessible and user-friendly for everyone.

Chatflow offers a chat interface for users to interact with any system using natural language.
Our engine understands the user's intent and executes the required
commands for the given task.

Users can easily navigate and utilize complex websites/products with multiple pages and
functionalities through a chat interface rather than using a point-and-click
approach.

This leads to decreased training expenses, enhanced user experience, and improved
productivity.

<img src="declarative-imperative.png">

## Running the App
Before running the app, please install Docker first.

## React UI
- `cd chat-ui`
- `npm install`
- `npm run build`
- `npm start`

## Backend

- Start the databases
    ```bash
    $ docker-compose up -d redis postgres
    ```

- Navigate to the backend src cod 
    ```bash
    $ cd server/src
    ```
  
- Create a .env file and set all required variables
    ```bash
    cp .env.template .env
    ```
  
- Start the backend service locally
    ```bash
   $ python load_data.py
   $ python server.py
    ```
  
- Visit http://localhost:8880/api/docs to see the API docs
- Access the Redis Vector DB UI on http://localhost:8001/redis-stack/browser
- Optional - For Github integration set the github token in the localStorage.setItem('github-token', 'your token')  



### Local Development with Docker
- Build the docker image `docker build -t apssouza/chatux:latest .`
- Run `docker-compose up` to start the app or `docker run -p 8880:8880 apssouza/chatux:latest` to run the container
- Visit http://localhost:8880/api/docs to see the API docs


## Backlog
Please look at the issues for the backlog

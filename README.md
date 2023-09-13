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

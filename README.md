# Chatflow

ChatUX is a tool to help the integration of natural language capabilities in any web systems,
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

### Local Development

- Ensure you set the following environment variables
    ```bash
    OPENAI_API_KEY_GPT3=YOUR_API_KEY
    OPENAI_API_KEY_GPT4=YOUR_API_KEY
    ```

- Start the vector-db
    ```bash
    $ docker-compose up -d redis-vector-db
    ```

- Create python virtual env. If mac m1, run `arch -x86_64 zsh` before the following commands 
    ```bash
   $ python -m pip install --upgrade pip
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements-dev.txt
    ```
  
- Start the backend service
    ```bash
   $ arch -x86_64 zsh
   $ source venv/bin/activate
   $ cd server/src
   $ python load_data.py
   $ python server.py
    ```
  
- Visit http://localhost:8880/api/docs to see the API docs
- Access the Redis Vector DB UI on http://localhost:8001/redis-stack/browser
- Optional - For Github integration set the github token in the localStorage.setItem('github-token', 'your token')  


## React UI
- `cd chat-ui`
- `npm install`
- `npm start`


### Local Development with Docker
- Build the docker image `docker build -t apssouza/chatux:latest .`
- Run `docker-compose up` to start the app or `docker run -p 8880:8880 apssouza/chatux:latest` to run the container
- Visit http://localhost:8880/api/docs to see the API docs


## Backlog
Please look at the issues for the backlog
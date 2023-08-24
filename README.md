# Simple Voting Application

This is a basic example of a voting application using Python (Flask), Redis for caching, and PostgreSQL for data storage. The application allows users to vote for their favorite option and view the voting results.

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose

## Getting Started

1. **Clone this repository to your local machine:**

   ```bash
   git clone https://github.com/yourusername/voting-app.git
   cd voting-app
2. **Build and push the Docker images to Docker Hub:**

   ```bash
   # Log in to Docker Hub
   docker login
   
   # Build and tag the images
   docker-compose build
   
   # Push the images to Docker Hub
   docker-compose push
3. **Update the Docker Compose configuration:**
   
   Open the docker-compose.yml file and replace <docker_hub_username> with your Docker Hub username.
4. **Start the application containers using Docker Compose:**
   ```bash
   docker-compose up
5. **Access the application in your web browser:**
   ```bash
   Voting Page: http://localhost:5000/
   Results Page: http://localhost:5001/result

## Usage

Visit the voting page (http://localhost:5000/) and vote for your favorite option.
Click on the "See Results" link to view the current voting results.

## Cleanup

   To stop and remove the containers, press Ctrl + C in the terminal where you started Docker Compose. Then, run:
      
      docker-compose down

## Customize

Feel free to customize and expand this application to match your requirements. You can modify the HTML templates, add more options, enhance security, and integrate additional features.

## Credits

This voting application is a simple example created for educational purposes.

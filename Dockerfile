# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5010

# # Define environment variable for Flask to run in production mode
# ENV FLASK_ENV=production

# Run the application
CMD ["python", "worker.py"]

# using a Python base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install Flask

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable
ENV SERVER_ID=1

# Command to run the Flask server
CMD ["python", "server.py"]

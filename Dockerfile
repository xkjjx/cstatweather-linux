# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt /app/requirements.txt
COPY files /app/files
COPY src /app/src

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir git+https://github.com/Zulko/moviepy.git


# Run app.py when the container launches
CMD ["python", "/app/src/main.py"]

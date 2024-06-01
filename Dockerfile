# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app directory contents into the container at /app
COPY app /app

# Copy the output directory into the container at /app/output
COPY output /app/output

# Make the specified port available to the world outside this container
EXPOSE 3000

# Declare the 'output' directory as a volume
VOLUME /app/output

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run main.py when the container launches
CMD ["python", "/app/main.py"]

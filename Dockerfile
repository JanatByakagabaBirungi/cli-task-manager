FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY task_manager.py .

# Create an empty JSON file to prevent errors on the first run
RUN echo "[]" > tasks.json

# Set the entrypoint to Python to pass arguments directly
ENTRYPOINT ["python", "task_manager.py"]
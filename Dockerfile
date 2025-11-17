# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install uv first
RUN pip install uv

# Install the dependencies
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
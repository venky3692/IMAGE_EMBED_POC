# Use the official Python image as a base
FROM python:3.9

# Set the working directory in the container
WORKDIR /backend

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "index.py"]

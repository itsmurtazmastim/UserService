# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application source code to the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Define the command to start the Flask app
CMD ["python", "app.py"]

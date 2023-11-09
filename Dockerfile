# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application source code to the container
COPY ./code /code/

# Expose the port your Flask app runs on
CMD ["uvicorn", "userservice.main:app", "--host", "0.0.0.0", "--port", "80"]


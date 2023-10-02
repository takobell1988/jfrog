# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#RUN apt-get install libpq-dev
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME test

# Run postgribbit.py (or the appropriate script)
CMD ["python", "postgribbit.py"]

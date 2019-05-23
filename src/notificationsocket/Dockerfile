# Use an official Python runtime as a parent image
FROM python:3.7.3

# Set the working directory to /app
WORKDIR /notificationsocket

# Copy the current directory contents into the container at /app
COPY . /notificationsocket

# Install any needed packages specified in requirements.txt
RUN make /notificationsocket
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
# Make port 80 available to the world outside this container
EXPOSE 8888

# Run app.py when the container launches
CMD python3 notifications.py

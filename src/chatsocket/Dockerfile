# Use an official Python runtime as a parent image
FROM python:3.7.3

# Set the working directory to /app
WORKDIR /chatsocket

# Copy the current directory contents into the container at /app
COPY . /chatsocket

# Install any needed packages specified in requirements.txt
RUN make /chatsocket
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
# Make port 80 available to the world outside this container
EXPOSE 8888

# Run app.py when the container launches
CMD python3 chatWebSocket.py



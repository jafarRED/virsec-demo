FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update -y &&  apt install awscli -y
RUN aws configure set aws_access_key_id "xxxxxxxxxxxx" \
    && aws configure set aws_secret_access_key "xxxxxxxxxxxxxxxxxxxxxxxx" \
    && aws configure set region ap-south-1
# Run the command to start the application
#CMD ["python", "./consumer.py"]
#CMD ["/bin/bash"]
CMD [ "python", "/app/consumer-app.py"]
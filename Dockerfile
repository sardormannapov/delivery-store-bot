# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app
ENV TZ="Asia/Tashkent"
# Copy the requirements file into the container
COPY requirements.txt .

# RUN pip3 install --no-cache-dir pip==23.1.2
# Install the required Python packages

RUN pip install --upgrade setuptools

RUN pip install --upgrade pip
#RUN pip3 install -e .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY . .

# Specify the command to run your bot when the container starts
CMD ["python", "bot.py"]

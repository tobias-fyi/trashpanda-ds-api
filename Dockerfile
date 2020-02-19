# Use Alpine-based Python base image
FROM python:3.8.0-alpine

# Create + set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Set envirovars
# Prevent pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents buffering stdout and sdterr
ENV PYTHONUNBUFFERED 1

# Add and install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add app
COPY . .

# Run the Flask dev server
CMD python manage.py run -h 0.0.0.0

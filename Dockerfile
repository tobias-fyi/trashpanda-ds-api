# Use Alpine-based Python base image
FROM python:3.8.0-alpine

# Install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd && \
    # Pillow dependencies
    apk add jpeg-dev zlib-dev

# Set envirovars
# Prevent pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents buffering stdout and sdterr
ENV PYTHONUNBUFFERED 1

# Create + set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add and install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Add app
COPY . /usr/src/app

# Run the Flask dev server
CMD python manage.py run -h 0.0.0.0

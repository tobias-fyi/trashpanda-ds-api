# Trash Panda Object Detection API

A Flask REST API to receive image data, run it through an object detection model, and send back the appropriate prediction(s).

## Overview

The core of the API is built on `Flask` and `Flask-RESTPlus`, containerized using docker and docker-compose, and deployed to Heroku. The app is connected to a Postgres database to manage the materials data, which is queried using `Flask-SQLAlchemy`.

A relatively simple image read/write package `imageio` is used to convert base64-encoded images into numpy arrays, which will be fed directly into the object detection model once it's deployed.

## Usage

Currently, when the proper request is made to the API, the app picks a cluster at random from the database and serves that as if it were a prediction. The "predicted" cluster is returned along with the list of materials that make it up.

### Object Detection

The primary object detection route accepts _only_ POST requests:

    https://gentle-mesa-73091.herokuapp.com/detect

The POST request should be `JSON`, formatted as follows:

```json
{
    "imgb64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAjcAAAOWCA..."
}
```

> Note: in this example, the base64-encoded image string has been truncated. A valid base64 string will likely be hundreds of thousands of characters in length.

### Database Queries

There are also 2 routes that accept GET requests and query the database accordingly.

> List of all materials

    https://gentle-mesa-73091.herokuapp.com/clusters

> Materials list for each cluster

    https://gentle-mesa-73091.herokuapp.com/clusters/<cluster>

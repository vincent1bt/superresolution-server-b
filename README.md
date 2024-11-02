# Infrastructure to Serve Deep Learning Models Using the Publish–Subscribe Pattern (Server B)

This repository contains the code to create an Infrastructure to serve Deep Learning models

To build this infrastructure, Django and Celery are used along with RabbitMQ and TensorFlow. However, these tools can be replaced, for instance, Pytorch can be used instead of TensorFlow, or FastAPI instead of Django, Celery is harder to replace but not impossible. 

This infrastructure is divided into two different servers, Server A and Server B. Server A receives the requests from users, and Server B serves the Deep Learning model.

In this repository, you can find the code for Server B (Celery, TensorFlow, Docker), and in [this additional repository](https://github.com/vincent1bt/superresolution-server-a) the code for Server A (Django, Celery).

Inside the *app/models** folder you can find two different models, *gan_model* can be used to test the infrastructure without any GPU, this model only transforms color images to black and white images.  *ema_gan_model* is the main model used when a GPU can be attached to the Server B instance.

Celery allows us to use the Publish-Subscribe Pattern to communicate Server A and Server B. A more detailed explanation can be found in [this blog post](https://vincentblog.link/posts/serving-deep-learning-models-using-the-publish-subscribe-pattern).

![infrastructure preview](https://res.cloudinary.com/vincent1bt/image/upload/c_scale,w_916/v1643836568/tf_server_app/Screen_Shot_2022-01-30_at_17.15.11.jpg)

FROM tensorflow/tensorflow:2.7.0-gpu

COPY app/requirements.txt /usr/src

WORKDIR /usr/src/

RUN pip3 install -r requirements.txt

COPY app /usr/src

ENV CELERY_BROKER=pyamqp://serverArabbituser:myrabbitsuperpw@ip:5672

EXPOSE 5672

CMD ["celery", "-A", "remote", "worker", "--pool=solo", "-Q", "images", "-l", "info", "--without-heartbeat"]
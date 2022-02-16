import os

from celery import Celery, shared_task
from celery.signals import worker_ready    

from utils import GCloudStorage
from inference import TFInference

broker_url = os.environ.get('CELERY_BROKER', '')

app = Celery('superresolution', broker=broker_url)
app.conf['worker_prefetch_multiplier'] = 1
app.conf['task_acks_late'] = True
app.conf['timezone'] = 'UTC'
app.conf['broker_heartbeat'] = 0

tf_inference = None
g_storage = None

"""
Local Tasks
"""

@shared_task(queue='images')
def run_sr_task(task_id, zip_id):
    g_storage.create_local_folders(zip_id)
    g_storage.download_images(zip_id)

    tf_inference.run_inference(zip_id)

    g_storage.upload_images(zip_id)

    # Logger

    app.send_task('tasks.tasks.task_finished', [task_id], queue='default')

"""
Remote Tasks
"""

@worker_ready.connect
def notify_server_created(sender, **kargs):
    server_name = os.environ.get('SERVER_NAME', '')

    global tf_inference
    tf_inference = TFInference()

    global g_storage
    g_storage = GCloudStorage()

    # print(type(sender)) <class 'celery.worker.consumer.consumer.Consumer'>
    with sender.app.connection() as conn:
        #  print(type(conn))  <class 'kombu.connection.Connection'>
         sender.app.send_task('tasks.tasks.remote_server_ready', [server_name], connection=conn, queue='default')
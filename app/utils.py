from google.oauth2 import service_account
from google.cloud import storage

from PIL import Image
from zipfile import ZipFile, ZipInfo
import pathlib
import io
import os

parent_file = pathlib.Path(__file__).resolve().parent

class GCloudStorage():
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            "./config/NAME-OF-THE-JSON-FILE.json"
        )

        self.gcloud_path_current = "current/"
        self.gcloud_path_done = "done/"

        self.local_path_current = "./data/input/"
        self.local_path_done = "./data/output/"
        
        self.storage_client = storage.Client(credentials=credentials)
        self.bucket_name = "tensorflow-spot-arch-bucket"

        self.bucket = self.storage_client.bucket(self.bucket_name)

    def create_local_folders(self, zip_id):
        input_folder_path = self.local_path_current + zip_id
        output_folder_path = self.local_path_done + zip_id

        os.makedirs(input_folder_path)
        os.makedirs(output_folder_path)

    def download_images(self, zip_id):
        file_name = self.gcloud_path_current + zip_id + ".zip"

        local_path = pathlib.Path(self.local_path_current, zip_id)

        blob = storage.Blob(file_name, self.bucket)

        object_bytes = blob.download_as_bytes()

        archive = io.BytesIO()
        archive.write(object_bytes)

        with ZipFile(archive, 'r') as zip_archive:
            # print(zip_archive.namelist())

            # for zinfo in zip_archive.filelist:
            #     print(zinfo.file_size)
            zip_archive.extractall(local_path)

    def upload_images(self, zip_id):
        local_path = pathlib.Path(self.local_path_done, zip_id)

        archive = io.BytesIO()
        with ZipFile(archive, 'w') as zip_archive:
            for file_path in local_path.iterdir():

                image_file = io.BytesIO()

                pil_image = Image.open(file_path)
                pil_image.save(image_file, "png")
                pil_image.close()
                
                zip_entry_name = file_path.name
                zip_file = ZipInfo(zip_entry_name)
                zip_archive.writestr(zip_file, image_file.getbuffer())

        archive.seek(0)
        
        file_name = self.gcloud_path_done + zip_id + ".zip"
        blob = self.bucket.blob(file_name)

        blob.upload_from_file(archive, content_type='application/zip')
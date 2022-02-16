import tensorflow as tf
from glob import glob

from loader import load_img

class TFInference():
    def __init__(self):
        # Test WITH GPU
        self.model = tf.keras.models.load_model('models/ema_gan_model')

        # Test WITHOUT GPU
        # self.model = tf.keras.models.load_model('models/gan_model')

    def load_dataset(self, zip_id):
        folder_path = f"./data/input/{zip_id}/*.jpg"
        images_paths = sorted(glob(folder_path))

        batch_size = 1

        dataset = tf.data.Dataset.from_tensor_slices((images_paths))
        dataset = dataset.map(load_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)

        return dataset.batch(batch_size)

    def run_inference(self, zip_id):
        generator = self.load_dataset(zip_id)

        index = 0

        for img in generator:
            output = self.model.predict(img)

            index += 1
            tf.keras.utils.save_img(f"data/output/{zip_id}/image{index}.png", output[0])



        
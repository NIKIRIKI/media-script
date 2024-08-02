import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class ImageDownloader:
    def __init__(self, urls, input_dir):
        self.urls = urls
        self.input_dir = Path(input_dir)

    def download_images(self):
        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(self.urls):
                executor.submit(self.download_image, url, i)

    def download_image(self, url, i):
        input_dir = self.input_dir / f'input_image_{i}'
        input_dir.mkdir(parents=True, exist_ok=True)
        output_file = input_dir / 'input_image.jpg'
        response = requests.get(url)
        response.raise_for_status()
        with open(output_file, 'wb') as f:
            f.write(response.content)

import logging
import os
import pathlib
import requests
from requests.exceptions import HTTPError

from pyunsplash import PyUnsplash
from dotenv import dotenv_values

config = dotenv_values()
api_key = config['API_KEY']


logging.basicConfig(
    format="[%(asctime)s] | %(filename)-20s:%(lineno)3d | %(levelname)-7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )
logging.warning('log into app account')


# instantiate PyUnsplash object
py_un = PyUnsplash(api_key=api_key)

def download_images(link: str):
    """
    downloading image from https://unsplash.com via requests library
    :param link: link to the photo. (link example: photo_object.body['urls']['full'])

    """
    try:
        response = requests.get(link, allow_redirects=True)
        # Raises an exception if status code is not 2xx
        response.raise_for_status()

        logging.warning('successfully connect to photo page')

        # create folder for images in current directory
        img_folder = pathlib.Path.cwd().__str__() + "/images"
        # do not create new folder if already exists
        if not pathlib.Path(img_folder).exists():
            pathlib.Path(img_folder).mkdir()

        # write image like binary file in current working directory
        with open(f'{img_folder}/image.jpg', mode='wb') as file:
            file.write(response.content)

        logging.warning('successfully downloading image')
    except HTTPError as e:
        logging.error('HTTP error %s', (e))

def main():
    logging.warning('search required photos')
    search = py_un.search(type_='photos', query='redhead beauty', per_page=2)
    for photo in search.entries:
        download_images(photo.body['urls']['full'])



if __name__ == '__main__':
    main()
    

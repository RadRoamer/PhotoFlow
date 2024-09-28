import logging
import pathlib
import requests
from requests.exceptions import HTTPError

from pyunsplash import PyUnsplash
from dotenv import dotenv_values

config = dotenv_values()
api_key = config['API_KEY']
# create logger
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

# create formatter to configure the log format
formatter = logging.Formatter(
    "[%(asctime)s] | %(filename)-20s:%(lineno)3d | %(levelname)-7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')
file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")
file_handler.setLevel('WARNING')

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# add formatter to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# configure logs for other modules
logging.basicConfig(handlers=[console_handler, file_handler])

def download_images(link: str, photo_name: str):
    """
    downloading image from https://unsplash.com via requests library
    :param link: link to the photo. (link example: photo_object.body['urls']['full'])
    """
    try:
        response = requests.get(link, allow_redirects=True)
        # Raises an exception if status code is not 2xx
        response.raise_for_status()

        logger.debug('successfully connect to photo page')

        # create folder for images in current directory
        image_path = pathlib.Path.cwd() / "images" / f"{photo_name}.png"
        # create folder if not already exists
        image_path.parent.mkdir(exist_ok=True)
        # write image to file
        image_path.write_bytes(response.content)

        logger.warning("successfully download image: '%s'", photo_name)
    except HTTPError as e:
        logger.error('HTTP error %s', e, exc_info=True)


def search_photos(py_un: PyUnsplash, query: str, quantity: int = 2):
    """
    Search for a specified number of photos based on a given query 
    :param py_un: PyUnsplash object
    :param query: searching query passed as string
    :param quantity: quantity of searching photos (by default equal 2)
    """
    logger.warning("search for the required photos using the following query: '%s'", query)
    if not isinstance(py_un, PyUnsplash):
        raise ValueError(
            f'you should pass the PyUnsplash object, not : {type(py_un)}')

    if not isinstance(query, str) or len(query) <= 0:
        raise ValueError('you should pass not empty srting to query value')

    search = py_un.search(type_='photos', query=query, per_page=quantity)

    for photo in search.entries:
        download_images(photo.body['urls']['full'],
                        photo.body['alt_description'])


def main():
    logger.warning('log into app account')
    # instantiate PyUnsplash object
    py_un = PyUnsplash(api_key=api_key)
    search_photos(py_un, 'supra turbo')


if __name__ == '__main__':
    main()

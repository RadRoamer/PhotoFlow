import logging
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

def main():
    logging.warning('search required photos')
    search = py_un.search(type_='photos', query='redhead beauty', per_page=5)
    for photo in search.entries:
        print(photo.link_download)


if __name__ == '__main__':
    main()

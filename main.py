import logging
from pyunsplash import PyUnsplash
from dotenv import dotenv_values

config = dotenv_values()
api_key = config['API_KEY']

# instantiate PyUnsplash object
py_un = PyUnsplash(api_key=api_key)


#
def main():
    search = py_un.search(type_='photos', query='redhead beauty', per_page=5)
    for photo in search.entries:
        print(photo.id, photo.link_download)


if __name__ == '__main__':
    main()

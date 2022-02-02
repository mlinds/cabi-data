# """
# Module Docstring
# """

# __author__ = "Maxwell Lindsay"
# __version__ = "0.1.0"
# __license__ = "MIT"

# %%

from logzero import logger
import requests
from xml.etree import ElementTree

data_url = "https://s3.amazonaws.com/capitalbikeshare-data/index.html"

try:
    with requests.get(data_url) as r:
        print(r.text)
except:
    logger.error('could not reach CaBi data repository')
# def main():
#     """Main entry point of the app"""
#     logger.info("hello world")


# if __name__ == "__main__":
#     """This is executed when run from the command line"""
#     main()

# %%

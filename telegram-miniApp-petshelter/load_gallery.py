import os
from dotenv import load_dotenv
load_dotenv()

from imgurpython import ImgurClient

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

client = ImgurClient(client_id, client_secret)

# get album images as list
def get_images(id_type, album_id = None):

    alist = []

    if album_id is None:
        if id_type == 2:
            alist.append("static/photos/place-holder-cat.png")
        elif id_type == 3:
            alist.append("static/photos/place-holder-dog.png")

    else:
        items = client.get_album_images(album_id)
        for item in items:
            alist.append(item.link)

    return alist
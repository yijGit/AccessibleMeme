import search
import database
from imgcmp import img_cmp
from ocr import retrieve_text
import os
import time
from sys import argv
from gtts import gTTS
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
import requests
import webbrowser


def strc_simil(img, db_imgs):
    max_value = 0
    max_index = 0
    for index, value in enumerate(db_imgs):
        if img_cmp(img, db_imgs)[0] > max:
            max_value = value
            max_index = index

    # from testing, seems that similarity score of 0.8+ is most accurate 
    # for finding the same image
    if max_value > 0.8:
        return max_index
    else:
        return None

def read_text(img):
    return retrieve_text(img)

def main(argv):
    db_file = r"/Users/jlyi/Desktop/Meme Image Captioning/src/memes.db"
    connection = database.create_connection(db_file)
    rows = database.select_all_images(connection)
    rows2 = database.select_all_descriptions(connection)
    # needs rework, won't always grab the name of the meme off KnowYourMeme.com
    '''
    if (strc_simil(argv[0], rows) == None):
        filePath = '/Users/jlyi/Desktop/MemeCaption/img/test3.png'
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']
        raw = get(fetchUrl).text
        page = fromstring(raw)
        for result in page.cssselect(".r a"):
            url = result.get("href")
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
            print(url[0])
    '''
    index = strc_simil(argv[0], rows)
    print(rows2[index])
    print('------------------------------')
    print(read_text(argv[0]))

if __name__ == "__main__":
    main(argv)
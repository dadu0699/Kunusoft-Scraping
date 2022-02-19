from email.mime import image
from pathlib import Path
import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image
import requests

time_wait = 1

load_dotenv()
FOLDER_PATH = os.getenv('FOLDER_PATH')

kunusoft_website = 'https://www.kunusoft.com/slides/ia1'
websites = [
    {
        'name': 'Presentation 01',
        'url': f'{kunusoft_website}/ia101_intro'
    },
    {
        'name': 'Presentation 02',
        'url': f'{kunusoft_website}/ia102_agentes'
    },
    {
        'name': 'Presentation 03',
        'url': f'{kunusoft_website}/ia103_otras'
    },
    {
        'name': 'Presentation 04',
        'url': f'{kunusoft_website}/ia104_informadas'
    },
    {
        'name': 'Presentation 05',
        'url': f'{kunusoft_website}/ia105_adversario'
    },
]

bcolors = {
    'OKBLUE': '\033[94m',
    'WARNING': '\033[93m',
    'ENDC': '\033[0m',
}


def colors(color, message):
    return f'{bcolors[color]}{message}{bcolors["ENDC"]}'


def visit_websites():
    for website in websites:
        print(colors(
            'OKBLUE',
            f'Visiting {website["name"]}'
        ))
        get_images(website)

        time.sleep(time_wait)


def get_images(website: dict[str, str]):
    website_url = website['url']

    while True:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'lxml')

        image_src = soup.find('img').get('src')
        image_url = f'{website["url"]}/{image_src}'
        image = Image.open(requests.get(image_url, stream=True).raw)
        save_image(website['name'], image_src, image)

        navigation_bar = soup.find('div', class_='navigation')
        links = navigation_bar.find_all('a')

        main_page = links[0].get('href')
        next_page = links[-2].get('href')
        if main_page == next_page:
            break

        website_url = f'{website["url"]}/{next_page}'


def save_image(folder_name: str, img_name: str, img: Image):
    path = f'{FOLDER_PATH}/{folder_name}'.replace('\\', '/')

    Path(path).mkdir(parents=True, exist_ok=True)
    img.save(f'{path}/{img_name}', 'JPEG')
    print(f'Saved {img_name}')


if __name__ == '__main__':
    start = time.time()

    visit_websites()

    end = time.time()
    total_time = round(end - start, 2)
    print(colors(
        'WARNING',
        f'Runtime of the program is {total_time} seconds'
    ))

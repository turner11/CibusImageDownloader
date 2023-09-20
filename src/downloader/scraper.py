import urllib
from bs4 import BeautifulSoup
import aiohttp
import urllib.request
from PIL import Image


async def get_images(url: str) -> Image:
    """
    Extracts links from a webpage.
    """

    image_url = await get_image_url(url)
    # Download the image:
    img = get_image_instance(image_url)
    img = set_image_size(img)

    return img


def set_image_size(img, min_height=None):
    magic_ratio = 3.115
    width, height = img.size
    min_height = min_height or width * magic_ratio
    if height < min_height:
        new_size = (int(min_height), int(width))
        img = img.resize(new_size)
    return img


def get_image_instance(image_url):
    image_bytes = urllib.request.urlopen(image_url).read()
    from io import BytesIO
    bio = BytesIO(image_bytes)
    img = Image.open(bio, )
    return img


async def get_image_url(url):
    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            image_elements = soup.find_all('img', src=True)

            a = image_elements[0]
            src = a['src']
            base = url.split('?')[0].strip('/')
            image_url = f'{base}/{src}'
    return image_url

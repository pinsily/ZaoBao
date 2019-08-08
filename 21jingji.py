import os
import re

import requests
from PIL import Image
from scrapy import Selector
import img2pdf
from utils import get_now_day, get_today_directory


def image_urls():
    base_url = "http://epaper.21jingji.com/"

    response = requests.get(base_url)

    selector = Selector(text=response.text)

    last = selector.xpath("//div[@class='main']/a[last()]/@onclick").extract_first()

    pages = re.search(r"changeMap\((.*)\)", last).group(1)

    year, month, day = get_now_day()

    img_urls = {f"{str(page).zfill(2)}.png": f"https://res.21jingji.com/download/ipadPaper/{year}{month}{day}/{str(page).zfill(2)}.png"
                for page in range(1, int(pages) + 1)}

    return img_urls


def img_pdf(files: list) -> None:
    directory = get_today_directory()
    year, month, day = get_now_day()
    output_file = f"{directory}/{year}{month}{day}_21jingji.pdf"
    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(files))


def download_img():
    img_urls = image_urls()

    paths = []

    for file_name, url in img_urls.items():
        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        paths.append(file_name)

    img_pdf(paths)
    remove_files(paths)


def remove_files(paths: list) -> None:
    """移出PDF子文件

    [description]
    :param
        paths: [description]
    """
    for file in paths:
        os.remove(file)


if __name__ == '__main__':
    download_img()

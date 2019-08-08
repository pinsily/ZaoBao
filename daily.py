import requests
from scrapy.selector import Selector
import os
import logging.config

from utils import get_now_day, merger_pdf, get_today_directory

logging.config.fileConfig(fname='logging.conf')
logger = logging.getLogger("daily")


def get_tech_pdf_dict() -> dict:
    """获取当前日报的所有pdf链接

    [description]

    :returns: {filenames: urls}
    """
    year, month, day = get_now_day()

    logger.info("开始获取{0}年{1}月{2}日科技日报pdf......".format(year, month, day))

    url = "http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/html/{0}-{1}/{2}/node_2.htm".format(year, month, day)

    base_url = "http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/html/{0}-{1}/{2}/{3}"

    resp = requests.get(url)
    selector = Selector(text=resp.text)

    # ./node_2.htm or node_2.htm
    pages = {url.split("/")[-1]: base_url.format(year, month, day, url) for url in
             selector.xpath("//div[@class='bmname']//a/@href").extract()}

    # get every pdf links
    # http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/images/2019-08/07/02/DefPub2019080702.pdf
    # ../../../images/2019-08/07/02/DefPub2019080702.pdf
    pdfs = dict()
    for name, link in pages.items():
        sel = Selector(text=requests.get(link).text)
        url = sel.xpath("//div[@class='pdf']/a/@href").extract_first()
        pdfs[url.split("/")[-1]] = "http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/{0}".format(url[9:])

    return pdfs


def get_people_pdf_dict() -> dict:
    """获取当前日报的所有pdf链接
    
    [description]
    
    :returns: {filenames: urls}
    """
    year, month, day = get_now_day()

    logger.info("开始获取{0}年{1}月{2}日人民日报pdf......".format(year, month, day))

    url = "http://paper.people.com.cn/rmrb/html/{0}-{1}/{2}/nbs.D110000renmrb_01.htm#".format(year, month, day)

    base_url = "http://paper.people.com.cn/rmrb/{0}"

    resp = requests.get(url)
    selector = Selector(text=resp.text)

    # ../../../page/2019-07/30/18/rmrb2019073018.pdf
    pdfs = {url.split("/")[-1]: base_url.format(url[9:]) for url in
            selector.xpath("//div[@class='right_title-pdf']/a/@href").extract()}

    return pdfs


def download_pdf(pdfs: dict, output_file_name: str) -> str:
    """下载当前所有电子书PDF
    
    [description]
    """
    logger.info("开始下载当天所有电子书......")
    year, month, day = get_now_day()
    directory = get_today_directory()

    output_file = f"{directory}/{year}{month}{day}_{output_file_name}.pdf"

    if os.path.exists(output_file):
        return output_file

    paths = []

    for file_name, url in pdfs.items():
        logger.info("-- 开始下载: {0}".format(file_name))
        with open(file_name, 'wb') as f:
            resp = requests.get(url)
            f.write(resp.content)

        logger.info("-- 下载完成: {}".format(file_name))

        paths.append(f"{file_name}")

    merger_pdf(output_file, paths)
    remove_files(paths)

    return output_file


def remove_files(paths: list) -> None:
    """移出PDF子文件
    
    [description]
    :param
        paths: [description]
    """
    for file in paths:
        os.remove(file)


def daily_main():
    download_pdf(get_people_pdf_dict(), "people_daily")
    download_pdf(get_tech_pdf_dict(), "tech_daily")


if __name__ == "__main__":
    daily_main()

import os
import time
import logging.config

from PyPDF2 import PdfFileWriter, PdfFileReader

logging.config.fileConfig(fname='logging.conf')
logger = logging.getLogger("utils")


def is_weekday():
    """判断是否是周末

    [description]

    :returns: True or False
    """
    return time.strftime("%A", time.localtime(time.time())) in ["Sunday", "Saturday"]


def get_now_day() -> tuple:
    """获取年月日

    [description]

    :returns: year: 2019, month: 08, day: 08
    """
    localtime = time.localtime(time.time())
    return localtime.tm_year, str(localtime.tm_mon).zfill(2), str(localtime.tm_mday).zfill(2)


def merger_pdf(output_path: str, input_paths: list) -> None:
    """合并当天的所有PDF为一份

    [description]
    :param
        output_path: str, 合并后的文件名
        input_paths: list, 所有当天电子书集合
    """
    logger.info("开始合并电子书......")
    pdf_writer = PdfFileWriter()

    for path in input_paths:
        pdf_reader = PdfFileReader(path, strict=False)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)


def get_today_directory() -> str:
    """创建当天的目录

    :return: None
    """
    year, month, day = get_now_day()

    directory = f"warehouse/{year}{month}{day}"
    if not os.path.exists(directory):
        logger.info(f"创建今日目录:{directory}")
        os.makedirs(directory)

    return directory


if __name__ == '__main__':
    get_today_directory()

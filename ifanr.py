import requests
from scrapy.selector import Selector
import pdfkit
import logging.config

from utils import is_weekday, get_now_day, get_today_directory

logging.config.fileConfig(fname='logging.conf')
logger = logging.getLogger("ifanr")

# 需要指定wkhtmltopdf位置，path里面没用
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '2.00in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}

pre = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">

    <title>{title}</title>
    <link rel="shortcut icon" href="https://images.ifanr.cn/wp-content/themes/ifanr-5.0-pc/static/images/favicon.ico"/>


    <link rel='stylesheet' id='videojs-css'
          href='https://images.ifanr.cn/wp-content/plugins/more-editor-style/editor-function-button-style.css?ver=4.9.9'
          type='text/css' media='all'/>
    <link rel='stylesheet' id='doge-style-css'
          href='https://images.ifanr.cn/wp-content/themes/ifanr-5.0-pc/static/dist/app-a8d89f4f50.min.css?ver=4.9.9'
          type='text/css' media='all'/>
    <link rel='stylesheet' id='widgetbuzz-css'
          href='https://images.ifanr.cn/wp-content/plugins/ifanr-widget-buzz/dist/build/buzz.auto_create_ts_1446046962.css?ver=4.9.9'
          type='text/css' media='all'/>

    <style>
        .o-single-content {{
            position: unset;
            float: unset;
            overflow: hidden;
            width: calc(50% + 230px);
            min-height: 100%;
            margin: auto;
        }}
    </style>

</head>

<body class="post-template-default single single-post postid-1245341 single-format-standard" data-component="TextClamp">
<div class="page-body">


    <div class="sidebar-drawer-menu-overlay js-drawer-menu-overlay--hide"
         data-component="DrawerMenuOverlay">

    </div>

    <div class="o-single-wrapper ">
        <div class="o-single" data-category="早报">
            <div class="o-single-content" id="article-content-wrapper">
                <div class="o-single-content__body o-single-content__body--main">
                    <div id="article-header" class="o-single-content__header">
                        <img src="{head_image}" alt=""
                             width="100%">
                    </div>
                    <div class="o-single-content__body c-single-normal__header" id="content-meta-header">
                        <div class="o-single-normal-content">
                            <h1 class="c-single-normal__title">{title}</h1>
                        </div>
                    </div>

                    {article}

                    </div>
                </div>
            </div>
        </div>
</div>
</body>
</html>
"""


def get_latest_url():
    """[获取最新文章链接]
    
    [description]
    
    :returns: [description]
    """
    response = requests.get("https://www.ifanr.com/category/ifanrnews")
    selector = Selector(text=response.text)
    latest_new_url = selector.xpath(
        "//div[@id='articles-collection']//a[@class='article-link cover-block']/@href").extract_first()

    return latest_new_url


def get_content() -> tuple:
    latest_new_url = get_latest_url()

    response = requests.get(latest_new_url)

    selector = Selector(text=response.text)

    article = selector.xpath("//article").extract_first()
    title = selector.xpath("//h1[@class='c-single-normal__title']/text()").extract_first()
    head_image = selector.xpath("//div[@class='o-single-content__header']/img/@src").extract_first()

    return title, head_image, article


def convert_pdf():
    title, head_image, article = get_content()

    if is_weekday():
        logger.warning("周末不发版")
        return "周末不发版"

    year, month, day = get_now_day()
    directory = get_today_directory()
    filename = f'{directory}/{year}{month}{day}.pdf'

    html = pre.format(title=title, article=article, head_image=head_image)
    pdfkit.from_string(html, filename, configuration=config, options=options)


def ifanr_main():
    convert_pdf()


if __name__ == '__main__':
    ifanr_main()

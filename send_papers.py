import os
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
import sys
import time
sys.path.append(".")

from email.message import EmailMessage
from email.policy import SMTP
from email.mime.text import MIMEText


"""

reference: https://docs.python.org/3.6/library/email.examples.html
"""


def get_now_day() -> tuple:
    """获取年月日
    
    [description]
    
    :returns: year, month, day
    """
    localtime = time.localtime(time.time())
    return localtime.tm_year, str(localtime.tm_mon).zfill(2), str(localtime.tm_mday).zfill(2)

def send_email(filename: str, receivers: list) -> None:
    
    msg = EmailMessage()
    year, month, day = get_now_day()
    msg['Subject'] = "{0}.{1}.{2} 早报推送".format(year, month, day)
    msg['To'] = receivers
    msg['From'] = "13160724868@163.com"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    msg.set_content("2019.08.07 日报推送")

    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(filename, 'rb') as fp:
        msg.add_attachment(fp.read(),maintype=maintype,subtype=subtype,filename=filename)
    
    with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
        server.login("13160724868@163.com", "pinsily96")
        server.send_message(msg) 
        print ("邮件发送成功")


if __name__ == '__main__':
    import people_daily
    import tech_daily

    pd = people_daily.download_pdf()

    send_email(pd, "13160724868@163.com")

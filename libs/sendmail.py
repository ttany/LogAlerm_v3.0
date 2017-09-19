#!/usr/bin/python
#_*_coding:utf-8_*_
# @Time    : 2017/9/13 11:15
# @Author  : kebz
# @Site    : 
# @File    : sendmail.py
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email import encoders
import smtplib,os

class SendMail(object):

    def __init__(self,from_addr,to_addr,server,port=25):

        self.host=server
        self.port=port
        self.from_name=from_addr[0]
        self.from_addr=from_addr[1]
        self.to_addr=to_addr

    message = MIMEMultipart()

    def add_html(self,subject=None,content=None):

        self.message['From'] = formataddr((Header(self.from_name,'utf-8').encode(),self.from_addr))
        self.message['To'] = ','.join(self.to_addr)
        self.message['Subject'] = Header("{}".format(subject),'utf-8').encode()
        self.message.attach(MIMEText(content, 'html', 'utf-8'))

    def add_attachment(self,file_name,file_data):
        att = MIMEBase('text', 'txt', filename=os.path.basename(file_name))
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
        att.set_payload(file_data)
        encoders.encode_base64(att)
        self.message.attach(att)

    def add_images(self,img_name,img_data):
        img = MIMEImage(img_data)
        img.add_header('Content-ID',img_name)
        self.message.attach(img)

    def send_mail(self):
        try:
            self.server=smtplib.SMTP()
            self.server.connect(self.host,self.port)
            self.server.sendmail(self.from_addr, self.to_addr, self.message.as_string())
            self.server.quit()
        except Exception as e:
            return e



if __name__=='__main__':

    content="<h1>你妹的，发什么文件啊</h1><img src='cid:ddd.png'></br><img src='cid:demo.jpg'>"

    mail=SendMail(
        server="intramail.lianlianpay.com",
        port=25,
        from_addr=["测试发件者","elk_monitor@lianlianpay.com"],
        to_addr=["kebz@lianlianpay.com","douwb@lianlianpay.com"]
    )
    mail.add_html(subject='我是柯斌志',content=content)


    attachment=["./text1.txt","text2.zip"]
    for att in attachment:
        with open(att,'rb') as f:
            data=f.read()
            file_name=os.path.basename(att)
            mail.add_attachment(file_name=file_name,file_data=data)

    #插入图片，将图片文件名称写入html文件中cid:demo.jpg
    img_list=['./ddd.png','./demo.jpg']
    for line in img_list:
        with open(line,'rb') as f:
            data=f.read()
            img_name=os.path.basename(line)
            mail.add_images(img_name=img_name,img_data=data)

    check=mail.send_mail()
    if check is not None:
        print("send mail failure:{}".format(check))
    else:
        print ("send mail success")


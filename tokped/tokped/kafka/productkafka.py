import scrapy
from logging import exception
import datetime
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
from pyvirtualdisplay import Display
from impala.dbapi import connect
from selenium.webdriver.common.proxy import *
import traceback
import setting
import MySQLdb
import sys
import json
import demjson

import time


class feedback:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host=setting.host,
            port=setting.port,
            user=setting.user,
            passwd=setting.passwd,
            db=setting.db)
        self.connect = self.conn
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Firefox()

    def parse(self):
        cur = self.conn.cursor()
        cou = self.conn.cursor()
        try:
            url = 'https://www.tokopedia.com/chocoapple/info'
            self.driver.get(url)
            response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
            penjual_url = MySQLdb.escape_string(response.xpath('//*[contains(@id,"mod-product-detail")]/aside/div/article/div[2]/h5/a/@href').extract_first())
        except Exception, e:
            print e
        cur.close()
        try:
            self.driver.close()
        except Exception, e:
            print e


if __name__ == '__main__':
    p = feedback()
    p.parse()

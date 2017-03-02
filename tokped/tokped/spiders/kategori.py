# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import pytesseract
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
from scrapy.http import Request
# from tokorobet.items import tcategory
# from impala.dbapi import connect
import traceback
import MySQLdb
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import urllib2
import urllib
from tokped.items import outjson



class ProductSpider(scrapy.Spider):
    name = "tokped"
    allowed_domains = ["https://www.tokopedia.com/"]
    start_urls = ["https://www.tokopedia.com/"]

    def __init__(self,conn):
        self.conn = conn
        global driver
        # path_to_chromedriver = 'D://chromedriver'
        # self.driver = webdriver.Chrome(executable_path = path_to_chromedriver)
        driver = webdriver.Firefox()
    @classmethod
    def from_crawler(cls,crawler):
        conn=MySQLdb.connect(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)

    def parse(self, response):
        # global response
        cur = self.conn.cursor()
        cou = self.conn.cursor()
        count = "select count(*)from tokopedia where status != 'done'"
        sql = "select penjual_url from tokopedia where status != 'done'"
        cur.execute(sql)
        cou.execute(count)
        results = cur.fetchall()
        b = cou.fetchall()
        terus = str(b).replace(",", "").replace("'", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("L", "")
        terus = int(terus)
        print "============================================"
        print (terus)
        for ulang in range(0,terus):
            try:
                print (ulang)
                a = results[ulang]
                url = str(a).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                info_url = url + '/info'
                driver.get(info_url)
                a = driver.current_url
                response = TextResponse(driver.current_url, body=driver.page_source, encoding='utf-8')
                for i in range(1,2):
                    try:
                        linkphoto = response.xpath('//*[contains(@class, "shop-info-location")]/li/p[4]/img/@src').extract_first()
                        photo = linkphoto.split('shop_id=')[1]
                        direktori = '/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/gambar/' + photo + '-nomor.png'
                        urllib.urlretrieve(linkphoto, direktori)
                        im = Image.open(direktori)
                        imB = im.resize((200, 22))
                        imB.save('/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/coy_nomor.png')
                        varnum = pytesseract.image_to_string(Image.open('/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/coy_nomor.png'))
                        varnum = str(varnum)
                        nomor = varnum.replace("«FE-2", '0')
                        #===============================
                        linkphoto2 = response.xpath('//*[contains(@class, "shop-info-location")]/li/p[3]/img/@src').extract_first()
                        photo2 = linkphoto2.split('shop_id=')[1]
                        direktori2 = '/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/gambar/' + photo2 + '-email.png'
                        urllib.urlretrieve(linkphoto2, direktori2)
                        im2 = Image.open(direktori2)
                        imB2 = im2.resize((320,69))
                        imB2.save('/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/coy_email.png')
                        varnum2 = pytesseract.image_to_string(Image.open('/home/grendy/Downloads/Telegram Desktop/Crawling/tokped/coy_email.png'))
                        varnum2 = str(varnum2)
                        email = varnum2
                        #PRINT
                        print "===========++++++==============="
                        print nomor
                        print "direktori_nomor = " + str(direktori)
                        print email
                        print "direktori_email = " + str(direktori2)
                        print "===========++++++=================="
                        time.sleep(2)
                        #
                    except:pass
            except:
                print traceback.print_exc()
        cur.close()
        try:
            driver.close()
        except:
            pass
def pagination(response):
    try:
        driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
    except:
        try:
            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
        except:
            try:
                driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
            except:
                try:
                    driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                except:
                    try:
                        driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                    except:
                        try:
                            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
                        except:
                            driver.find_element_by_xpath('//*[contains(@class,"pagination light-theme simple-pagination")]//*[contains(text(),"Next")]').click()
import scrapy
# from kafka import KafkaProducer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
import traceback
import MySQLdb
from pyvirtualdisplay import Display

import time


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["https://tokopedia.com"]
    start_urls = ["https://www.tokopedia.com"]

    def __init__(self,conn):
        self.conn = conn
        # path_to_chromedriver = 'D://chromedriver'
        # self.driver = webdriver.Chrome(executable_path = path_to_chromedriver)
        # self.driver = webdriver.PhantomJS()
        # display = Display(visible=0, size=(800,600))
        # display.start()
        self.driver = webdriver.Firefox()

    @classmethod
    def from_crawler(cls, crawler):
        conn = MySQLdb.connect(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)

    def parse(self, response):
        cursor = self.conn.cursor()
        try:
            a = 0
            for tidur in range(0, 100):
                time.sleep(1)
                try:
                    sql = "select url from tokopedia_kategori"
                    cursor.execute(sql)
                    results = cursor.fetchall()
                   # import pdb;pdb.set_trace()
                    # results = "https://www.tokopedia.com/p/pakaian"
                    for ulang in range(0, 21):
                        a = results[ulang]
                        url = str(a).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                        print "====================================="
                        print(url)
                        print "====================================="
                        self.driver.get(url)
                        a = self.driver.current_url
                        time.sleep(5)
                        try:
                            for click in range(1, 240):
                                if url == "https://www.tokopedia.com/p/handphone-tablet":
                                    break
                                else:
                                    for kat in range(1,26):
                                        for kalem in range(0,100):
                                            time.sleep(1)
                                            try:
                                                response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
                                                penjual_url = response.xpath('//*[@class="product-content ng-scope"]/div['+str(kat)+']//*[@class="shop-table"]/div/div[2]/a/@href').extract_first()
                                                penjual = response.xpath('//*[@class="product-content ng-scope"]/div['+str(kat)+']//*[@class="shop-table"]/div/div[2]/a/text()').extract_first()
                                                if penjual_url == None:
                                                    pass
                                                else:
                                                    try:
                                                        status = ""
                                                        sql = "INSERT INTO `tokopedia`(`penjual_url`,`penjual`, `status`) VALUES ('{}','{}','{}') ".format(penjual_url,penjual,status)
                                                        cursor.execute(sql)
                                                        self.conn.commit()
                                                        print "======================================="
                                                        print penjual_url
                                                        print "INSERT SUKSES"
                                                        print "======================================="
                                                    except:
                                                        print "==============================================================================="
                                                        print "Data Duplicate"
                                                        print penjual_url
                                                        print "==============================================================================="
                                                        pass
                                                    break
                                            except:
                                                pass
                                nex = url + '?page=' + str(click+1)
                                try:
                                    self.driver.get(nex)
                                except:
                                    pass
                                b = self.driver.current_url
                                if a == b:
                                    break
                        except:
                            pass
                except:
                        pass

        except:
            pass
        db.close()
        try:
            self.driver.close()
        except:
            pass

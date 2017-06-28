# -*- coding: utf-8 -*-
from miette import DocReader
from crpn.items import CrpnItem
from scrapy.selector import Selector
from docx import Document
import scrapy
import win32ctypes
import redis
import re


class spider(scrapy.Spider):

    def __init__(self):
        # super(CrpnRedisSpider, self).__init__()
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    name = 'crpn'
    start_urls = ['http://www.crpn.cn/']
    header = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    cookie = {
        't': 'X8j2R3'
    }

    def start_requests(self):
        yield scrapy.Request('http://www.crpn.cn/news.php?classid=84', headers=self.header, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        # print response.xpath('//tr[@height="25"]')
        # datas = Selector(response)
        for data in response.xpath('//tr[@height="25"]'):
            item = CrpnItem()
            item['title'] = data.xpath('td/a/font/text()').re('\](.*)\(')
            item['region'] = data.xpath('td/a/font/text()').re('\[(.*)\]')
            item['tender_number'] = data.xpath('td/a/font/text()').re('\((.*)\)')
            href = data.xpath('td/a/@href').extract()
            detail_url = 'http://www.crpn.cn/' + href[0]
            id = re.findall('id=(\d+)', detail_url)[0]

            # print item, detail_url
            if not self.r.get(id):
               yield scrapy.Request(detail_url, meta={'item': item}, headers=self.header, cookies=self.cookie, callback=self.parse_detail)

    def parse_detail(self, response):
        # print response.body
        item = response.meta['item']
        item['url'] = response.url
        item['tender_type'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').re(u'公开')[0]
        item['tender_person'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'[(招标人)|(采购人))]：(.*)\r')[0]
        item['address'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td/span/p[27]/span').xpath('string(.)').re(u'址：(.*)')
        item['contact_person'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'联系人：(.*)\r')[0]
        item['tel_number'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td/span/p').re(u'\d{3}-\d{8}')
        item['start_time'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'\d{4}\年\d{1,2}\月\d{1,2}日')[-1]
        item['doc_sell_period'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'发售时间：(\w*)\，')[0]
        item['bid_open_time'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'开标时间：(.*)\。')
        item['bid_open_address'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'开标地点：(\w*)\（')
        item['doc_sell_price'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'(\d*元)')
        item['doc_sell_address'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'发售地点：(.*)\（')[0]
        item['doc_send_address'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re(u'开标地点：(\w*)\（')
        # item['tender_requirement'] = response.xpath('/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody').xpath('string(.)').re('//n')
        href = response.xpath('//a/@href').re('(.*\.doc)')[0]
        item['file_url'] = 'http://www.crpn.cn' + href
        id = re.findall('id=(\d+)', response.url)[0]
        self.r.set(id, '1')

        yield scrapy.Request(item['file_url'], meta={'item': item}, cookies=self.cookie, headers=self.header, callback=self.parse_file)

    def parse_file(self, response):
            item = response.meta['item']
            item['path'] = response.url.split('/')[-1]
            self.logger.info('Saving word %s', item['path'])
            with open(item['path'], 'wb') as f:
                f.write(response.body)
            print item
            yield item

    #

    # def parse_doc(f):
    #
    #     doc = w.Documents.Open(FileName=f)
    #     t = doc.Tables[0]
    #     name = t.Rows[0].Cells[1].Range.Text
    #     situation = t.Rows[0].Cells[5].Range.Text
    #     people = t.Rows[1].Cells[1].Range.Text
    #     title = t.Rows[1].Cells[3].Range.Text
    #     print name, situation, people, title
    #     doc.Close()


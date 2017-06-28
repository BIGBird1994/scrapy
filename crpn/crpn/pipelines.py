# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
import redis
import MySQLdb

# class DuplicatesPipeline(object):
#
#     def process_item(self, item, spider):
#
#             r = redis.Redis(host='127.0.0.1', port=6379, db=0)
#             r.set('url:%s' % item['url'], 1)
#             return item


class CrpnPipeline(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="192.168.1.212", user="yufabu", port=43666,
                                      passwd="2015SJGTWYUFABUgxm1234560",
                                      db="gt", charset="utf8")
            self.cursor = self.db.cursor()
            print "=============Connect to db successfully!==================="
        except:
            print "=============Fail to connect to db!==================="


    def process_item(self, item, spider):
        title = item['title']
        tender_number = item['tender_number']
        tender_type = item['tender_type']
        tender_person = item['tender_person']
        address = item['address']
        contact_person = item['contact_person']
        tel_number = item['tel_number']
        start_time = item['start_time']
        doc_sell_period = item['doc_sell_period']
        bid_open_time = item['bid_open_time']
        bid_open_address = item['bid_open_address']
        url = item['url']
        doc_sell_price = item['doc_sell_price']
        doc_sell_address = item['doc_sell_address']
        doc_send_address = item['doc_send_address']
        # tender_requirement = 1
        region = item['region']
        # material_detail = 2
        # file_url = item['file_url']
        path = item['path']
        param = [title,tender_number,tender_type,tender_person,address,contact_person,tel_number,start_time,doc_sell_period,bid_open_time,bid_open_address,url,doc_sell_price,doc_sell_address,doc_send_address,region,path]
        sql = 'insert into tender(title,tender_number,tender_type,tender_person,address,contact_person,tel_number,start_time,doc_sell_period,bid_open_time,bid_open_address,url,doc_sell_price,doc_sell_address,doc_send_address,region,path) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        self.cursor.execute(sql, param)

        self.db.commit()

        return item

    def close_spider(self, spider):

        self.db.commit()
        self.db.close

#!/usr/bin/python
#_*_coding:utf-8_*_
# @Time    : 2017/9/15 15:21
# @Author  : kebz
# @Site    : 
# @File    : es_search.py

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q,MultiSearch
from elasticsearch_dsl.query import MultiMatch,Match,Range
import sys
class Es(object):
    def __init__(self,host_list,sniffer_timeout=int(30)):
        self.hosts=host_list
        self.sniffer_timeout=int(sniffer_timeout)

    def connect(self):
        try:
            client= Elasticsearch(self.hosts, sniff_on_start=False,sniff_on_connection_fail=True, sniffer_timeout=self.sniffer_timeout)
            return client
        except Exception as e:
            return False

    def getResponse(self,**kwargs):
        self.index=kwargs['index']
        self.keyword=kwargs['keyword']
        self.interval=kwargs['interval']
        self.client=self.connect()
	#print self.keyword
        if self.client:
            s = Search(using=self.client, index=self.index, ) \
                .filter("query_string", query='%s' %self.keyword) \
                .query("range", **{'@timestamp': {'lt': 'now', 'gte': 'now-%s'%self.interval}})
            response = s.execute()
            #print response
	    #print s.count()
            try:
                return s.count(),{"dt":response[0].dt,"level":response[0].level,"msg":response[0].msg}
            except Exception as e:
		#print e
                return s.count(),""
        else:
            return 0,""

if __name__=="__main__":
    conn = Es(host_list=['192.168.162.57:9200', '192.168.162.58:9200', '192.168.162.59:9200'])
    error_count, log = conn.getResponse(keyword='host:("0.0.0.0") AND message:"10.20.37.72"')
    #print error_count,log


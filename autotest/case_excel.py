# #encoding:utf-8
#
# import ConfigParser
# import os
# import xlrd
# import re
# import httplib
# import urllib
# from urlparse import urlparse
# import json
# import time
# import unittest
# import pdf
#
# currentdir=os.path.split(os.path.realpath(__file__))[0]
# class test_class():
#     def getexcel(self):
#         casefile=currentdir + '/case.xls'
#         if ((os.path.exists(casefile))==False):
#             print "当前路径下没有case.xls，请检查！"
#         data=xlrd.open_workbook(casefile)
#         table = data.sheet_by_name('login')
#         nrows = table.nrows #行数
#         ncols = table.ncols #列数
#     #colnames = table.row_values(1) #某一行数据
#         for rownum in range(1,nrows):
#             for col in range (3, ncols):
#                 value=table.cell(rownum,col).value
#                 if (col==3):
#                     method=value
#                 if (col==4):
#                     url=value
#         return table,nrows,ncols
#
#     def getexceldetail(self,table,row,ncols):
#         #rownum = table.row_values(row) #某一行数据
#
#         for col in range (0, ncols):
#             value=table.cell(row,col).value
#             if (col==0):
#                 caseid=value
#         print caseid
#             if (col==3):
#                 method=value
#         print method
#             if (col==4):
#                 url=value
#         return method,url,caseid
#
#     def httpget(self,url):
#         httpClient = None
#         conn = urlparse(url)
#         url=url.encode('utf-8')
#         try:
#             httpClient = httplib.HTTPConnection(conn.netloc, timeout=10)
#             httpClient.request('GET', url)
#
#         # response是HTTPResponse对象
#             response = httpClient.getresponse()
#             print response
#             d0=response.read()
#             d0=d0.decode('unicode_escape')
#         except Exception, e:
#             print e
#         finally:
#             if httpClient:
#                 httpClient.close()
#         return response.status,d0
#
#     def httppost(self,url):
#         httpClient = None
#         conn = urlparse(url)
#         url=url.encode('utf-8')
#         try:
#             header = {"Content-type": "application/x-www-form-urlencoded",
#                   "Accept": "text/plain"}
#
#             httpClient = httplib.HTTPConnection(conn.netloc, timeout=30)
#             httpClient.request("POST", url)
#             response1 = httpClient.getresponse()
#             d1=response1.read()
#             d1=d1.decode('unicode_escape')
#         except Exception, e:
#             print e
#         finally:
#             if httpClient:
#                 httpClient.close()
#         return response1.status,d1

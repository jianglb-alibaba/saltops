#!/usr/bin/env python  
# -*- coding: utf8 -*-  
  
from weibo1 import APIClient, OAuthToken  
import MySQLdb  
import time  
"""
APP_KEY和 APP_SECRET填入你申请到的APP的key和secret，从新浪的网站上可以查询到。

"""  



#通过提供的账号和密码，返回APIClient对象实例  
def GetBlogClient(uname, passw):  
    APP_KEY = u'XXXXXXXXXX' # app key  
    APP_SECRET = u'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # app secret  
    #实例化APIClient  
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET)  
    #获取OAuth request token  
    reqToken = client.get_request_token()  
    #用户授权url  
    auth_url =  client.get_authorize_url(reqToken)  
    post_data = urllib.urlencode({  
            "action": "submit",  
            "forcelogin": "",  
            "from": "",  
            "oauth_callback" : "http://api.weibo.com/oauth2/default.html",  
            "oauth_token" : reqToken.oauth_token,  
            "passwd" : passw,  
            "regCallback": "",  
            "ssoDoor": "",  
            "userId" : uname,  
            "vdCheckflag" : 1,  
            "vsnval":""  
        })  
  
    mat = re.search(  
                r'&oauth_verifier=(.+)',  
                urllib2.urlopen(urllib2.Request(  
                    "http://api.t.sina.com.cn/oauth/authorize",  
                    post_data,  
                    headers={  
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)',  
                        'Referer': auth_url  
                    }  
                )).url  
            )  
    if mat:  
        client = APIClient(  
                APP_KEY,  
                APP_SECRET,  
                OAuthToken(  
                    reqToken.oauth_token,  
                    reqToken.oauth_token_secret,  
                    mat.group(1)  
                ))  
        #返回APIClient  
        return APIClient(APP_KEY, APP_SECRET, client.get_access_token())  
    else:  
        raise Exception()  
  
# end of class MyFrame  
if __name__ == "__main__":  
    client = GetBlogClient("XXXXXXXXXX","XXXXX")  
    r = client.get.statuses__user_timeline()    #使用APIstatuses/user/timeline  

import urllib
import urllib.request
import http.cookiejar
import json

class Fetion:

    def __init__(self):
        print('init Fetion class ... ')

        self.name = '135xxxx0000' #填写自己的手机号
        self.password = '747580' #填写手机短信密码

        cj = http.cookiejar.LWPCookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        self.opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(self.opener)

        self.ssid = ''
        self.uid = ''
        self.counter = 0

        is_success = self._login()
        if is_success:
            self._get_personal_info()
        else:
            self._get_sms_pwd()
            if self._login():
                self._get_personal_info()

    def _get_sms_pwd(self):
        print('request a sms password ... ')
        url = 'http://webim.feixin.10086.cn/WebIM/GetSmsPwd.aspx'

        postData = {
            "uname": self.name
        }

        postData = urllib.parse.urlencode(postData).encode('utf-8')

        request = urllib.request.Request(url, postData)
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        if '{"rc":200}' == data:
            print('request successful ... ')
            self.password = input('please input your sms password: ')
        else:
            print(data)


    def _login(self):
        print('start to login ... ')
        is_success = True

        url = 'http://webim.feixin.10086.cn/WebIM/Login.aspx'

        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Accept-Language": "zh-cn",
            "Referer": "https://webim.feixin.10086.cn/loginform.aspx",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }

        postData = {
            "UserName": self.name,
            "Pwd": self.password,
            "OnlineStatus": 400,
            "AccountType": 1
        }

        postData = urllib.parse.urlencode(postData).encode('utf-8')

        request = urllib.request.Request(url, postData, headers)
        response = urllib.request.urlopen(request)
        info = response.info()
        if info['Set-Cookie']:
            self.ssid = info['Set-Cookie'].split("webim_sessionid=")[1].split(";")[0]

        data = response.read().decode()
        if '{"rc":200,"rv":{"ndsms":false}}' == data:
            print('login successful ... ')
        else:
            is_success = False
            print(data)
        return is_success

    def _get_personal_info(self):
        print('get personal info ... ')
        url = 'http://webim.feixin.10086.cn/WebIM/GetPersonalInfo.aspx?Version=' + str(self.counter)
        self.counter = self.counter + 1

        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Accept-Language": "zh-cn",
            "Referer": "https://webim.feixin.10086.cn/main.aspx",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }

        postData = {
            "ssid": self.ssid
        }

        postData = urllib.parse.urlencode(postData).encode('utf-8')

        request = urllib.request.Request(url, postData, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        print(data)
        if data:
            data = json.loads(data)
        self.uid = str(data['rv']['uid'])
        return data

    def _get_contact_list(self):
        print('get contact list ... ')
        url = 'http://webim.feixin.10086.cn/WebIM/GetContactList.aspx?Version=' + str(self.counter)
        self.counter = self.counter + 1

        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Accept-Language": "zh-cn",
            "Referer": "https://webim.feixin.10086.cn/main.aspx",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }

        postData = {
            "ssid": self.ssid
        }

        postData = urllib.parse.urlencode(postData).encode('utf-8')

        request = urllib.request.Request(url, postData, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        print(data)
        if data:
            data = json.loads(data)
        return data

    def get_friend_uid(self, user_name):
        data = self._get_contact_list()
        friends = data["rv"]["bds"]
        for friend in friends:
            name = friend["ln"]
            uid = str(friend["uid"])
            if name.encode("utf8") == user_name:
                print(name, uid)
                return uid
        return '0'

    def send_sms(self, receivers, msg):
        print('send sms ... ')
        url = 'http://webim.feixin.10086.cn/content/WebIM/SendSMS.aspx?Version=' + str(self.counter)
        self.counter = self.counter + 1

        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Accept-Language": "zh-cn",
            "Referer": "https://webim.feixin.10086.cn/content/freeSms.htm?tabIndex=0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }

        postData = {
            "UserName": self.uid,
            "Msg": msg,
            "Receivers": receivers,
            "ssid": self.ssid
        }

        postData = urllib.parse.urlencode(postData).encode('utf-8')

        request = urllib.request.Request(url, postData, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        print(data)
        if data:
            data = json.loads(data)
        return data


if __name__ == '__main__':
    api = Fetion()
    api.send_sms(api.uid, '相逢一醉是前缘，风雨散、飘然何处')

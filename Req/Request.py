# -*- coding: UTF-8 -*-
import json
import requests
from lxml import etree


def find_xpath(html_body, xpath_load):
    selector = etree.HTML(html_body)
    path = selector.xpath(xpath_load)
    return path


class AnalysisUrl:
    # userid = input("用户名： ")
    # password = input("密码： ")

    def __init__(self, userid=716101520010, password='yanjiankai'):
        # self.userid = input("用户名： ")
        # self.password = input("密码： ")
        self.res = requests.session()
        self.dian_bo_url = ''
        self.kao_qin_url = ''
        self.course_down_url_list = []
        self.course_xun_lei_url_list = []
        self.course_url_relationship = {}
        self.relationship = {}
        self.login_url = 'http://www.onlinesjtu.com/Index.aspx'
        self.left_list_url = 'http://www.onlinesjtu.com/learningspace/learning/'
        self.org_url = 'http://www.onlinesjtu.com/learningspace/learning/student/'
        self.dian_bo_xpath = '//*/a[starts-with(@href,"dianbolist.asp?")]/@href'
        self.left_xpath = '//*[@name="left"]/@src'
        self.kao_qin_xpath = '//*/a[starts-with(@href,"kaoqin_list.asp?")]/@href'
        self.course_down_url_xpath = '//*/a[starts-with(@href,"downloadlist.asp?")]/@href'
        self.xun_lei_down_xpath = '//*/a[contains(text(),"迅雷下载")]/@href'
        self.course = ['毛泽东思想和中国特色社会主义理论体系概论', '大学英语（三)', '数据库原理与应用', '数据结构', '嵌入式系统及应用', '应用软件开发（C＃）']
        self.data = {
            '__VIEWSTATE': '/wEPDwUKMTExOTI5NDk3OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFImN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkaWJ0TG9naW7UcgS82I2VmoQMeY9GdU2K8I+8zQ==',
            '__VIEWSTATEGENERATOR': '90059987',
            '__EVENTVALIDATION': '/wEWCAKHwK2XDAKP6repDwL59L30DgLs64TUCQLz64TUCQLy64TUCQL8hK66BQKflO50CfaHMVnqLBIAhLgyEgQIbayqmQw=',
            'ctl00$ContentPlaceHolder1$tbuserid': userid,
            'ctl00$ContentPlaceHolder1$tbpassword': password,
            'ctl00$ContentPlaceHolder1$rblusertype': 0,
            'ctl00$ContentPlaceHolder1$ibtLogin.x': 36,
            'ctl00$ContentPlaceHolder1$ibtLogin.y': 18
        }

    def get_source_url(self):
        homepage = self.res.post(url=self.login_url, data=self.data)
        left_url = self.left_list_url + find_xpath(homepage.content.decode(encoding=homepage.apparent_encoding),
                                                   self.left_xpath)[0]
        print('获取导航连接并请求 ' + left_url)
        left_tree = self.res.get(url=left_url)
        self.dian_bo_url = self.org_url + find_xpath(left_tree.content.decode(encoding=left_tree.apparent_encoding),
                                                     self.dian_bo_xpath)[0]
        print('获取点播url路径 ' + self.dian_bo_url)
        self.kao_qin_url = self.org_url + find_xpath(left_tree.content.decode(encoding=left_tree.apparent_encoding),
                                                     self.kao_qin_xpath)[0]
        print('获取考勤url路径 ' + self.kao_qin_url)
        return self.dian_bo_url, self.kao_qin_url

    def get_course_down_url_list(self):
        dian_bo_url = self.get_source_url()[0]
        dow = self.res.get(dian_bo_url)
        print('获取到点播下载页面，并获取对应课程现在页面连接 ')
        coursebooks = find_xpath(dow.content.decode(encoding=dow.apparent_encoding), self.course_down_url_xpath)
        for i in range(0, len(coursebooks)):
            self.course_down_url_list.append(self.org_url + coursebooks[i])
        return self.course_down_url_list

    def get_course_xun_lei_url_list(self):
        print('获取每个课程下的迅雷下载链接 ')
        for i in range(0, len(self.course_down_url_list)):
            dow = self.res.get(self.course_down_url_list[i])
            course_xun_lei_url_list = find_xpath(dow.content.decode(encoding=dow.apparent_encoding),
                                                 self.xun_lei_down_xpath)
            self.course_xun_lei_url_list.append(course_xun_lei_url_list)
        return self.course_xun_lei_url_list

    def get_course_url_relationship(self):
        for i in range(0, len(self.course)):
            relationship = {self.course_down_url_list[i]: self.course_xun_lei_url_list[i]}
            self.relationship[self.course[i]] = relationship
        return self.relationship

    def write_json(self):
        f = open('course.json', mode='w', encoding='utf-8')
        f.write(json.dumps(self.get_course_url_relationship(), ensure_ascii=False, indent=4))


if __name__ == '__main__':
    AnalysisUrl = AnalysisUrl()
    AnalysisUrl.get_course_down_url_list()
    AnalysisUrl.get_course_xun_lei_url_list()
    AnalysisUrl.write_json()

# -*- coding: UTF-8 -*-
from lxml import etree
import requests

from Req import Request


def find_xpath(self, htmlbody, xpathload):
    selector = etree.HTML(htmlbody)
    path = selector.xpath(xpathload)
    return path

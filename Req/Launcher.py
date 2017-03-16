import json
import threading

import time

from Req import Request

AnalysisUrl = Request.AnalysisUrl()
# AnalysisUrl = AnalysisUrl()
down_url_list = AnalysisUrl.get_course_down_url_list()
course_xun_lei_url_list = AnalysisUrl.get_course_xun_lei_url_list()


def json_course(file_name='course.json'):
    while True:
        try:
            f = open(file_name, encoding='utf-8')
            json_courses = json.loads(f.read(), encoding='utf-8')
            f.close()
            return json_courses
        except Exception as e:
            AnalysisUrl.get_course_url_relationship()
            AnalysisUrl.write_json(file_name)
            print(e)
            continue


course_new_url = {}


def need_down_url(file_name='course.json'):
    for i in range(0, len(AnalysisUrl.course)):
        local_url = json_course(file_name)[AnalysisUrl.course[i]][down_url_list[i]]
        link_url = course_xun_lei_url_list[i]
        new_url = []
        if len(local_url) == len(link_url):
            print(AnalysisUrl.course[i] + "------课程没有更新")
            continue
        else:
            for a in range(len(local_url), len(link_url)):
                new_url.append(link_url[a])
            course_new_url[AnalysisUrl.course[i]] = new_url
            continue
    return course_new_url


class JdThread(threading.Thread):
    def __init__(self, key):
        threading.Thread.__init__(self)
        self.key = key
        self.org_url = 'http://www.onlinesjtu.com/learningspace/learning/student/'

    def run(self):
        print(threading.currentThread().getName())

        for b in course_new_url[self.key]:
            xx = self.org_url + b
            print(str(time.ctime()) + self.key + xx)
            # print(threading.currentThread().getName())
            time.sleep(2)

if __name__ == '__main__':
    # json_course('coursesss.json')
    need_down_url()
    print(course_new_url)
    # print(course_new_url.keys()[0])
    a = []
    for i in course_new_url.keys():
        a.append(i)
    print(a)
    threads = []
    for i in a:
        j = JdThread(i)
        # j.start()
        # j.join()
        threads.append(j)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    # j = JdThread(a)
    # j.start()
    # j.join()
    print('..............')

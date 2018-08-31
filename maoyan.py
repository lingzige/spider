# coding=utf-8

import re
import urllib2
import json


class MaoYan(object):
    def pa(self, offset):
        url = 'http://maoyan.com/board/4?offset=' + str(offset)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        # html = requests.get(url, headers)
        # print(html.text)
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request).read()
        # re.S是匹配换行的标签
        ranks = re.findall(r'<dd>.*?board-index.*?>(.*?)</i>', response, re.S)
        # print(ranks)
        # print(rank)
        names = re.findall(r'<dd>.*?name.*?><a.*?>(.*?)</a>', response, re.S)
        # print(names)
        # images = re.findall(r'<img.*?board-img.*?data-src="(.*?)"', response, re.S)
        actors = re.findall(r'<p.*?star.*?>(.*?)</p>', response, re.S)
        times = re.findall(r'<p.*?releasetime.*?>(.*?)</p>', response, re.S)
        # print(time)
        # print(images)
        score1 = re.findall(r'<i.*?integer.*?>(.*?)</i>', response, re.S)
        score2 = re.findall(r'<i.*?fraction.*?>(.*?)</i>', response, re.S)
        # print(score2)
        # print(score)
        # 将获得的内容存储在字典中
        item = {}
        for rank, name, actor, time, score11, score22 in zip(ranks, names, actors, times, score1, score2):
            # 使用正则的目的是只提取出时间即可，而去掉包含的文字内容
            utime = re.search(r'([0-9-]+\w+)', time)
            # print(utime.group(1))
            item['rank'] = rank
            item['name'] = name
            # strip方法去掉空格
            item['actor'] = actor.strip()
            item['releasetime'] = utime.group(1)
            # 因为评分是在两个标签中的，所以将这两个标签中的内容相加即得到总评分
            item['score'] = score11 + score22
            self.write(item)

    def write(self, item):
        with open('result.txt', 'a')as f:
            # dumps方法是将字典形式的转化为json格式的
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def main(self):
        for i in range(10):
            offset = i * 10
            self.pa(offset)


if __name__ == '__main__':
    maoyan = MaoYan()
    maoyan.main()


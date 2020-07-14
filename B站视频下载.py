import os, sys, you_get, requests, json

class Download():
    def __init__(self):
        self.api = 'http://api.bilibili.com/x/web-interface/view?bvid='
        self.AV_url = 'https://www.bilibili.com/video/av'
        self.path = os.path.abspath('.')

    def video_download(self, BV_url):
        '''单独视频下载'''
        AV_url = self.AV_url + str(self.BV_to_AV(BV_url))
        sys.argv = ['you-get', '-o', self.path, AV_url]
        you_get.main()

    def BV_to_AV(self, url):
        '''BV转AV'''
        url = self.api + url.split('/')[-1]
        response = requests.get(url)
        html = response.content.decode('utf-8')
        data = json.loads(html)
        avid = data['data']['aid']
        return avid

if __name__ == "__main__":
    url = input('请输入url：')
    download = Download()
    download.video_download(url)
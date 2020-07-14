from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time, os, sys, you_get, re, requests, json

def browser(up_url):
    '''爬取UP所有视频并下载'''
    chrome_opt = Options()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs) # 不加载图片
    chrome_opt.add_argument('--headless')   # 无界面化.
    chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1920,1080') #设置页面大小
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get(up_url)

    try:
        urls = []
        wait = WebDriverWait(driver, 10)
        name = wait.until(EC.presence_of_element_located((By.NAME, 'h-name')))
        final_page = str(wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[3]/span[1]'))).text)
        num = int(re.search(r'\d+', final_page)[0])
        for _ in range(num):
            elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[1]')))
            for i in elems:
                url = i.get_attribute('href')
                url = BV_to_AV(url)
                urls.append(url)

            next_page = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '下一页')))
            if next_page:
                time.sleep(5)
                next_page.click()
                driver.refresh()
                print('next_page')
        
        path = os.path.abspath('.') + f'//{name}'
        [download(path, url) for url in urls]
    except Exception as e:
        print(e)

def download(path, url):
    '''下载'''
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()

def BV_to_AV(url):
    '''BV转AV'''
    api = 'http://api.bilibili.com/x/web-interface/view?bvid='
    url = api + url.split('/')[-1]
    response = requests.get(url)
    html = response.content.decode('utf-8')
    data = json.loads(html)
    avid = data['data']['aid']
    return avid
    
if __name__ == "__main__":
    # 下载UP所有视频
    up = input('请输入UP数字ID：') # 我的空间: 9174628
    up_url = f'https://space.bilibili.com/{up}/video'
    browser(up_url)
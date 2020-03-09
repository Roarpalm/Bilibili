from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time, os, sys, you_get

def browser(ip_url):
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
        final_page = int(wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[3]/li[6]'))).get_attribute('title').split(':')[-1])
        for _ in range(final_page-1):
            elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[1]')))
            for i in elems:
                url = i.get_attribute('href')
                urls.append(url)

            next_page = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '下一页')))
            time.sleep(5)
            next_page.click()
            driver.refresh()
            print('next_page')
        
        path = os.path.abspath('.') + f'//{name}'
        [download(path, url) for url in urls]
    except Exception as e:
        print(e)

def download(path, url):
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()

if __name__ == "__main__":
    # UP个人空间视频url
    # 日食记 = 'https://space.bilibili.com/8960728/video'
    up = input('请输入UP数字ID：')
    up_url = f'https://space.bilibili.com/{up}/video'
    browser(up_url)
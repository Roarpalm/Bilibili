from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import re

def browser(up_url):
    chrome_opt = Options()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs) # 不加载图片
    chrome_opt.add_argument('--headless')   # 无界面化.
    chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1920,1080') #设置页面大小
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get(up_url)

    titles = []
    links = []
    plays = []
    dates = []

    try:
        wait = WebDriverWait(driver, 10)
        final_page = str(wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-video-list"]/ul[3]/span[1]'))).text)
        num = int(re.search(r'\d+', final_page)[0])
        for _ in range(num):
            old_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/a[2]')))
            for i in old_titles:
                title = i.get_attribute('title')
                print(title)
                link = i.get_attribute('href')
                titles.append(title)
                links.append(link)
                
            old_plays = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/div/span[1]')))
            for i in old_plays:
                play = i.text
                plays.append(play)

            old_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="submit-video-list"]/ul[2]/li/div/span[2]')))
            for i in old_dates:
                date = i.text
                dates.append(date)
            next_page = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '下一页')))
            if next_page:
                sleep(5)
                next_page.click()
                driver.refresh()
                print('next_page')

    except Exception as e:
        print(e)

    all_list = list(zip(titles, links, plays, dates))
    with open('播放量.txt', 'w', encoding='utf-8') as f:
        for title, link, play, date in all_list:
            f.write(f'标题：{title}\n链接：{link}\n播放量：{play}\n日期：{date}\n\n')

if __name__ == "__main__":
    # 我的B站视频：'https://space.bilibili.com/9174628/video'
    up = input('请输入UP数字ID：')
    up_url = f'https://space.bilibili.com/{up}/video'
    browser(up_url)
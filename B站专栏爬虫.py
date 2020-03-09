from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import time

def browser(url):
    chrome_opt = Options()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs) # 不加载图片
    chrome_opt.add_argument('--headless')   # 无界面化.
    chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1920,1080') #设置页面大小
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get(url)

    titles = []
    links = []
    up_names = []
    scores = []
    reads = []

    try:
        wait = WebDriverWait(driver, 10)
        old_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="App"]/div/div[3]/ul/li/div/div/div[2]/div[1]/a')))
        for i in old_titles:
            title = i.get_attribute('title')
            link = i.get_attribute('href')
            titles.append(title)
            links.append(link)

        old_up_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="App"]/div/div[3]/ul/li/div/div/div[2]/div[1]/div[2]/a[1]/span[2]')))
        for i in old_up_names:
            up_name = i.text
            up_names.append(up_name)

        old_scores = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="App"]/div/div[3]/ul/li/div/div/div[2]/div[2]/label[1]')))
        for i in old_scores:
            score = i.text
            scores.append(score)

        old_reads = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="App"]/div/div[3]/ul/li/div/div/div[2]/div[1]/div[2]/span[1]')))
        for i in old_reads:
            read = i.text
            reads.append(read)

    except Exception as e:
        print(e)
    
    new_list = list(zip(titles, links, up_names, scores, reads))
    if url.split('=')[-1] == '1':
        filename = '月榜'
    if url.split('=')[-1] == '2':
        filename = '周榜'
    if url.split('=')[-1] == '3':
        filename = '昨天榜'
    if url.split('=')[-1] == '4':
        filename = '前天榜'
    with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
        for title, link, up_name, score, read in new_list:
            f.write(f'标题：{title}\n链接：{link}\nUP：{up_name}\n综合得分：{score}\n阅读：{read}\n\n')

if __name__ == "__main__":
    list_url = [f'https://www.bilibili.com/read/ranking#type={i}' for i in range(1,5)]
    with ThreadPoolExecutor(max_workers=4) as e:
        [e.submit(browser, url) for url in list_url]
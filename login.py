from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import base64
import random

username = ''
password = ''
driver = webdriver.Chrome()


class Start:
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = driver
        self.wait = WebDriverWait(self.browser, 20)
        self.name = username
        self.pw = password

    def get_login_button(self):
        """
        获取初始登录按钮
        :return: 按钮对象
        """
        button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'btn') and contains(@class, 'btn-login')]")))
        return button

    def get_slider_button(self):
        """
        获取拖动碎片的地方
        :return: 拖动对象
        """
        sliderbutton = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_slider_button']")))
        return sliderbutton

    def get_login_input(self):
        """
        获取登陆输入框(用户名/密码)
        :return: 输入框对象
        """
        user_login = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='login-username']")))
        pw_login = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='login-passwd']")))
        return user_login, pw_login

    def save_pic(self, data, filename):
        """
        解码获取到的base64再写入到文件中，保存图片
        :return:
        """
        data = data.split(',')[1]
        data = base64.b64decode(data)
        with open(filename, 'wb') as f:
            f.write(data)

    def get_pic(self):
        """
        获取无缺口图片和有缺口图片
        :return: 图片对象
        """
        # 图片对象的类名
        # 首先需要这个东西已经出现了，我们才能去执行相关的js代码
        picName = ['full.png', 'slice.png']
        className = ['geetest_canvas_fullbg', 'geetest_canvas_bg']
        # canvas标签中的图片通过js代码获取base64编码
        for i in range(len(className)):
            js = "var change = document.getElementsByClassName('"+className[i]\
                 + "'); return change[0].toDataURL('image/png');"
            im_info = self.browser.execute_script(js)
            self.save_pic(im_info, picName[i])

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素点是否是相同
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :param x: 像素点的x坐标
        :param y: 像素点的y坐标
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 40
        if abs(pixel1[0] - pixel2[0]) < threshold \
                and abs(pixel1[1] - pixel2[1]) < threshold \
                and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        # 这个可以自行操作一下，如果发现碎片对不准，可以调整
        left = 10
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param self:
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 因为老对不的不准确，所以自行调整一下distance
        distance = distance - 9
        # 减速阈值 -> 也就是加速到什么位置的时候开始减速
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def test(self):
        # 输入用户名和密码
        self.browser.get(self.url)
        user_login, pw_login = self.get_login_input()
        user_login.send_keys(self.name)
        pw_login.send_keys(self.pw)
        # 点击按钮对象
        button = self.get_login_button()
        button.click()
        # 保存图片
        time.sleep(3)
        self.get_pic()
        image1 = Image.open('full.png')
        image2 = Image.open('slice.png')
        left = self.get_gap(image1, image2)
        #track = self.get_track(left)
        slider = self.get_slider_button()
        self.move_to_gap(slider, left, self.browser)

    def move_to_gap(self, slider, left, browser):
        """
        拖动滑块到缺口处
        :param self:
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
        # click_and_hold()点击鼠标左键，不松开
        ActionChains(self.browser).click_and_hold(slider).perform()

        left = left - 9
        
        left += 10
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = left * 3 / 5  # 减速阀值
        back_tracks = [-3, -2, -2, -2, -1]
        while current < left:
            if current < mid:
                a = 6  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        for x in forward_tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(self.browser).pause(random.uniform(0.6, 0.9))
        for x in back_tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        
        # release()在某个元素位置松开鼠标左键
        ActionChains(self.browser).release().perform()


Start().test()
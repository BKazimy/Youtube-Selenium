from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import common
import dotenv
import os
import time

dotenv.load_dotenv()


def main():
    net_speed = NetSpeedTwitter()
    speed = net_speed.get_site_speed()

    print(speed)

    tweet = f"My internet speed report:\ndownload speed: {speed[0]} mb/s\nupload speed: {speed[1]} mb/s\nping: {speed[2]}ms\nISP: #{speed[3]} "

    net_speed.twitter_login()
    net_speed.twitter_tweet(tweet)


class NetSpeedTwitter:


    def __init__(self) -> None:
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome()#options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 60)


    #_internet speed tester() -> [download_speed, upload_speed, ping, ISP]
    def get_site_speed(self):
        #_get the website
        url = 'https://www.speedtest.net/'
        self.driver.get(url=url)
        time.sleep(2)

        #_cookie confirmer
        try:
            time.sleep(3)
            self.btn_locator('button#onetrust-accept-btn-handler').click()
        except:
            pass

        #_locating the clickable start butn
        start = self.btn_locator('a.js-start-test')

        #_call js function for running the test.
        self.driver.execute_script("arguments[0].click();", start)

        #_wait for connection
        self.wait.until(expected_conditions.invisibility_of_element_located((common.by.By.CSS_SELECTOR, 'div.connecting-message')))
        time.sleep(5)

        #_wait untill the speed test is running
        self.wait.until(expected_conditions.invisibility_of_element_located((common.by.By.CSS_SELECTOR, 'canvas.gauge-speed-text')))

        #_get isp with xpath_locator
        isp = self.xpath_locator('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[4]/div/div[2]/div/div/div/div[2]')

        #_get other parameters
        download = self.driver.find_element(common.by.By.CSS_SELECTOR, 'span.download-speed')
        upload = self.driver.find_element(common.by.By.CSS_SELECTOR, 'span.upload-speed')
        ping = self.driver.find_element(common.by.By.CSS_SELECTOR, 'span.ping-speed')

        return [download.text, upload.text, ping.text, isp.text]


    #_twitter post creator(tweet_content) -> None
    def twitter_tweet(self, tweet_phrase):
        input_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
        post_btn_css = '#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010.r-18u37iz > main > div > div > div > div.css-175oi2r.r-14lw9ot.r-jxzhtn.r-13l2t4g.r-1ljd8xs.r-1phboty.r-16y2uox.r-184en5c.r-61z16t.r-11wrixw.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div > div.css-175oi2r.r-14lw9ot.r-184en5c > div > div.css-175oi2r.r-14lw9ot.r-1h8ys4a > div:nth-child(1) > div > div > div > div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-1h8ys4a.r-1bylmt5.r-13tjlyg.r-7qyjyx.r-1ftll1t > div.css-175oi2r.r-14lw9ot.r-jumn1c.r-xd6kpl.r-gtdqiz.r-ipm5af.r-184en5c > div:nth-child(2) > div > div > div > div.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-19u6a5r.r-2yi16.r-1qi8awa.r-ymttw5.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l > div'

        #_type the tweet content
        tweet_input = self.xpath_locator(input_xpath)
        self.input_filler(tweet_input, tweet_phrase)

        #_tweet content
        self.btn_locator(post_btn_css).click()


    #_login to twitter account() -> None
    def twitter_login(self):
        password = os.getenv('TWITTER_PASSWORD')
        email = os.getenv('TWITTER_EMAIL')
        user = os.getenv('TWITTER_USER')
        url = "https://twitter.com/"
        
        #_open twitter.com
        self.driver.get(url)

        #_locating te log in button and click
        login_btn_css = '#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010 > main > div > div > div.css-175oi2r.r-tv6buo.r-791edh.r-1euycsn > div.css-175oi2r.r-1777fci.r-nsbfu8.r-1qmwkkh > div > div.css-175oi2r > div.css-175oi2r.r-2o02ov > a'        
        login_btn = self.btn_locator(login_btn_css)
        login_btn.click()

        #_locating mail input
        mail_input_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
        element = self.xpath_locator(mail_input_xpath)
        self.input_filler(element, email)
        element.send_keys(common.keys.Keys.RETURN)

        #_looking for username input field
        username_input_xpath =  '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
        element = self.xpath_locator(username_input_xpath)
        self.input_filler(element, user)
        element.send_keys(common.keys.Keys.RETURN)

        #_looking for password field
        password_input_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
        element = self.xpath_locator(password_input_xpath)
        print('')
        self.input_filler(element, password)
        element.send_keys(common.keys.Keys.RETURN)


    #_element locator by xath(xpath_address) -> element_object
    def xpath_locator(self, xpath_address):
        #_find and locate desired element
        return self.wait.until(expected_conditions.presence_of_element_located((common.by.By.XPATH, xpath_address)))
    

    #_clickable button locator(css_address) -> clickable_object
    def btn_locator(self, css_selector):
        #_wait and locate the desired clickable button
        return self.wait.until(expected_conditions.element_to_be_clickable((common.by.By.CSS_SELECTOR, css_selector)))


    #_input filler(input_obj, str(input_value) -> True|False
    def input_filler(self, element_obj, input_value):
        
        #_type the passed value to target input one character at a time
        try:
            [element_obj.send_keys(i) for i in input_value]
            return True
        except:
            return False


if __name__=="__main__":
    main()
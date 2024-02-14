from selenium import webdriver
from selenium.webdriver import common


def main():
    url = "https://www.livechat.com/typing-speed-test/#/"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()

    driver.get(url=url)

    test_input = driver.find_element(common.by.By.CSS_SELECTOR, 'div#test-input')

    score = word(driver, test_input)
    print(f"\nTimes up\nYou scored: {score.text}")


def word(driver, test_input):
    while True:
        word = driver.find_element(common.by.By.CSS_SELECTOR, 'span.u-pl-0')
        print('>> ' + word.text)

        for i in word.text:
            test_input.send_keys(i)
        try:
            score = driver.find_element(common.by.By.CSS_SELECTOR, '#app > div > div.o-container > span > div > div > div > div > div.u-bg-gray-900.u-Pt-md.u-Px-sm.u-Pb-xs > div > div:nth-child(2) > p > span.u-text-p6-bold.u-bg-accent.u-rounded-sm.u-px-2xs')
            return score
        except:
            pass
        test_input.send_keys(common.keys.Keys.SPACE)


if __name__=="__main__":
    main()

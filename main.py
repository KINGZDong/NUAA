from selenium import webdriver
import time
from OCR import MyOCR
from Send_email import SendEmails

browser = webdriver.Edge("/usr/local/bin/msedgedriver")
browser.implicitly_wait(20)
browser.maximize_window()
# 登录
browser.get("https://m.nuaa.edu.cn/ncov/wap/default/index?t=20210430")
browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/input').send_keys('SX2007084')
browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/input').send_keys('St201511')
browser.find_element_by_xpath('//*[@id="app"]/div[3]').click()
time.sleep(5)
# 提交信息
browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[4]/ul/li[5]/div/div/div[2]/span[1]/i').click()
browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[4]/ul/li[12]/div/div/div[1]/span[1]').click()
browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[4]/ul/li[13]/div/div/div[1]/span[1]').click()
location = browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[4]/ul/li[7]/div/input')
location.click()
time.sleep(5)
location.screenshot('location.png')
# 识别地点
ocr = MyOCR()
location_info = ocr.pic2text(img_path='location.png')['words']
# 设置常用地点，如果不是常用地点则提示
common_locations = ['江苏省', '江西省', '上海市', '陕西省', '江西省']
if location_info[0:3] in common_locations:
    content = "在常用地点，打卡地点为" + location_info  # 正文
else:
    content = "不在常用地点，打卡地点为" + location_info  # 正文

browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[5]/div/a').click()
browser.find_element_by_xpath('//*[@id="wapcf"]/div/div[2]/div[2]').click()
# 发邮件
send_email = SendEmails()
try:
    browser.find_element_by_xpath('//*[@id="wapat"]/div/div[2]/div').click()
    content = '打卡成功啦！ ' + content
    send_email.Send(content)
except:
    content = '信息提交失败！' + content
    send_email.Send(content)
finally:
    browser.quit()



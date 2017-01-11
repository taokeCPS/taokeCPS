# -*- coding: utf-8 -*-

import chardet,requests,sys,os,time,base64,json

from selenium import webdriver

#头部参数
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://pub.alimama.com/myunion.htm',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

#1. 读取cookies文件,如果存在则获取它
def load():
    try:
        with open('cookies.json') as f:
            cookies = json.load(f)
        return cookies
    except FileNotFoundError:
        return None

#2. 验证Cookies值,成功则输出名字，失败输出空值
def validate():
    cookies = load()

    url = 'http://pub.alimama.com/common/getUnionPubContextInfo.json'
    s = requests.session()

    html = s.get(url, headers=headers, cookies=cookies, timeout=10)
    result = html.json()

    try:
        # 成功读取用户名
        name = result['data']['mmNick']
        # print(name)
        return name
    except:
        # 当前Cookies失效
        return None

#3. 不存在Cookies文件或Cookies已失效，则更新 Cookies 文件并输出最新 Cookie 的值
def update():
    #driver = webdriver.Chrome(r"C:\Python35\selenium\webdriver\chrome\chromedriver.exe")
    # driver = webdriver.Chrome(r'/Users/Chao/bin/chromedriver') # Mac版本
    driver = webdriver.Chrome(r'/usr/local/chromedriver-Linux64')
    # loginurl = 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true'
    loginurl = 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://pub.alimama.com/common/getUnionPubContextInfo.json'
    driver.get(loginurl)
    driver.set_window_size(500,300)
    time.sleep(1)

    # 点击用户名登陆
    driver.find_element_by_xpath('//*[@id="J_Quick2Static"]').click()
    # print('✔ 恭喜，点击用户名登陆按钮成功！')
    time.sleep(1)

    # 输入用户名
    driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys('CPS')
    # print('✔ 恭喜，用户名输入成功！')
    time.sleep(1)

    # 输入密码
    driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys('TaoKe')
    # print('✔ 恭喜，密码输入成功！')
    time.sleep(1)

    # 点击登陆按钮
    driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
    # print ('✔ 恭喜，点击登陆按钮成功！')
    time.sleep(1)



    #页面标题没有‘验证’字样
    if '验证' not in driver.title:
        time.sleep(1)

    #需要输入手机验证码
    else:
        print('✘ Maybe you need type in the sms code.')
        time.sleep(20)
        # update()

    # 获得cookie2信息
    cookie2 = driver.get_cookie('cookie2')['value']
    #获取token值
    token = driver.get_cookie('_tb_token_')['value']

    #
    # print ('✔ 恭喜，成功获取到最新到Cookies值！')
    # print(cookie2)

    # 组装Cookies
    cookies = {
        'cookie2':cookie2,
        '_tb_token_':token
        }
    with open('cookies.json','w',encoding='utf-8') as f:
        f.write(json.dumps(cookies))

    #关闭窗口
    try:
        driver.quit()
    except:
        print('关闭出错')

    return cookies

# 输出欢迎信息
def login():
    name = validate()
    if name:
        # print('\n♛ 主人,欢迎回来,江湖一直有你的传说.  ┊┊  %s  ┊┊ \n' % name)
        cookies = load()
        return cookies
    else:
        print("\n✎ 主人，需要更新Cookies，即将打开浏览器窗口，请耐心等待...")
        time.sleep(0.5)
        cookies = update()
        return cookies


if __name__ == "__main__":
        login()
        # update()



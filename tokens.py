# -*- coding: utf-8 -*-



import requests,login

#1. 获取高佣／普通淘口令
def TaoToken(itemid,pid):

    headers = login.headers
    cookies = login.load()

    #提交PID
    pid_list = pid.split('_')
    siteid = pid_list[2] #推广渠道
    adzoneid = pid_list[3] #推广位ID

    #普通商品提交参数
    normal_para = {
        'auctionid':'%s' %itemid, #宝贝ID
        'adzoneid':'%s' %adzoneid, #推广位PID
        'siteid':'%s' %siteid, #推广渠道
        'scenes':1, #普通商品推广场景 ，高佣为3
    }

    #高佣商品提交参数
    gaoyong_para = {
        'auctionid':'%s' %itemid, #宝贝ID
        'adzoneid':'%s' %adzoneid, #推广位PID
        'siteid':'%s' %siteid, #推广渠道
        'scenes':3, #普通商品推广场景 ，高佣为3
        'channel':'tk_qqhd', #高佣商品必须参数
    }

    #校验当前商品是否为高佣活动商品
    checkurl = 'http://pub.alimama.com/items/channel/qqhd.json?channel=qqhd&q=https://item.taobao.com/item.htm?id=%s' %itemid
    html = requests.get(url = checkurl, headers=headers)
    check_result = html.json()['data']['pageList'] #高佣计划信息
    # print (check_result)

    if check_result == None:
        # 不存在高佣计划
        param = normal_para
        # print('✘ 当前宝贝不存在高佣计划。')
        # 准备申请定向计划

    else:
        #存在高佣计划
        param = gaoyong_para
        # print('✔✔✔ 当前宝贝存在高佣计划。')


    i = 0
    while i < 3:

        #提取淘口令（和优惠券链接）
        url = 'http://pub.alimama.com/common/code/getAuctionCode.json'

        html = requests.get(url, headers=headers, cookies=cookies, params=param)

        # Status 200则cookies未过期

        if html.status_code == 200 and html.json()['data']:

            r = html.json()

            # print(r)

            if r['data']['couponLink']:
                #当前宝贝存在优惠券链接,直接输出优惠券淘口令
                # print('✔✔✔ 当前宝贝有优惠券！')
                TaoToken = r['data']['couponLinkTaoToken'] #优惠券淘口令
                couponLink = r['data']['couponLink'] #优惠券链接（已加密，可解析）

            else:
                #当前宝贝不存在优惠券链接，直接输出商品淘口令
                # print('✘ 当前宝贝不存在优惠券！')
                TaoToken = r['data']['taoToken']
                couponLink = ''

            return TaoToken,couponLink

        #cookies过期
        else:

            #更新cookies
            login.update()
            cookies = login.load()

    i += 1

    # else:
    #     print('自动登录失败超过3次。')

    #     # need to fix
    #     return (None, None, None)


if __name__ == "__main__":
    TaoToken,couponLink = TaoToken('527976555588','mm_118081706_19234461_67230599')
    if couponLink != '':
        # print ('优惠券链接：%s' %couponLink)
        print ('带优惠券的淘口令：%s'%TaoToken)
    else:
        print('不带优惠券的商品淘口令:%s' %TaoToken)

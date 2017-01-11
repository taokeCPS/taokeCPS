# -*- coding: utf-8 -*-


import requests,login,time,tokens,os

#1. 下载宝贝图片
def get_image(itemid):
    headers = login.headers
    r = requests.get('https://scenes.taobao.com/content/json/getItemDetailByUrl.do?url=http://item.taobao.com/item.htm?id=%s&appKey=cps' % itemid, headers=headers)
    image = r.json()['jsonObject']['itemDetail']['coverUrl']
    url = 'http:' + image + '_400x400.jpg'
    r = requests.get(url, stream=True)

    #不存在img文件夹则自动创建
    if not os.path.isdir('img/'):
        os.mkdir('img/')

    pic = 'img/' + str(itemid) + '.jpg'

    with open(pic, "wb") as f:
        f.write(r.content)
    return pic

#2. 根据宝贝ID和PID组装发送消息需要的内容
def get_content(itemid,pid):

    headers = login.headers

    #获取淘口令（与优惠券链接）
    TaoToken,couponLink = tokens.TaoToken(itemid,pid)

    #包含优惠券信息
    if couponLink != '':

        url = couponLink.replace('coupon/edetail','cp/coupon') #转换为json信息页面
        html = requests.get(url, headers=headers)
        r = html.json()['result']
        startFee = r['startFee'] #优惠券使用门槛
        Price = r['item']['discountPrice'] #商品售价
        nice = 1 if startFee <= Price else 0 #优惠券使用门槛大于售价的都是耍流氓
        amount = int(r['amount']) #优惠券金额
        EndTime = r['effectiveEndTime'] #优惠券活动结束时间
        picUrl = r['item']['picUrl'] #宝贝主图地址
        title = r['item']['title'] #宝贝标题
        tmall = '【天猫正品】' if r['item']['tmall'] == '1' else '' #是否天猫
        freeShip = '【包邮】' if r['item']['postFree'] == '1' else '' #是否包邮
        sale = r['item']['biz30Day'] #30天销量
        nicePrice = int(Price - amount ) #券后价
        recommend = '[Heart]【群主推荐】[Heart]\n' if amount / Price > 0.5 else '' #优惠力度大于50%则力荐之

        #组装有券商品发送内容
        content = (recommend + tmall + title + '\n[Packet]本群独享 Ұ ' + str(amount) +
                    '元优惠,先领券后下单! \n[Packet]原价 Ұ ' + str(Price) + ',券后价 Ұ ' + str(nicePrice) + freeShip
                    + '\n复制这条信息,打开[手机淘宝]即可领券下单\n' + TaoToken + '\n[Rose]本群专享优惠,已抢'
                    + str(sale) + '件!')

    #不含优惠券信息
    else:
        url = 'http://pub.alimama.com/items/search.json?q=https://item.taobao.com/item.htm?id=%s' %itemid
        html = requests.get(url, headers=headers)
        r = html.json()['data']['pageList'][0]

        title = r['title'] #商品标题
        price = r['zkPrice'] #商品价格
        sale = r['biz30day'] #30天销量
        tmall = '【天猫正品】' if r['userType'] == '1' else '' #天猫为1，C店为0

        #组装无券商品发送内容
        content = ( tmall + title + '\n[Packet]复制这条信息,打开[手机淘宝]即可领券下单\n'
        + TaoToken + '\n[Rose]本群专享优惠，已抢' + str(sale) + '件!')


    return content


if __name__ == "__main__":
        # print (get_content('521379829157','mm_118081706_19234461_67230599'))
        get_image('521379829157')

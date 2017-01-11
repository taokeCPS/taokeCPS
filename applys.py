# -*- coding: utf-8 -*-



import requests,login

#1. 检查宝贝是否参加鹊桥高佣计划，输入宝贝ID，输出True（存在），False（不存在）
def check_gaoyong(itemid):
    url = 'http://pub.alimama.com/items/channel/qqhd.json?q=https://detail.tmall.com/item.htm?id=%s' %itemid
    headers = login.headers
    html = requests.get(url, headers=headers)
    r = html.json()['data']
    gaoyong_status = r['head']['status'] #高佣计划是否存在，“OK”则存在，“NORESULT”则不存在

    #存在高佣计划
    if gaoyong_status == 'OK':
        eventRate = r['pageList'][0]['eventRate'] #高佣计划佣金比例
        print('❤ 当前宝贝在鹊桥计划中,佣金比例： %.2f%% 不需要申请定向。' %eventRate)
        return True

    #不存在高佣计划
    elif gaoyong_status == 'NORESULT':
        print('✘ 当前宝贝不存在高佣计划。')
        return False

#2. 检查宝贝是否存在定向计划,输入宝贝ID，输出True（存在），False（不存在）
def check_special(itemid):
    url = 'http://pub.alimama.com/items/search.json?q=https://item.taobao.com/item.htm?id=%s' %itemid
    headers = login.headers
    html = requests.get(url, headers=headers)
    r = html.json()['data']['pageList'][0]
    special_status = r['includeDxjh'] #是否包含定向计划

    #存在定向计划
    if special_status == 1:
        return True

    #不存在定向
    elif special_status == 0:
        return False

#3. 根据宝贝ID获取最高佣金的定向计划ID,定向 > 通用，则输出定向计划ID，否则输出None
def get_campaign_id(itemid):
    url = 'http://pub.alimama.com/items/search.json?q=https://item.taobao.com/item.htm?id=%s' %itemid
    headers = login.headers
    html = requests.get(url, headers=headers)
    r = html.json()['data']['pageList'][0]

    tkRate = r['tkRate'] #当前宝贝通用计划佣金比例
    SpecialRate = r['tkSpecialCampaignIdRateMap'] #定向计划字典信息
    includeDxjh = r['includeDxjh'] #是否包含定向计划

    for k,rate in set(SpecialRate.items()):
        rate = float(rate)
        SpecialRate[k] = rate

    #获取佣金比例最高的定向计划
    CampaignID,highrate = max(zip(SpecialRate.keys(),SpecialRate.values()))

    if highrate >= tkRate:
        #定向计划佣金比例大于等于通用计划
        return CampaignID

    else:
        #定向计划最高的佣金比例都低于通用
        # print('ㄨ 请注意，发现坑爹商家，定向佣金低于通用。')
        return None


#3. 获取定向计划KeeperID，成功则输出KeeperID，失败输出None
def get_keeper_id(itemid):
    url = 'http://pub.alimama.com/pubauc/getCommonCampaignByItemId.json?itemId=%s'%itemid
    headers = login.headers
    cookies = login.login()

    html = requests.get(url, headers=headers, cookies=cookies)
    result = html.json()['data'][0]
    KeeperID = result['ShopKeeperID'] #KeeperID

    return KeeperID

    # # 如果成功获取到定向计划
    # for result in results['data']:
    #     #CampaignID,ShopKeeperID,AvgCommission,manualAudit
    #     commissionRate = result['commissionRate'] #单品佣金比例
    #     CampaignID = result['CampaignID'] #定向计划ID
    #     ShopKeeperID = result['ShopKeeperID'] #KeeperID
    #     AvgCommission = result['AvgCommission'] #平均佣金比例
    #     manualAudit = result['manualAudit'] #是否手动审核，手动=1，自动=0
    #     Exist = result['Exist'] #是否已申请 true为已申请,false为尚未申请
    #     print('申请状态。')
    #     print (Exist)
    #
    #     # ExistStatus = 2为通过,1为审核中，
    #     ExistStatus = result['ExistStatus'] if 'ExistStatus' in result.keys() else '' #如果审核状态存在则输出审核结果
    #
    #     # print('CampaignID = %d'%CampaignID)
    #
    #     #找到之前搜索到的最高佣金比例定向计划ID,且尚未申请该计划
    #     if CampaignID == str(CampaignID) and Exist is False:
    #         print('keepid = %s'%ShopKeeperID)
    #         break
    #         return ShopKeeperID
    #     else:
    #         print('没找到相同ID的定向。')
    #         return None


#4. 申请最高佣金比例的定向计划,输入宝贝ID，输出 True，False，None
def enroll(itemid):

    headers = login.headers
    cookies = login.login()
    token = cookies['_tb_token_']

    CampaignID = get_campaign_id(itemid)
    KeeperID = get_keeper_id(itemid)

    apply_reason = '专业淘客团队，技术实力超群，专营精准微信群淘客模式，日出千单，诚意与商家合作，有意请联系，谢谢。'
    data = {
         'campId': CampaignID,
         'keeperid': KeeperID,
        'applyreason':apply_reason,
        '_tb_token_':token
    }
    # print (CampaignID,KeeperID)
    url = 'http://pub.alimama.com/pubauc/applyForCommonCampaign.json'
    r = requests.post(url, headers=headers, cookies=cookies, data=data)
    r = r.json()

    if r['ok'] == True and r['info']['ok'] == True:
        #定向计划申请成功
        return True
    else:
        if '已经' in r['info']['message']:
            #已申请过当前计划，已通过／正在审核，后期会加判断
            return None
        elif '失效' in r['info']['message']:
            #提示页面失效，cookies过期，或者token值出错
            return False

#5. 判断并申请最高佣金，输入itemid，输出结果，（申请成功）True，（申请失败／需要审核）False，（不需要申请）None
def apply_rate(itemid):

    #如果存在鹊桥高佣计划，或者不存在定向，返回None
    if check_gaoyong(itemid) is True or check_special(itemid) is False:
        # print('❤ 当前宝贝在鹊桥计划中，或者不存在定向。')
        return None

    #没有鹊桥高佣且存在定向计划
    else:

        if get_campaign_id(itemid) is None or get_keeper_id(itemid) is None:
            print('ㄨ 请注意，发现坑爹商家，定向低于通用，已跳过申请。')
            return None

        else:
            #成功获取到定向ID和KeeperID
            print('☻ 请注意，发现一个牛逼定向计划，正在大力申请中，请稍候...')

            #开始申请最高佣金的定向计划
            result = enroll(itemid)

            if result is True:
                #申请成功
                print('✔ 成功申请了最高佣金的定向计划。')

            elif result is False:
                #申请失败，cookies过期，token出错
                print('✘ 哦不，申请失败，可能是Cookies过期，或者Token值失效了。')

            elif result is None:
                #已经申请了，或者已通过
                print ('☁ 主人，当前定向计划已经申请过了。')

if __name__ == "__main__":
    apply_rate('538729266551')

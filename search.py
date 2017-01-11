# -*- coding: utf-8 -*-

'''
@高佣搜索失败则切换普通搜索
@用法：search(关键词) 调用，随机返回一个最多包含3个商品ID的list
'''

import requests,random

#1. 采集鹊桥活动商品
def gaoyong_search(keyword):
	url = 'http://pub.alimama.com/items/channel/qqhd.json'
	payload = {
	'q':'%s'%keyword,
	'sortType':7, #按月支出佣金排序
	'userType':1, #天猫
	'dpyhq':1, #有店铺优惠券
	'channel':'qqhd', #鹊桥活动商品，必须
	'perPageSize':80 #每页商品数量
	}
	r =  requests.get(url,params=payload)
	# print(r.url) #打印搜索URL
	r = r.json()['data']
	number = r['head']['docsfound'] #搜索到的商品数量
	print('高佣数量：' + str(number))

	if number == None: #查无商品,则切换普通搜索
		# print('高佣计划查无数据，切换普通搜索ing...')
		return None
	else:
		# print('高佣计划采集完毕，开始进行普通搜索。')
		#print(r['pageList'])
		return r['pageList']

#2. 采集超级搜索普通类商品
def normal_search(keyword):
	url = 'http://pub.alimama.com/items/search.json'
	payload = {
	'q':'%s'%keyword,
	'sortType':7, #按月支出佣金排序
	'userType':1, #天猫
	'dpyhq':1, #有店铺优惠券
	'perPageSize':80 #每页商品数量
	}
	r =  requests.get(url,params=payload)
	# print(r.url) #打印搜索URL
	r = r.json()['data']
	number = r['head']['docsfound'] #搜索到的商品数量
	print('普通数量：' + str(number))

	if number is None: #查无商品
		return None
	else:
		return r['pageList']

#3. 随机返回3个商品ID
def get_itemids(results):

		# 准备获取采集到的宝贝信息
		itemids = []
		if results:
			for result in results:
				itemid = result['auctionId'] #宝贝ID
				# print(itemid)
				# TkRate = result['tkRate'] #佣金比例
				Price = result['zkPrice'] #商品售价
				Coupon = result['couponAmount'] #优惠券额度
				StartFee = result['couponStartFee'] #使用门槛
				CouponRate = round(((Price-Coupon)/Price*100),2)

				# 剔除优惠券使用门槛大于商品售价 或者 优惠券额度为 0 的坑爹商品
				if StartFee <= Price and Coupon != 0:
					itemids.append({'itemid': itemid,'CouponRate': CouponRate})
					# 暂时默认30天支出佣金顺序输出TOP 5，后续做进一步筛选
					# items['itemid'] = itemid
					# items['TkRate'] = TkRate
					# items['CouponRate'] = CouponRate

		else:
			print("flag_5");
			return None,None

			#随机输出3个商品,少于3个则全部输出，为0则输出None
		itemids = sorted(itemids, key=lambda s: s['CouponRate'])
		infos = [];
		if itemids == []: return None,None

		for itemid in itemids: infos.append(itemid['itemid'])
		# print(infos)
		number = len(infos)

		print('过滤后数量：%d'%number)
		infos = infos[:6]
		idnumber = 3 if len(infos) > 3 else len(infos)
		sendinfo = random.sample(infos,idnumber)

		if  number >= 15:
			return sendinfo,len(infos)
		elif number < len(infos):
			return sendinfo,number
		else:
			return sendinfo,len(infos)


def search(keyword):
	# 运行高佣采集计划
	gao = gaoyong_search(keyword)
	if gao == None :
		normal = normal_search(keyword)
		if normal != None :
			return get_itemids(normal)
		else : return None
	else:
		# 运行通用采集计划
		# normal = normal_search(keyword)
		# if normal != None :
		# 	return get_itemids(gao+normal)
		# else : return get_itemids(gao)
		return get_itemids(gao)

if __name__ == "__main__":
        print(search('蕾丝吊带衫'))

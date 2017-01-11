# -*- coding: utf-8 -*-



import itchat,time,os,sys
import search,login,content,chatroom,tokens,applys


from itchat.content import TEXT

i = 0

@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=False, isMpChat=False)


def simple_reply(msg):

		# 接收用户发送的消息
		message = msg['Content']

		print(message)

		# 判断发送内容格式是否合法并回复消息 '1#关键词'
		reply_message = ''

		#包含 # 号才回复消息:
		if '#' in message:

			#指令有误则提示出错
			if not message.split('#')[0].isdigit() or message.split('#')[1] == '':

				reply_message = '[Moue]亲，当前发送指令有误，请检查后重新发送。'

				# 给用户发送确认消息
				itchat.send(reply_message, msg['FromUserName'])

			#指令无误则开始后续工作
			else:

				reply_message = '[Determined]亲，已收到你的查询请求，请稍候...'

				# 给用户发送确认消息
				itchat.send(reply_message, msg['FromUserName'])


				# 切分群号与搜索关键词
				number,keyword = message.split('#')



				if keyword != '':
					# with open('pid.txt') as f:
					# 	content = f.read()
					# pid = content.split('\n')[int(number)]
					# print(pid)
					# print('\n✈  %s 群的查询关键词:%s ' % (number,keyword))

					#获取搜索结果的宝贝ID
					itemids,idnumber = search.search(keyword)

					# get username and pid
					username,pid = chatroom.get_chatroom_name(number)
					# print(username)
					# print(pid)

					if itemids == None:
						#搜索到的宝贝ID列表为空
						reply_content = '[Whimper]抱歉，当前关键词查询结果为空，请尝试一下替换其他关键词，谢谢。'
						itchat.send(reply_content, msg['FromUserName'])

					else:
						#正常搜索到宝贝ID列表
						if itemids:
							for k,itemid in enumerate(itemids):
								item_content = content.get_content(itemid,pid) #获取完整广告内容
								applys.apply_rate(itemid) #自动申请定向计划

								if item_content:

									try:
										# 发送主图
										pic = content.get_image(itemid)
										itchat.send('@img@%s' % pic, username)
										itchat.get_msg()
									except Exception as e:
										print("flag_2");
										print(Exception, ":", e)
									time.sleep(5)

									try:
										# 发送广告文案
										itchat.send(item_content, username)
										itchat.get_msg()
									except Exception as e:
										print("flag_3");
										print(Exception, ":", e)
									time.sleep(5)


									# 删除已下载的图片
									os.remove(pic)

									print('✔ 亲，已成功发送了 %d 条宝贝信息'%(k+1))

								else:
									# continue # content is None,need to fix
									error_message = '小贝出了点小问题，请电话联系管理员,马上为您修复。'
									itchat.send(error_message, msg['FromUserName'])
									sys.exit()

						else:
							print("flag_4");

						print('\n')

						global i
						i = i + 1

						print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

						print ('\n█▇▆▅▄▃▂  From',  number  ,'群, Keyword:',keyword,'Totle times:  ',i,'  次查询请求。 ▂▃▄▅▆▇█\n')


						# 给用户发送成功消息

						success_message = '[Joyful]宝贝信息已发送到您的群，请查看。'

						itchat.send(success_message, msg['FromUserName'])

itchat.auto_login(enableCmdQR=0,hotReload=True)
itchat.run()

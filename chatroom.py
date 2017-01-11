
#coding=utf8
import itchat

# never open this again,you will send the message for many many times
# itchat.auto_login(hotReload=True)

def get_chatroom_name(number):
	
	owner_name = {
		'0':{'uin':'','name':'CPS','chatroom':'优惠0群','pid':'pid'},
		}
	number = str(number)
	if number == None: return None
	if number not in owner_name.keys(): return None
	name = owner_name[number]['chatroom']
	pid = owner_name[number]['pid']
	chatrooms = itchat.search_chatrooms(name)
	if not chatrooms: 
		return None
	else:
		try:
			chatrooms = itchat.search_chatrooms(name)[0]
			# chatroomprint(chatrooms)
			if chatrooms:
				return chatrooms['UserName'],pid
		except:
			return None


if __name__ == "__main__":
        
	print(get_chatroom_name(3))
	
	#print(itchat.send('test now3 !!', get_chatroom_name('0')))

import send_matrix

conn_send = send_matrix.db_send_open();
cursor_send = send_matrix.db_send_batch_start(conn_send);

conn_item = storage.db_open();
cursor_item = storage.db_batch_start(conn_item);

while True:
        for groupid in range(16):
                
            #判断群是否允许发送消息
            if db_send_allowed_get(cursor_send, groupid):
                
                #取出该群未发送的分数最高的商品
                item, taotoken = db_send_item_get_id_and_tao(cursor_send, groupid);

                #如果商品存在
                if item:
                     content =   cursor_item.execute("SELECT content FROM Item WHERE itemid = (?) LIMIT 1", item);
                        image_path =  storage.image_get_path(item);
                        
                    print ("group",i, "item", item, "tao ", tao);
                    

                    #设置商品在该群已发送
                    db_send_item_set(conn_send, cursor_send, item, i);
                    time.sleep(10);




def image_store(item_id, ret.content, img_type="jpg"):

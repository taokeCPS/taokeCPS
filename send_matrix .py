#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import time

## 对于群 1是允许发
## 对内容 0是没发过
def db_send_open():
    conn = sqlite3.connect('send_matrix.db');
    cursor = conn.cursor();
    
    # 标识商品与群对应是否发送过及群口令
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' \
                   AND name='matrix'");
    if not cursor.fetchall()[0][0]:
        string = "create table matrix (ItemID DECIMAL(20,0) primary key, \
            Score integer"
        for i in range(100):
            string = string + ",label_"+ str(i)+" boolean";
            string = string + ",tao_"+ str(i)+" varchar(100)";
        string =string + ")";
        cursor.execute(string);
    
    # 标识群是否允许发送
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' \
                   AND name='allowed'");
    if not cursor.fetchall()[0][0]:
        string = "create table allowed  (group_id DECIMAL(20,0) primary key, \
            allowed integer)"
        cursor.execute(string);
        
    
    cursor.close();
    conn.commit();
    conn.close();

    conn = sqlite3.connect('send_matrix.db');
    return conn;


def db_send_batch_start(conn):
    cursor = conn.cursor();         
    return cursor;

  

def db_send_batch_end(conn, cursor):
    cursor.close();                   
    conn.commit();
                   
def db_send_close(conn):
    conn.close();

# 返回群是否允许发送，空值，false，0都是不可以发送
def db_send_allowed_get(cursor, group_id):
    if (group_id<0) or (group_id>=100):
        return None;
    string = "select allowed FROM allowed where group_id =" + str(group_id);
    #print(string)
    cursor.execute(string);
    tmp = cursor.fetchall();
    #print (tmp)
    if tmp:
        if tmp[0][0]:
            return tmp[0][0];
    return None;
    
    
# 设置群是否允许发送
def db_send_allowed_set(conn, cursor, group_id, value):
    if (group_id<0) or (group_id>=100):
        return;
    if (value != 0) and (value != 1):
        return;
##    string = "insert or ignore into allowed ( \
##        group_id, allowed) values (" +str(group_id)+","+str(value)+")";    
##    cursor.execute(string);
    
    cursor.execute("insert or ignore into allowed (group_id, allowed) \
        values (?,?)",(group_id, value)) ;
     
##    string = "UPDATE allowed SET allowed =" +str(value)+" WHERE group_id =" +str(group_id);
##    cursor.execute(string);
    
    cursor.execute("UPDATE allowed SET allowed =? WHERE group_id = ?", (value, group_id));   
    conn.commit();

    
# 返回得分最高的、允许发送的、淘口令不存在商品ID，没有返回None
def db_send_item_get_id_and_no_tao(cursor, group_id):
    if (group_id<0) or (group_id>=100):
        return None;
    string = "SELECT ItemID FROM matrix \
        WHERE (label_" +str(group_id)+"=0 OR label_" +str(group_id)+" IS NULL)"+ " \
        AND tao_"+str(group_id)+" IS NULL \
        ORDER BY score DESC LIMIT 1";
    #print(string)
    cursor.execute(string);
    tmp = cursor.fetchall();
    #print(tmp);
    if tmp:
        if tmp[0][0]:
            return tmp[0][0];
    return None;


# 返回得分最高的、允许发送的、淘口令存在的商品ID，没有返回None
def db_send_item_get_id_and_tao(cursor, group_id):
    if (group_id<0) or (group_id>=100):
        return None;
    string = "SELECT ItemID, tao_"+str(group_id)+" FROM matrix \
        WHERE (label_" +str(group_id)+"=0 OR label_" +str(group_id)+" IS NULL)"+ " \
        AND tao_"+str(group_id)+" IS NOT NULL \
        ORDER BY score DESC LIMIT 1";
    #print(string)
    cursor.execute(string);
    tmp = cursor.fetchall();
    #print(tmp);
    if tmp:
        if tmp[0][0]:
            return tmp[0][0], tmp[0][1];
    return None, None;

    
# 将对应商品标识为以发送过
def db_send_item_set(conn, cursor, item_id, group_id):
    if (group_id<0) or (group_id>=100):
        return;
##    string = "insert or ignore into matrix ( \
##        ItemID, label_"+str(group_id)+") values \
##        (" +str(item_id)+",1)"
##    cursor.execute(string);
    

    cursor.execute("insert or ignore into matrix ( \
        ItemID, label_"+str(group_id)+") values \
        (? ,1)", (item_id,));
    
##    string = "UPDATE matrix SET label_" +str(group_id)+"=1 WHERE ItemID =" +str(item_id);
##    cursor.execute(string);

    
    #print ("UPDATE matrix SET tao_" +str(group_id)+"=? WHERE ItemID =?")
    cursor.execute("UPDATE matrix SET label_" +str(group_id)+"=? WHERE ItemID = ?", (1, item_id));
    
    #print(string)
    conn.commit();


# 向主动发送表格内新增商品
def db_send_item_add(conn, cursor, item_id, score):
##    string = "insert or ignore into matrix (ItemID, score) values \
##        (" +str(item_id)+","+str(score)+")"
##    cursor.execute(string);

    cursor.execute("insert or ignore into matrix (ItemID, score) values (?,?)", (item_id,score));
    
    #print(string)
    conn.commit();

# 向主动发送表格内新增商品对应的淘口令
def db_send_tao_add(conn, cursor, item_id, group_id, tao):
##    string = "insert or ignore into matrix (ItemID, tao_"+str(group_id)+") values \
##        (" +str(item_id)+","+str(tao)+")"
##    cursor.execute(string);     
    #print(string)

    #print("insert or ignore into matrix (ItemID, tao_"+str(group_id)+") values (?,?)")
    cursor.execute("insert or ignore into matrix (ItemID, tao_"+str(group_id)+") values (?,?)", (item_id, tao));  
    
##    string = "UPDATE matrix SET tao_" +str(group_id)+"="+str(tao)+" WHERE ItemID =" +str(item_id);
##    cursor.execute(string);
##    print(string)
    
    
    #print("UPDATE matrix SET tao_" +str(group_id)+"=? WHERE ItemID =?")
    cursor.execute("UPDATE matrix SET tao_" +str(group_id)+"=? WHERE ItemID =?", (tao, item_id));
    conn.commit();
    


def func_demo():    
    #连接至数据库标准步骤
    conn = db_send_open();
    cursor = db_send_batch_start(conn);
    
    #把0-4群标记为允许发送的状态
    for i in range(5):
        db_send_allowed_set(conn, cursor, i, 1);


    #把商品11-13增加至数据库
    for i in range(11,14):    
        db_send_item_add(conn, cursor, i, i+100);


    #把2群标记为禁止发送
    db_send_allowed_set(conn, cursor, 1, 0);
    
    
    #把商品11标记为3群已发送过 等价于 禁止3群发送此类商品
    db_send_item_set(conn, cursor, 11, 3);

    
    
    while True:
        #标识位，如果轮询了一圈，所有的群都没有需要获取淘口令的商品了，就退出
        break_flag = 1;
        
        for i in range(5):
            
            #读出没获取淘口令的商品id
            item = db_send_item_get_id_and_no_tao(cursor, i);
        
            #如果商品存在
            if item:
                break_flag = 0;
                
                #设置淘口令
                db_send_tao_add(conn, cursor, item, i, "tao"+str(i)+" item"+str(item));
            
        if break_flag:
            break;

        

    while True:
        break_flag = 0;
        for i in range(5):
            time.sleep(1);
            
            #判断群是否允许发送消息
            if db_send_allowed_get(cursor, i):
                
                #取出该群未发送的分数最高的商品
                item, tao = db_send_item_get_id_and_tao(cursor, i);

                #如果商品存在
                if item:
                    print ("group",i, "item", item, "tao ", tao);

                    #设置商品在该群已发送
                    db_send_item_set(conn, cursor, item, i);
                    
        if break_flag:
            break;
                

    db_send_batch_end(conn, cursor);                   
    db_send_close(conn);
    
func_demo();
    
##执行开始，出错会自动重新执行
##while True:
##    try:
##        func_run();
##        time.sleep(60);
##    except KeyboardInterrupt:
##        print("bye!")
##    except Exception as e:
##        time.sleep(60);
##        print(Exception,":",e);
##        


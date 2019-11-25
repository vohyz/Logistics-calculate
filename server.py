#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from concurrent import futures
import pymysql
import data_pb2, data_pb2_grpc
import random
import json, urllib
from urllib import parse
from urllib.request import urlopen

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '5002'

def GetDistance(x1, x2, y1, y2):
    x = x1 - x2
    y = y1 - y2

    distance = ((x ** 2) + (y ** 2)) ** 0.5 // 10
    return distance

class RouteBuild(data_pb2_grpc.RouteBuildServicer):
    def Build(self, request, context):

        begin_place = request.begin_place
        end_place = request.end_place
        id = request.id
        print('收到消息:' + begin_place + end_place + id)
        # 获取起点
        try:
            connect, cursor = connect_mysql()
            sql1 = 'select * from place where place_name = %s'
            args1 = begin_place
            cursor.execute(sql1, args1)
            place1 = cursor.fetchone()
            connect.commit()
            cursor.close()
            connect.close()
        except:
            return data_pb2.return_message(ok='place_name_error')
        # 获取终点
        try:
            connect, cursor = connect_mysql()
            sql2 = 'select * from place where place_name = %s'
            args2 = end_place
            cursor.execute(sql2, args2)
            place2 = cursor.fetchone()
            connect.commit()
            cursor.close()
            connect.close()
        except:
            return data_pb2.return_message(ok='place_name_error')

        if place1[1]<place2[1]:
            x1,x2 = place1[1],place2[1]
        else:
            x1,x2 = place2[1],place1[1]

        if place1[2]<place2[2]:
            y1,y2 = place1[2],place2[2]
        else:
            y1,y2 = place2[2],place1[2]
        # 获取随机点
        connect, cursor = connect_mysql()
        sql3 = 'select * from place where (place_x between %s and %s) and (place_y between %s and %s)'
        args3 = (x1 + 1, x2 - 1, y1 + 1, y2 - 1)
        cursor.execute(sql3,args3)
        place_in = cursor.fetchmany(random.randint(3, 5))
        connect.commit()
        cursor.close()
        connect.close()

        placefaker = []
        for i in place_in:
            placefaker.append(list(i))
        if place1[1]>place2[1]:
            flag = True
        else:
            flag = False
        place_better_in = sorted(placefaker,key=lambda x:x[1],reverse=flag)
        place_all = [place1] + place_better_in + [place2]
        print(place_all)
        size = len(place_all)
        print('起点为' + place_all[0][0])
        order_time = ''
        order_place = ''

        for i in range(size - 1):
            x = str(int(GetDistance(place_all[i][1], place_all[i + 1][1], place_all[i][2], place_all[i + 1][2])))
            order_time += ' '
            order_time += x
            order_place += ' '
            order_place += place_all[i][0]
            state = place_all[i+1][0]
            print('经过' + str(x) + '到达了' + state)

        order_place += ' ' + place_all[-1][0]

        connect, cursor = connect_mysql()
        sql4 = 'UPDATE `order` set transport_place = %s where `order_id` = %s'
        args4 = (order_place, id)
        cursor.execute(sql4, args4)
        connect.commit()
        cursor.close()
        connect.close()

        params = {
            "Time": order_time,
            "ID": id
        }
        print(id)
        request_to_timing(params)

        return data_pb2.return_message(ok='ok')

def connect_mysql():#链接mysql
    conn = pymysql.connect(host="cdb-518aglpe.bj.tencentcdb.com", port=10101, user="root", password="zyx1999zyx", database="service")
    cursor = conn.cursor()
    return conn,cursor

def request_to_timing(p, m="GET"):
    url = "http://127.0.0.1:5003"
    params = p
    params = parse.urlencode(params)
    if m == "GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    print(res)

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_RouteBuildServicer_to_server(RouteBuild(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()
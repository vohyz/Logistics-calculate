#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import data_pb2, data_pb2_grpc

_HOST = 'localhost'
_PORT = '8080'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = data_pb2_grpc.RouteBuildStub(channel=conn)
    response = client.Build(data_pb2.order_place(begin_place='上海', end_place="北京"))
    print("received: " + response.ok)

if __name__ == '__main__':
    run()
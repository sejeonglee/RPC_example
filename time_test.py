#!/usr/bin/env python
"""
CASE 1: LOCAL INVOKE
CASE 2: MSG_QUEUE INVOKE(RPC Pattern)

실행 환경을 같게 하기 위하여 실제 Function을 수행하는 Worker는
로컬 코드로 실행(worker_server/worker.py 코드에 존재)

CPU Bounded 코드로 먼저 실험
ex)
    {"method":"fibonacci", "value": {N}}으로 전달하면
    피보나치 수를 구하는 코드를 각각의 케이스에 대하여 실행하고 반환값을 전달
"""
from typing import Any
import pika
import uuid
import time
import json

from worker_server.worker import response_function

CREDENTIALS = pika.PlainCredentials('test_admin', 'admin1234')
PARAMETERS = pika.ConnectionParameters('210.183.178.47',
                                       25672,
                                       '/',
                                       credentials=CREDENTIALS)

class RpcClient(object):
    """RPC CALL을 수행하는 클래스

    Methods:
        on_response: RabbitMQ pika client의 callback 메소드
        call: 실제로 함수를 Invoke하는데에 사용하는 함수
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(PARAMETERS)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.queue_declare(queue='rpc_queue_return')
        self.channel.basic_consume("rpc_queue_return", self.on_response)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, args: dict) -> Any:
        """RabbitMQ 메세지 큐를 통해 RPC를 수행.
        동기적으로 실행되며 반환값이 다른 큐를 통해 들어올 때까지 반복문을 돌려 Block됨.

        Parameters:
            args: Dictionary. JSON형태로 원격 함수의 인자를 정의
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = 'rpc_queue_return',
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(args))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == "__main__":
    call_args = json.dumps({"method": "fibonacci", "value": "32"})

    case1_starttime = time.time()
    process_return = response_function(call_args)
    case1_endtime = time.time()

    print("<Case 1>")
    print(f"Time: {case1_endtime-case1_starttime:.8f} Return: {process_return}")

    case2_starttime = time.time()
    rpc_client = RpcClient()  
    process_return = rpc_client.call(call_args)
    case2_endtime = time.time()

    print("<Case 2>")
    print(f"Time: {case2_endtime-case2_starttime:.8f} Return: {process_return}")
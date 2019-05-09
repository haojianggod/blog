#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from Queue import Empty

from queue import Queue


class Producer(object):
	def __init__(self, q):
		self._queue = q

	def produce(self):
		for i in range(1, 10):
			self._queue.put("msg: %d" % i)


class Consumer(object):
	def __init__(self, q):
		self._queue = q

	def consume(self):
		while True:
			try:
				msg = self._queue.get(block=False, timeout=10)
				print("consume: %s" % msg)
			except Empty as e:
				print("queue is empty, break")
				break


if __name__ == '__main__':
	q = Queue(20)
	producer = Producer(q)
	consumer = Consumer(q)

	producer.produce()
	consumer.consume()
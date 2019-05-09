---
title: python Queue学习
date: 2019-05-02 15:41:36
updated:
tags:
categories:
- python
- Queue
---
#### example

  ```python
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

  ```

#### 代码分析 + 流程图

##### __init__ 方法

```python

def __init__(self, maxsize=0):
    self.maxsize = maxsize
    self._init(maxsize)
    # mutex must be held whenever the queue is mutating.  All methods
    # that acquire mutex must release it before returning.  mutex
    # is shared between the three conditions, so acquiring and
    # releasing the conditions also acquires and releases mutex.
    self.mutex = _threading.Lock()
    # Notify not_empty whenever an item is added to the queue; a
    # thread waiting to get is notified then.
    self.not_empty = _threading.Condition(self.mutex)
    # Notify not_full whenever an item is removed from the queue;
    # a thread waiting to put is notified then.
    self.not_full = _threading.Condition(self.mutex)
    # Notify all_tasks_done whenever the number of unfinished tasks
    # drops to zero; thread waiting to join() is notified to resume
    self.all_tasks_done = _threading.Condition(self.mutex)
    self.unfinished_tasks = 0

# Initialize the queue representation
def _init(self, maxsize):
    self.queue = deque()
```

-  maxsize： 最大队列长队，如果 maxsize<=0， 长度不限制
-  mutex: 该锁用来生成3个条件变量，not_empty，not_full, all_tasks_done，

-  队列底层实现 用的是collections.deque() 双端队列

##### put 方法

```python
def put(self, item, block=True, timeout=None):
       """Put an item into the queue.

       If optional args 'block' is true and 'timeout' is None (the default),
       block if necessary until a free slot is available. If 'timeout' is
       a non-negative number, it blocks at most 'timeout' seconds and raises
       the Full exception if no free slot was available within that time.
       Otherwise ('block' is false), put an item on the queue if a free slot
       is immediately available, else raise the Full exception ('timeout'
       is ignored in that case).
       """
       self.not_full.acquire()
       try:
           if self.maxsize > 0:
               if not block:
                   if self._qsize() == self.maxsize:
                       raise Full
               elif timeout is None:
                   while self._qsize() == self.maxsize:
                       self.not_full.wait()
               elif timeout < 0:
                   raise ValueError("'timeout' must be a non-negative number")
               else:
                   endtime = _time() + timeout
                   while self._qsize() == self.maxsize:
                       remaining = endtime - _time()
                       if remaining <= 0.0:
                           raise Full
                       self.not_full.wait(remaining)
           self._put(item)
           self.unfinished_tasks += 1
           self.not_empty.notify()
       finally:
           self.not_full.release()
```

1) 加锁，self.not_full.acquire

2) 队列如果有长队限制：

   - 如果是not block, 队列满，直接抛出Full exception
   - 如果是block && timeout is None, 判断队列是否满，如果满则一直等待
   - 如果timeout < 0 ， 抛出异常信息`timeout` must be a non-negative number
   - block && timeout > 0, 如果满，则等待timeout 时间（单位为秒），等待timeout 秒后，如果队列还是满则抛出 Full 异常
   - 将item 插入队列，unfinished_tasks++, 通知not_empty 条件变量队列非空了。
   - 最后，释放not_full 锁

3）队列没有长度限制：

  - 将item 插入队列，unfinished_tasks++, 通知not_empty 条件变量队列非空了。
  - 最后，释放not_full 锁

  ![avatar](http://rpig-images.oss-cn-beijing.aliyuncs.com/python%E5%AD%A6%E4%B9%A0/queue-put%E6%B5%81%E7%A8%8B%E5%9B%BE.jpg)

##### get 方法

```python
def get(self, block=True, timeout=None):
    """Remove and return an item from the queue.

    If optional args 'block' is true and 'timeout' is None (the default),
    block if necessary until an item is available. If 'timeout' is
    a non-negative number, it blocks at most 'timeout' seconds and raises
    the Empty exception if no item was available within that time.
    Otherwise ('block' is false), return an item if one is immediately
    available, else raise the Empty exception ('timeout' is ignored
    in that case).
    """
    self.not_empty.acquire()
    try:
        if not block:
            if not self._qsize():
                raise Empty
        elif timeout is None:
            while not self._qsize():
                self.not_empty.wait()
        elif timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")
        else:
            endtime = _time() + timeout
            while not self._qsize():
                remaining = endtime - _time()
                if remaining <= 0.0:
                    raise Empty
                self.not_empty.wait(remaining)
        item = self._get()
        self.not_full.notify()
        return item
    finally:
        self.not_empty.release()

```

1）not_empty.acquire(), 加锁
2）如果block=False, 此时如果队列长度 = 0， 直接抛异常：Empty
3）如果block=True， timeout is None, 等待直到队列不空
4）如果timeout < 0, 抛异常:ValueError，timeout > 0, 阻塞timeout 直到队列不为空，timeout 后如果队列还是空，抛异常：Empty

5) get 队列元素，通知not_full 条件变量，告知put 等待线程队列有元素 出，可以进行后续操作了。

6）最后释放锁，not_empty.release()

![Queue-get 方法流程图](http://rpig-images.oss-cn-beijing.aliyuncs.com/python%E5%AD%A6%E4%B9%A0/queue-get%E6%B5%81%E7%A8%8B%E5%9B%BE.jpg)

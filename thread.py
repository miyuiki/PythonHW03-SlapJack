import threading
import sys
import socket
import time

class myThread(threading.Thread):
	"""docstring for myThread"""
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def run(self):
		print "Starting" + self.name
		threadLock.acquire()
		print_time(self.name, self.counter, 3)
		threadLock.release()
	
def print_time(threadName, delay, counter):
	while counter:
		time.sleep(delay)
		print "%s: %s" %(threadName, time.ctime(time.time()))
		counter -= 1

threadLock = threading.Lock()
threads = []

thread1 = myThread(1, "thread-1", 1)
thread2 = myThread(2, "thread-2", 2)

thread1.start()
thread2.start()

threads.append(thread1)
threads.append(thread2)

for x in threads:
	x.join()

print "Exiting Main Thread"

import threading
import sys
import random
import time

card = []
player = [[], [], [], []]

threadLock = threading.Lock()

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
        for i in xrange(0, 3):
            player[self.threadID-1].append(getCard())
        print_card(self.name, self.counter, player[self.threadID-1],1)
        threadLock.release()
def initCard():
    for i in xrange(1, 5):
        for j in xrange(1, 14):
            card.append((i, j))
    random.shuffle(card)

def getCard():
    content = card[len(card)-1]
    card.remove(content)
    return content

def print_card(threadName, delay, first3card, counter):
    while counter:
        time.sleep(2)
        print "%s : %s" %(threadName, str(first3card))
        counter -= 1

if __name__ == '__main__':
    initCard()
    threads = []
    thread1 = myThread(1, "PLAYER-1", 1)
    thread2 = myThread(2, "PLAYER-2", 2)
    thread3 = myThread(3, "PLAYER-3", 3)
    thread4 = myThread(4, "PLAYER-4", 4)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)

    for t in threads:
        t.join()

    print "Exiting Main Thread"

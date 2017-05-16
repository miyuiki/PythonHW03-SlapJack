import threading
import sys
import random
import time

card = []
player = [[], [], [], []]
point = []
now = (0,0) 
get = False
flag = False
no_first = True
no_second = True
first = ""
second = ""
player_pass = [False,False,False,False]
global end
lock = threading.Lock()
sem = threading.Semaphore(1)

class myThread(threading.Thread):
    """docstring for myThread"""

    def __init__(self, lock, threadName, threadID, selfcard, same_color, same_point, steal):
        super(myThread,  self ).__init__(name = threadName)    
        self.lock = lock 
        self.selfcard = selfcard
        self.threadID = threadID
        self.same_color = same_color
        self.same_point = same_point
        self.steal = steal

    def run(self):
        global flag
        global get
        global player_pass
        global no_first
        global no_second
        global first
        global second

        while 1:
            if len(card) == 0:
                return
            while 1:
                if len(self.selfcard) is 0:
                    player_pass[self.threadID] = True
                    if no_second or no_first:
                        if no_first:
                            first = self.name
                            no_first = False
                        else:
                            second = self.name
                            no_second = False
                    break
                self.lock.acquire()
                if flag:
                    for x in self.selfcard:
                        if now[1] == x[1]:
                            print "current card: %s" %str(now)
                            print "Player %s got same point card + 30" %self.name
                            self.selfcard.remove(x)
                            print("Player #1: " + str(player[0]))
                            print("Player #2: " + str(player[1]))
                            print("Player #3: " + str(player[2]))
                            print("Player #4: " + str(player[3]))
                            self.same_point += 1
                            flag = False
                            break
                    for x in self.selfcard:
                        if now[0] == x[0] and flag :
                            print "current card: %s" %str(now)
                            print "Player %s got same color card + 10" %self.name
                            self.selfcard.remove(x)
                            print("Player #1: " + str(player[0]))
                            print("Player #2: " + str(player[1]))
                            print("Player #3: " + str(player[2]))
                            print("Player #4: " + str(player[3]))
                            self.same_color += 1
                            flag = False
                            break
                    if flag:
                        player_pass[self.threadID] = True
                        self.lock.release()
                        break
                self.lock.release()
            while player_pass.count(True) == 4:
                if len(self.selfcard) == 0:
                    return
                else:
                    self.lock.acquire()
                    print "current card: %s" % str(now)
                    print "Player %s stolen a card + 5" % self.name
                    print("Player #1: " + str(player[0]))
                    print("Player #2: " + str(player[1]))
                    print("Player #3: " + str(player[2]))
                    print("Player #4: " + str(player[3]))
                    self.steal += 1
                    flag = False
                    self.lock.release()
                    break
            if len(self.selfcard) is 0:
                break
     
def initCard():
    for i in xrange(1, 5):
        for j in xrange(1, 14):
            card.append((i, j))
    random.shuffle(card)

def getCard():
    content = card[len(card)-1]
    card.remove(content)
    return content

def isWinner(thread):
    if thread.name == first:
        return 50
    elif thread.name == second:
        return 20
    else:
        return 0

if __name__ == '__main__':
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    end = False
    initCard()
    for i in xrange(0,4):
        for j in xrange(0,3):
            player[i].append(getCard())
    now = (0,0)
    print ("Player #1's card " + str(player[0]))
    print ("Player #2's card " + str(player[1]))
    print ("Player #3's card " + str(player[2]))
    print ("Player #4's card " + str(player[3]))

    thread1 = myThread(sem, "PLAYER-1", 0, player[0], 0, 0, 0)
    thread2 = myThread(sem, "PLAYER-2", 1, player[1], 0, 0, 0)
    thread3 = myThread(sem, "PLAYER-3", 2, player[2], 0, 0, 0)
    thread4 = myThread(sem, "PLAYER-4", 3, player[3], 0, 0, 0)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    time.sleep(1.5)

    while len(card) != 0:
        now = getCard()
        flag = True
        time.sleep(1.5)

        if len(player[0]) == 0 and len(player[1]) == 0 and len(player[2]) == 0 and len(player[3]) == 0:
            p1 = thread1.same_point * 30 + thread1.same_color * 10 + thread1.steal * 5 + isWinner(thread1)
            p2 = thread2.same_point * 30 + thread2.same_color * 10 + thread2.steal * 5 + isWinner(thread2)
            p3 = thread3.same_point * 30 + thread3.same_color * 10 + thread3.steal * 5 + isWinner(thread3)
            p4 = thread4.same_point * 30 + thread4.same_color * 10 + thread4.steal * 5 + isWinner(thread4)
            print "player's card is empty"
            print "player #1 total point: {}, got same point {} times, got same color {} times, stealing {} times, rank bonus + {}"\
                .format(str(p1),str(thread1.same_point),str(thread1.same_color),str(thread1.steal),str(isWinner(thread1)))
            print "player #2 total point: {}, got same point {} times, got same color {} times, stealing {} times, rank bonus + {}" \
                .format(str(p2),str(thread2.same_point),str(thread2.same_color), str(thread2.steal),str(isWinner(thread2)))
            print "player #3 total point: {}, got same point {} times, got same color {} times, stealing {} times, rank bonus + {}"\
                .format(str(p3),str(thread3.same_point), str(thread3.same_color), str(thread3.steal),str(isWinner(thread3)))
            print "player #4 total point: {}, got same point {} times, got same color {} times, stealing {} times, rank bonus + {}" \
                .format(str(p4),str(thread4.same_point), str(thread4.same_color), str(thread4.steal),str(isWinner(thread4)))
            end = True
            break
        elif len(card) == 0:
            print "no more card"
            end = True
            break
        else:
            print
    while 1:
        if end:
            sys.exit()
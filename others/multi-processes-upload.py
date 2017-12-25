from multiprocessing import Process, Queue
from datetime import datetime
keep_processing = True

def loop_a(q):
    try:
        while keep_processing:
            q.put([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'hello'])
    except KeyboardInterrupt:
        return "KeyboardInterrupt loop_a"

def loop_b(q):
    try:
        while keep_processing:
            print(q.get())
    except KeyboardInterrupt:
        return "KeyboardInterrupt loop_b"

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=loop_a, args=(q,))
    p2 = Process(target=loop_b, args=(q,))
    p1.start()
    p2.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        keep_processing = False

    p1.join()
    p2.join()

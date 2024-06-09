from threading import Thread, Event, Lock
import queue
from queue import Queue
import cv2
import numpy as np


class PicGen:
    def __init__(self, q: Queue, lock: Lock) -> None:
        self.q = q
        self.lock = lock

    def run(self):
        while not event.is_set():
            arr = np.random.random((640, 640, 4))
            self.lock.acquire()
            try:
                self.q.put_nowait(arr)
            except queue.Full:
                continue
            finally:
                self.lock.release()


class Monitor:
    def __init__(self, q: Queue, lock: Lock) -> None:
        self.q = q
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            try:
                if self.q.empty():
                    continue
                arr = self.q.get()
            finally:
                self.lock.release()
            cv2.imshow("img", arr)
            if cv2.waitKey(1) == ord("q"):
                event.set()
                cv2.destroyAllWindows()
                return


def main():
    ts = [Thread(target=PicGen(q, lock).run) for _ in range(thread_num)]
    [t.start() for t in ts]
    Monitor(q, lock).run()
    [t.join() for t in ts]


if __name__ == "__main__":
    thread_num = 2
    event = Event()
    lock = Lock()
    q = Queue(10)
    main()

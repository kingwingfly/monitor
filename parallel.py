from multiprocessing import Process, Queue, Lock
import numpy as np
import cv2


class PicGen:
    def __init__(self, q: Queue, lock: Lock) -> None:
        self.q = q
        self.lock = lock

    def run(self):
        while True:
            arr = np.random.random((640, 640, 4))
            self.lock.acquire()
            try:
                self.q.put_nowait(arr)
            except:
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
                cv2.destroyAllWindows()
                return


def main():
    ps = [Process(target=PicGen(q, lock).run) for _ in range(process_num)]
    [p.start() for p in ps]
    Monitor(q, lock).run()
    [p.terminate() for p in ps]


if __name__ == "__main__":
    process_num = 2
    lock = Lock()
    q = Queue(10)
    main()

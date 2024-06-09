from multiprocessing.shared_memory import SharedMemory
import cv2
import numpy as np
from multiprocessing import Process, Lock
from multiprocessing.synchronize import Lock as Locktype

SIZE = 640 * 640 * 4


class PicGen:
    def __init__(self, s: SharedMemory, lock: Locktype) -> None:
        self.s = s
        self.lock = lock

    def run(self):
        while True:
            arr = np.random.random(SIZE)
            self.lock.acquire()
            try:
                shared_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=self.s.buf)
                np.copyto(shared_arr, arr)
            except:
                continue
            finally:
                self.lock.release()


class Monitor:
    def __init__(self, s: SharedMemory, lock: Locktype) -> None:
        self.s = s
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            try:
                arr = np.frombuffer(self.s.buf).reshape((640, 640, 4))
            finally:
                self.lock.release()
            cv2.imshow("img", arr)
            if cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                return


def main():
    arr = np.random.random(SIZE)
    shared_mem = SharedMemory(size=arr.nbytes, create=True)
    lock = Lock()
    process_num = 2
    ps = [Process(target=PicGen(shared_mem, lock).run) for _ in range(process_num)]
    [p.start() for p in ps]
    Monitor(shared_mem, lock).run()
    [p.terminate() for p in ps]
    shared_mem.close()
    shared_mem.unlink()


if __name__ == "__main__":
    main()

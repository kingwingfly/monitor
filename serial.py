import numpy as np
import cv2


class Monitor:
    @staticmethod
    def run():
        while True:
            arr = yield
            cv2.imshow("img", arr)
            if cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                break


class PictureGen:
    def __init__(self) -> None:
        self.rd = Monitor().run()
        self.rd.send(None)

    def run(self):
        while True:
            arr = np.random.random((640, 640, 4))
            try:
                self.rd.send(arr)
            except StopIteration:
                break


def main():
    pg = PictureGen()
    pg.run()


if __name__ == "__main__":
    main()

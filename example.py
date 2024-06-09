import threading
import asyncio


class Foo:
    async def async_run(self):
        while True:
            print("A job need await")

    def start(self):
        def wrapper():
            asyncio.run(self.async_run())

        t1 = threading.Thread(target=wrapper)
        t1.start()
        # bad way: it blocked the current thread
        while True:
            ...


class Bar:
    def start(self):
        while True:
            print("I am another job")


def bad_example():
    foo = Foo()
    bar = Bar()
    foo.start()
    bar.start()


class BetterFoo:
    async def start(self):
        while True:
            print("A better Foo")
            await asyncio.sleep(0)


class BetterBar:
    async def start(self):
        while True:
            print("A better Bar")
            await asyncio.sleep(0)


def good_example():
    async def wrapper():
        foo = BetterFoo()
        bar = BetterBar()
        more = [BetterFoo().start() for _ in range(3)]
        await asyncio.gather(foo.start(), bar.start(), *more)

    asyncio.run(wrapper())


if __name__ == "__main__":
    bad_example()

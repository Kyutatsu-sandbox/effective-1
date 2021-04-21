from threading import Thread
from queue import Queue
import time
​
​
def download(item):
    return item
​
​
def resize(item):
    time.sleep(0.1)
    return item
​
​
def upload(item):
    return item
​
​
class ClosableQueue(Queue):
    SENTINEL = object()
​
    def close(self):
        self.put(self.SENTINEL)
​
    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                print("task_done")
                self.task_done()
​
​
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
​
    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)
​
​
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]
​
​
for thread in threads:
    thread.start()
​
for _ in range(10):
    download_queue.put(object())
​
download_queue.close()
download_queue.join()
print("download_join")
resize_queue.close()
resize_queue.join()
print("re_join")
upload_queue.close()
upload_queue.join()
print("upd_join")
print(done_queue.qsize(), "items finished")
​
for thread in threads:
    thread.join()

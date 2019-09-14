from threading import Thread
from time import sleep


class File_writer(Thread):
    def __init__(self, queue_writer_reader):
        super().__init__(daemon=True)
        self.file = open("links.lst", "a")
        self.queue_writer_reader = queue_writer_reader
        self.writing = True

    def write(self, link):
        self.file.write("{}\n".format(link))
        self.file.flush()

    def get(self):
        link = self.queue_writer_reader.get_new_link_to_write()
        self.write(link)

    def stop_living(self):
        self.crawling = False

    def run(self):
        while self.writing:
            if self.queue_writer_reader.new_link_to_write_available:
                self.get()
            else:
                sleep(5)

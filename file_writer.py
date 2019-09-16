from threading import Thread
from time import sleep
from multiprocessing import Process


class File_writer_Thread(Thread):
    def __init__(self, queue_writer_reader, max_counter):
        super().__init__(daemon=True)
        self.file = open("links.lst", "a")
        self.queue_writer_reader = queue_writer_reader
        self.writing = True
        self.max_counter = max_counter
        self.counter = 0

    def write(self, link):
        self.file.write("{}\n".format(link))
        self.file.flush()
        self.counter += 1

    def get(self):
        link = self.queue_writer_reader.get_new_link_to_write()
        self.write(link)

    def stop_living(self):
        self.writing = False

    def run(self):
        loop_without_link = 0

        while self.writing:
            if self.max_counter > 0 and self.counter > self.max_counter:
                self.queue_writer_reader.stop_crawlers()
                self.stop_living()

            if self.queue_writer_reader.new_link_to_write_available:
                self.get()
                loop_without_link = 0
            else:
                loop_without_link += 1
                sleep(5)
                if loop_without_link == 10:
                    valid = False
                    while not valid:
                        q = str(input(
                            "[*] There was no link to write for 10 loops,\n    would you like to [S]top or [W]ait another 10 loops"))
                        if q.upper() == "S":
                            self.stop_living()
                            valid = True
                        elif q.upper() == "W":
                            loop_without_link = 0
                            valid = True
                        else:
                            print("[+] That was not S or W, try again")


class File_writer_Process(Process):
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
        self.writing = False

    def isAlive(self):
        return True

    def run(self):
        loop_without_link = 0

        while self.writing:
            if self.queue_writer_reader.new_link_to_write_available:
                self.get()
                loop_without_link = 0
            else:
                loop_without_link += 1
                sleep(5)
                if loop_without_link == 10:
                    valid = False
                    while not valid:
                        q = str(input(
                            "[*] There was no link to write for 10 loops,\n    would you like to [S]top or [W]ait another 10 loops"))
                        if q.upper() == "S":
                            self.stop_living()
                            valid = True
                        elif q.upper() == "W":
                            loop_without_link = 0
                            valid = True
                        else:
                            print("[+] That was not S or W, try again")

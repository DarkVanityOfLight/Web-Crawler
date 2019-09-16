from threading import Thread
from time import sleep
from urllib.request import urlopen
from analyse import re_analyser as analyser
from sys import exit
from re import match
from multiprocessing import Process


class Thread_spider(Thread):
    def __init__(self, queue_writer_reader, _name):
        super().__init__(daemon=True)
        self.queue_writer_reader = queue_writer_reader
        self._name = _name
        self.crawling = True

    def get_link(self):
        # print("[*] Getting link from queue")
        if self.queue_writer_reader.new_link_to_visit_available():
            link = self.queue_writer_reader.get_new_link_to_visit()
            return link
        else:
            return None

    def _request(self, link):
        print("[*] Following {}".format(link))
        try:
            text = urlopen(link).read()
            self.queue_writer_reader.put_new_link_to_write(link)

            return text
        except:

            return None

    def analyse(self, text):

        return analyser(text)

    def write_links_to_visit(self, links):
        for link in links:

            self.queue_writer_reader.put_new_link_to_visit(str(link, "utf-8"))

    def write_link_to_write(self, link):
        self.queue_writer_reader.put_new_link_to_write(str(link, "utf-8"))

    def stop_living(self):
        print("[*] {} died".format(self._name))
        self.crawling = False

    def run(self):
        loops_without_link = 0
        while self.crawling:
            if self.queue_writer_reader.new_link_to_visit_available():

                link = self.get_link()
                if link != None:
                    loops_without_link = 0
                    text = self._request(link)
                    if text != None:
                        links = self.analyse(text)
                        if len(links) != 0:
                            self.write_links_to_visit(links)

                else:
                    sleep(5)
                    loops_without_link += 1

            else:
                sleep(5)
                loops_without_link += 1

            if loops_without_link >= 10:
                valid = False
                while not valid:
                    a = str(input(
                        "[*] {} got no link for 10 loops, would you like to [E]nd, [G]ive a new link or [W]ait another 10 loops".format(self._name)))
                    if a.upper() == "E":
                        self.stop_living()
                    elif a.upper() == "G":
                        while not valid:
                            start_point = str(
                                input("[+] Start link(has to start with http[s])\n"))
                            if match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", start_point):
                                valid = True
                            else:
                                print("[+] That's not a valid link")
                    elif a.upper() == "W":
                        print(
                            "[*] {} will wait for another 10 loops".format(self._name))
                        loops_without_link = 0
                        valid = True

                    else:
                        print("That was not E, G or W, try again")
        exit(0)


class Process_spider(Process):
    def __init__(self, queue_writer_reader, _name):
        super().__init__(daemon=True)
        self.queue_writer_reader = queue_writer_reader
        self._name = _name
        self.crawling = True

    def get_link(self):
        # print("[*] Getting link from queue")
        if self.queue_writer_reader.new_link_to_visit_available():
            link = self.queue_writer_reader.get_new_link_to_visit()
            return link
        else:
            return None

    def _request(self, link):
        print("[*] Following {}".format(link))
        try:
            text = urlopen(link).read()
            self.queue_writer_reader.put_new_link_to_write(link)

            return text
        except:

            return None

    def analyse(self, text):

        return analyser(text)

    def write_links_to_visit(self, links):
        for link in links:

            self.queue_writer_reader.put_new_link_to_visit(str(link, "utf-8"))

    def write_link_to_write(self, link):
        self.queue_writer_reader.put_new_link_to_write(str(link, "utf-8"))

    def stop_living(self):
        print("[*] {} died".format(self._name))
        self.crawling = False

    def isAlive(self):
        return True

    def run(self):
        loops_without_link = 0
        while self.crawling:
            if self.queue_writer_reader.new_link_to_visit_available():

                link = self.get_link()
                if link != None:
                    loops_without_link = 0
                    text = self._request(link)
                    if text != None:
                        links = self.analyse(text)
                        if len(links) != 0:
                            self.write_links_to_visit(links)

                else:
                    sleep(5)
                    loops_without_link += 1

            else:
                sleep(5)
                loops_without_link += 1

            if loops_without_link >= 10:
                valid = False
                while not valid:
                    a = str(input("[*] {} got no link for 10 loops, would you like to [E]nd, [G]ive a new link or [W]ait another 10 loops\n".format(self._name)))
                    if a.upper() == "E":
                        self.stop_living()
                    elif a.upper() == "G":
                        while not valid:
                            start_point = str(
                                input("[+] Start link(has to start with http[s])\n"))
                            if match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", start_point):
                                valid = True
                            else:
                                print("[+] That's not a valid link")
                    elif a.upper() == "W":
                        print(
                            "[*] {} will wait for another 10 loops".format(self._name))
                        loops_without_link = 0
                        valid = True

                    else:
                        print("That was not E, G or W, try again")
            if self.queue_writer_reader.stop_crawling == True:
                print("[*] Max depth was reached, killing spider {}".format(self._name))
                self.stop_living()
        exit(0)

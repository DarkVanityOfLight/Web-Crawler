from threading import Thread
from time import sleep
from urllib.request import urlopen
from analyse import re_analyser as analyser
from sys import exit

class Thread_spider(Thread):
    def __init__(self, queue_writer_reader, _name):
        super().__init__(daemon=True)
        self.queue_writer_reader = queue_writer_reader
        self._name = _name
        self.crawling = True

    def get_link(self):
        return self.queue_writer_reader.get_new_link_to_visit()

    def _request(self, link):
        try:
            text = urlopen(link).read()
            self.queue_writer_reader.write_link_to_write(link)
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
        self.crawling = False

    def run(self):
        while self.crawling:
            if self.queue_writer_reader.new_link_to_visit_available():
                link = self.get_link()
                text = self._request(link)
                print(text)
                if text != None:
                    links = self.analyse(text)
                    print(links)
                    self.write_links_to_visit(links)
            else:
                sleep(5)
        #self._is_stopped = True
        exit(0)
        

class Process_spider:
    pass
from queue import Queue


class Queue_writer_reader:
    def __init__(self, links_to_visit):
        self.links_to_write = Queue()
        self.links_to_visit = links_to_visit

    def get_new_link_to_write(self):
        return self.links_to_write.get()

    def get_new_link_to_visit(self):
        return self.links_to_visit.get()

    def put_new_link_to_visit(self, link):
        self.links_to_visit.put(link)

    def put_new_link_to_write(self, link):
        self.links_to_write.put(link)

    def new_link_to_write_available(self):
        if self.links_to_write.all_tasks_done:
            return False
        else:
            return True

    def new_link_to_visit_available(self):
        if self.links_to_visit.all_tasks_done:
            return False
        else:
            return True

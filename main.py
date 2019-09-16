from spider import Thread_spider, Process_spider
from queue_writer_reader import Queue_writer_reader
from sys import exit
from os import system
from time import sleep
from file_writer import File_writer
from queue import Queue
from re import match

# //TODO Add argv


def get_arg_input():
    return None

# //TODO validate user input


def get_cmd_input():
    names = []
    valid = False

    while not valid:
        t_or_p = str(input("[+] [T]read or [P]rocess?\n"))
        if t_or_p.upper() == "T" or t_or_p.upper() == "P":
            valid = True
        else:
            print("[+] {} is not T or P, try again")

    while not valid:
        try:
            number = int(input("[+] How many crawlers do you want?\n"))
            valid = True
        except:
            print("[+] That's not a number")
    valid = False
    while not valid:
        start_point = str(input("[+] Start link(has to start with http[s])\n"))
        if match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", start_point):
            valid = True
        else:
            print("[+] That's not a valid link")

    for _ in range(number):
        names.append(str(input("[+] Name your little crawler/s\n")))

    system("clear")
    return t_or_p, number, start_point, names


def create(t_or_p, number, start_point, names):
    crawlers = {}

    queue = Queue()
    queue.put(start_point)
    queue_writer_reader = Queue_writer_reader(queue)
    file_writer = File_writer(queue_writer_reader)

    if t_or_p.upper() == "T":
        for i in range(number):
            crawlers[names[i]] = Thread_spider(queue_writer_reader, names[i])

        return crawlers, queue_writer_reader, file_writer
    else:
        for i in range(number):
            crawlers[names[i]] = Process_spider(queue_writer_reader, names[i])
            return crawlers, queue_writer_reader, file_writer


def main():
    print("[+] Hit CTRL-C\n   to exit")

    running = True
    threads = []

    if get_arg_input() == None:
        t_or_p, number, start_point, names = get_cmd_input()
        crawlers, queue_writer_reader, file_writer = create(
            t_or_p, number, start_point, names)
        crawler_threads = [crawlers[i] for i in crawlers.keys()]
        threads = threads + crawler_threads
        threads.append(file_writer)

    for thread in threads:
        thread.start()

    while running:
        try:
            threads = [t.join(0)
                       for t in threads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print("\n[+] Killing threads")
            for t in threads:
                t.stop_living()
            sleep(2)
            exit(0)


if __name__ == "__main__":
    main()

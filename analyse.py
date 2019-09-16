import re


def re_analyser(text):
    links = re.findall(b"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)
    if links:
        return links
    else:
        #print("[*] Found no link")
        return []

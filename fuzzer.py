# Created: 1/30/2023 by Jonathan Wilson
# Version: 0.0.2
# 
# 
# Arguments
# 1: Target URL
# 2: Port
# 3: Wordlist


import sys
from os.path import exists
from termcolor import colored
import re
import requests

def FileExists(_file):
    fileExists = exists(_file)
    return fileExists

def validateURL(_url):
    isValid = re.match('^(http(s){0,1}:\/\/){0,1}(([a-zA-Z]*\.){0,1}([a-zA-Z0-9]*)\.[a-zA-Z]{1,10}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(\/[\d\w\s\/\.\-\+\_\?\=\|\$\^\\\(\)\{\}\[\]]*){0,1}$', _url)
    return isValid


if __name__ == "__main__":

    print("FUZZER")
    print("Usage: fuzzer.py <Target URL> <Port> <Wordlist>")
    print("")

    if len(sys.argv) !=  4:
        print("Not enough arguments")
        exit()

    url = sys.argv[1]
    port = int(sys.argv[2])
    wordlist = sys.argv[3]
    error = 0

    # Validate the URL
    isValidURL = validateURL(url)

    if isValidURL:
        print("Target: \t" + url)
    else:
        print(colored("Target: \tNot a valid URL or IP address! (%s)" % url, 'red'))

    # Validate the port
    if port > 65535:
        print(colored("Port: Not a valid port! (%d)" % port, 'red'))
        error = 1
    else:
        print("Port: \t\t%d" % port)

    # Validate that the wordlist exists
    wlExists = FileExists(wordlist)
    if not wlExists:
        print(colored("Wordlist: Not a valid file path! (%s)" % wordlist, 'red'))
        error = 1
    else:
        print("Wordlist: \t" + wordlist)


    if error:
        exit()


    # Build the proper URL. Needs http:// if it doesn't have it
    hasHTTP = re.match('^(http(s){0,1}:\/\/){1}', url)

    if not hasHTTP:
        url = "http://" + url

    # print("Effective URL:\t%s\n" % url)

    
    # # Open the wordlist
    wordlistOpen = open(wordlist, 'r')

    print("")

    for line in wordlistOpen:
        urlFuzz = url + "/"+ line.replace("\n", "") + "/"
        r = requests.get(urlFuzz)
        if r.status_code == 200:
            print(colored("[*] ", 'blue') + urlFuzz + " " + str(r.status_code))

    wordlistOpen.close()



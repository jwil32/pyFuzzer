# Created: 1/30/2023 by Jonathan Wilson
# Updated: 
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
import resource
import os
import encodings


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
validURL = re.match('^(http(s){0,1}:\/\/){0,1}(([a-zA-Z]*\.){0,1}([a-zA-Z0-9]*)\.[a-zA-Z]{1,10}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(\/[\d\w\s\/\.\-\+\_\?\=\|\$\^\\\(\)\{\}\[\]]*){0,1}$', url)
if validURL:
    print("Target: \t" + url)
else:
    print(colored("Target: Not a valid URL or IP address! (%s)" % url, 'red'))
    error = 1

# Validate the port
if port > 65535:
    print(colored("Port: Not a valid port! (%d)" % port, 'red'))
    error = 1
else:
    print("Port: \t\t%d" % port)

# Validate that the wordlist exists
fileExists = exists(wordlist)
if not fileExists:
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


print("Effective URL:\t%s\n" % url)

# Open the wordlist
wordlistOpen = open(wordlist, 'r')


for line in wordlistOpen:
    #print(line)
    urlFuzz = url + "/"+ line.replace("\n", "") + "/"
    r = requests.get(urlFuzz)
    if r.status_code == 200:
        print(colored("[*] ", 'blue') + urlFuzz + " " + str(r.status_code))

wordlistOpen.close()



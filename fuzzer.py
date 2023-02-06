# Created: 1/30/2023 by Jonathan Wilson
# Version: 0.0.2
# 
# 
# Arguments
# 1: Target URL
# 2: Wordlist
#
# Todo:
# 1. Add option to specify if you want to search for directories, files, or both. Allow multiple file endings
# 2. Calculate the total amount of requests that are going to be run and display it
# 3. Progress bar?

import sys
from os.path import exists
from termcolor import colored
import re
import requests

def FileExists(_file):
    fileExists = exists(_file)
    return fileExists

def ValidateURL(_url):
    isValid = re.match('^(http(s)?:\/\/)?(([a-zA-Z]*\.)?([a-zA-Z0-9]*)\.[a-zA-Z]{1,10}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(\:[0-9]{1,5})?(\/[\d\w\s\/\.\-\+\_\?\=\|\$\^\\\(\)\{\}\[\]]*)?$', _url)
    return isValid


if __name__ == "__main__":

    print("FUZZER")
    print("Usage: fuzzer.py <Target URL> <Wordlist>")
    print("")

    if len(sys.argv) !=  3:
        print("Not enough arguments")
        exit()

    url = sys.argv[1]
    wordlist = sys.argv[2]
    error = 0

    # Validate the URL
    isValidURL = ValidateURL(url)

    if isValidURL:
        print("Target: \t" + url)
    else:
        print(colored("Target: \tNot a valid URL or IP address! (%s)" % url, 'red'))

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
    
    # Open the wordlist
    wordlistOpen = open(wordlist, 'r')

    print("\nStart fuzzing? (y/n)")
    confirm = input()
    
    if confirm.lower() == "y" or confirm.lower() == "yes":

        for line in wordlistOpen:
            urlFuzz = url + "/"+ line.replace("\n", "") + "/"
            r = requests.get(urlFuzz)
            if r.status_code == 200:
                print(colored("[*] ", 'blue') + urlFuzz + " " + str(r.status_code))

        wordlistOpen.close()


    else:
        print("Exiting...")
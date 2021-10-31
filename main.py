#########################################################
#  CS-47206: Data Security and Privacy - Course Project #
#  By: Cieara Pfeifer, Jayden Stearns, & Jarrett Woo    #
#########################################################

#imports
import os
import getpass
import hashlib


# Program Opener and Information display
PROGRAM_NAME = "Hashword"
VERSION = "0.1.0"
DESCRIPTION = "Password Generator and Handler"
print("\n\n\t\t" + PROGRAM_NAME + " \t[v" + VERSION + "]\n\n\t\t" + DESCRIPTION + "\n\n")



SERVICE_INFO_FILE_PATH = "ServiceData.dat"  # the desired and checked-for name of service data file


# Try to open service data file (check if existent in current directory)

if not os.path.exists(SERVICE_INFO_FILE_PATH):

    #
    #if NOT opened: create new file of that name

    print("Service Information File \"" + SERVICE_INFO_FILE_PATH + "\" not found.\n\tPlease continue to create a new file.")

    serviceDataFile = open(SERVICE_INFO_FILE_PATH, "wt")


    #
    # Ask user for hash algorithm to use (default = SHA256)
    hashAlgorithm = (input("\n\tEnter Desired Hash Algorithm [default: sha256]: ") or 'sha256').lower()

    # ensure algorithm CAN be used on this system (SHA256 is in 'guaranteed' set, for example)
    availableAlgorithms = hashlib.algorithms_available

    while(hashAlgorithm not in availableAlgorithms):
        
        print("\n\t\tInvalid Hash Algorithm \'" + hashAlgorithm + "\' given.\n")
        print("\t\tValid Algorithms: ", availableAlgorithms, "\n")
        hashAlgorithm = (input("\tEnter Desired Hash Algorithm [default: sha256]: ") or 'sha256').lower()

    hash = hashlib.new(hashAlgorithm)  # Begin hash algorithm

    #
    # Ask user for master password to use for file
    masterPasswordPlaintext = getpass.getpass("\tEnter " + PROGRAM_NAME + " Master Password [input is hidden]: ")

        # Encode string to be able to use in upcoming hash
    masterPasswordPlaintext = masterPasswordPlaintext.encode()

    # Hash the master password
    hash.update(masterPasswordPlaintext)
    hashedMasterPassword = hash.hexdigest()

    #
    # store the hash algo used to the new file
    serviceDataFile.write("hash:" + hashAlgorithm + '\n')

    # store the password to the new file
    serviceDataFile.write("master:" + hashedMasterPassword + '\n')

    #
    # close file (will be re-opened in read mode shortly)
    serviceDataFile.flush()
    serviceDataFile.close()

# END IF: File creation sequence on file not found



# load info from the file into program
serviceDataFile = open(SERVICE_INFO_FILE_PATH, "rt")


        # Ask the user for master password


        # Hash the master password


        # compare Hash to the hash stored in password data file

            # if NOT matching: ask for re-try UNTIL successful hash-match




# Ask the user which service they want their password for


    # if service NOT found in Data File:

        # Notify the user that they need to register the new service
        # Ask the user for the max length allowed for the password
        
        # Enter this service into the data file w/ the information

    


# Take the selected service's name and append it to end of master password given earlier

# Hash the newly-concatenated string, resulting in the service's password


# Trim the resulting hash sequence to the max length specified in the data file



# Copy the password to the user's clipboard (for ease-of-use, only if possible)



# Wait a few seconds, then clear the user's clipboard to clear the password data


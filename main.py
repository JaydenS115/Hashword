#########################################################
#  CS-47206: Data Security and Privacy - Course Project #
#  By: Cieara Pfeifer, Jayden Stearns, & Jarrett Woo    #
#########################################################


import os
from io import TextIOWrapper
import getpass
import hashlib
import codecs
from time import sleep
import pyperclip


# Program Opener and Information display
PROGRAM_NAME = "Hashword"
VERSION = "0.2.0"
DESCRIPTION = "Password Generator and Handler"
print("\n\n\t\t" + PROGRAM_NAME + " \t[v" + VERSION + "]\n\n\t\t" + DESCRIPTION + "\n\n")


#
# the desired and checked-for name of service data file
SERVICE_INFO_FILE_PATH = "ServiceData.dat"


#
# Function: closeAndMoveFile(fileObject)
# If something "wrong" is found with a service info file,
# invoke this function on the fileObject that has the file .open(),
# and this function will close the file, move its contents elsewhere,
# then delete the file, to be made new next execution of the program.

def closeAndMoveFile(fileObject: TextIOWrapper):
    
    # hold onto file name for later re-opening
    filePath = fileObject.name

    # close file, then re-open in read mode
    fileObject.close()
    fileObject = open(filePath, "rt")

    # get file's contents
    fileContents = fileObject.read()
    fileObject.close()

    #
    # get desired filename for service info file
    svcFileInfo = filePath.split('.', 1)


    svcFileName = svcFileInfo[0]
    svcFileName = "[OLD]-"

    svcFileExt = "."
    svcFileExt += svcFileInfo[1]


    #
    # find next available [OLD] filename to store to
    i = 1
    while(os.path.exists(svcFileName + str(i) + svcFileExt)):
        i += 1

    #
    # create and write to new file to store previous file contents
    fileObject = open(svcFileName + str(i) + svcFileExt, "wt")
    fileObject.write(fileContents)
    # close file when done writing
    fileObject.flush()
    fileObject.close()

    #
    # if the previous file is SERVICE_INFO_FILE_PATH, delete it
    # so that it can be re-made in the next execution of the program
    if(filePath == SERVICE_INFO_FILE_PATH):
        os.remove(filePath)


# END FUNCTION: closeAndMoveFile(fileObject)


def bytesToString(b):
    s = str(codecs.encode(b,"hex"),"utf-8")
    return s

# def stringToBytes(s):
#     b = codecs.decode(bytes(s,"utf-8"), "hex")
#     return b

# FUNCTION getMasterPass(masterPasswordPlaintext)
# Takes a string argument as the password and hashes it.
# Returns a hashed string
# (attempt to make code a little more DRY)

def getMasterPass(masterPasswordPlaintext, hashAlgorithm='sha256'):
    
    # Encode string to be able to use in upcoming hash    
    hash = hashlib.pbkdf2_hmac(hashAlgorithm, masterPasswordPlaintext.encode('utf-8'), b'', 1)
    hash = bytesToString(hash)
    return hash

# END FUNCTION: getMasterPass()

# FUNCTION: verifyPass(str: password)
# Takes a string password and a string hash as arguments 
# Hashes password and compares with hash
# Returns true if hashes are equal
def verifyPass(password, savedHash, hashAlgorithm='sha256'):
    hash = getMasterPass(password, hashAlgorithm)
    return hash == savedHash

#
# Try to open service data file (check if existent in current directory)
if not os.path.exists(SERVICE_INFO_FILE_PATH):

    #
    #if NOT opened: start to create new file of that name
    print("Service Information File \"" + SERVICE_INFO_FILE_PATH + "\" not found.\n\tPlease continue to create a new file.")

    #
    # Ask user for hash algorithm to use (default = SHA256)
    hashAlgorithm = (input("\n\tEnter Desired Hash Algorithm [default: sha256]: ") or 'sha256').lower()

    # ensure algorithm CAN be used on this system (SHA256 is in 'guaranteed' set, for example)
    # availableAlgorithms = hashlib.algorithms_available
    availableAlgorithms = hashlib.algorithms_guaranteed

    while(hashAlgorithm not in availableAlgorithms):
        
        print("\n\t\tInvalid Hash Algorithm \'" + hashAlgorithm + "\' given.\n")
        print("\t\tValid Algorithms: ", availableAlgorithms, "\n")
        hashAlgorithm = (input("\tEnter Desired Hash Algorithm [default: sha256]: ") or 'sha256').lower()

    # hash = hashlib.new(hashAlgorithm)  # Begin hash algorithm

    #
    # Ask user for master password to use for file
    masterPasswordPlaintext = getpass.getpass("\tEnter " + PROGRAM_NAME + " Master Password [input is hidden]: ")

        # Encode string to be able to use in upcoming hash
    # masterPasswordPlaintext = masterPasswordPlaintext.encode()

    hashedMasterPassword = getMasterPass(masterPasswordPlaintext, hashAlgorithm)

    # Hash the master password
    # hash.update(masterPasswordPlaintext)
    # hashedMasterPassword = hash.hexdigest()

    # securely clean up the plaintext password
    # to remove it from memory and then from accidental use
    masterPasswordPlaintext = ""
    del masterPasswordPlaintext

    #
    # create the file for writing
    serviceDataFile = open(SERVICE_INFO_FILE_PATH, "wt")

    # store the hash algo used to the new file
    serviceDataFile.write("hash:" + hashAlgorithm + '\n')

    # store the password to the new file
    serviceDataFile.write("master:" + hashedMasterPassword + '\n')

    #
    # close file (will be re-opened in read mode shortly)
    serviceDataFile.flush()
    serviceDataFile.close()

# END IF: File creation sequence on file not found



#
# load info from the file into program
serviceDataFile = open(SERVICE_INFO_FILE_PATH, "rt")

#
# Read from file and store for use in program
# Info is stored in this order: hash algorithm, master password's hash, 
#   then all of the services and their maximum password lengths (to truncate the password to)

# Use split() function to parse strings?

hashAlgorithm = serviceDataFile.readline().split(':')[1].strip()
hashedMasterPassword = serviceDataFile.readline().split(':')[1].strip()
serviceDictionary = {}
for line in serviceDataFile:
    service = line.split(':')
    serviceDictionary[service[0]] = service[-1]

#close service info file (as we're done with it for this execution)
serviceDataFile.close()


# Ask the user for master password
print(f"MasterHash is : {hashedMasterPassword}") # debug print
masterPasswordPlaintext = getpass.getpass("\tEnter " + PROGRAM_NAME + " Master Password [input is hidden]: ")
# compare Hash to the hash stored in password data file
while not verifyPass(masterPasswordPlaintext, hashedMasterPassword, hashAlgorithm):
    # if NOT matching: ask for re-try UNTIL successful hash-match
    print("\tLogin failed\n\tPlease try again")
    masterPasswordPlaintext = getpass.getpass("\tEnter " + PROGRAM_NAME + " Master Password [input is hidden]: ")


#
# Ask the user which service they want their password for
serviceName = input("\nEnter Service Name: ")

while(serviceName == ''): # re-try until you get an input
    print("\n\tPlease enter the name of the service you would like to retrieve your password for.")
    serviceName = input("\nEnter Service Name: ")


# if service NOT found from Data File's original reading:
if(serviceName not in serviceDictionary):

    # Notify the user that they need to register the new service
    print("\n\tService \"" + serviceName + "\" not registered.\n\t\tBeginning Registration to file \"" + serviceDataFile.name + "\".")

    # Ask the user for the max length allowed for the password
    maxPassLength = input("\n\tEnter Maximum " + serviceName + " Password Length: ")

    while(str(maxPassLength) == ''): # re-try until you get an input
        print("\n\tPlease enter the maximum character length for a " + serviceName + " password.")
        maxPassLength = input("\n\tEnter Maximum " + serviceName + " Password Length: ")
        
    #
    # Append this service into the data file w/ the information
    serviceDataFile = open(SERVICE_INFO_FILE_PATH, "at")
    serviceDataFile.write(serviceName + ':' + str(maxPassLength) + '\n')
    serviceDataFile.close()

# END: registration of new service



#
# Take the selected service's name and append it to end of master password plaintext given earlier

# Hash the newly-concatenated string, resulting in the service's password


# Trim the resulting hash sequence to the max length specified in the data file



#
# Copy the password to the user's clipboard
pyperclip.copy(hashedMasterPassword)

print("\n\t\tCopied " + serviceName + " Password to Clipboard.\n")


# Wait a few seconds, then clear the user's clipboard to clear the password data
sleep(10)

if(pyperclip.paste() == hashedMasterPassword):
    pyperclip.copy("")


#
# cleanup values in memory for security purposes
hashedMasterPassword = ''
del hashedMasterPassword


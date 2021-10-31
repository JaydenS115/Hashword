#########################################################
#  CS-47206: Data Security and Privacy - Course Project #
#  By: Cieara Pfeifer, Jayden Stearns, & Jarrett Woo    #
#########################################################

#imports
import os
from io import TextIOWrapper
import getpass
import hashlib


# Program Opener and Information display
PROGRAM_NAME = "Hashword"
VERSION = "0.1.4"
DESCRIPTION = "Password Generator and Handler"
print("\n\n\t\t" + PROGRAM_NAME + " \t[v" + VERSION + "]\n\n\t\t" + DESCRIPTION + "\n\n")



SERVICE_INFO_FILE_PATH = "ServiceData.dat"  # the desired and checked-for name of service data file


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


#hashAlgorithm = 
#hashedMasterPassword = 
#serviceDictionary = 



        # Ask the user for master password


        # Hash the master password


        # compare Hash to the hash stored in password data file

            # if NOT matching: ask for re-try UNTIL successful hash-match




# Ask the user which service they want their password for


    # if service NOT found in Data File:
    

        # Notify the user that they need to register the new service
        # Ask the user for the max length allowed for the password
        
        # Enter this service into the data file w/ the information

    

#close service info file (done with it for this execution)
serviceDataFile.close()


# Take the selected service's name and append it to end of master password given earlier

# Hash the newly-concatenated string, resulting in the service's password


# Trim the resulting hash sequence to the max length specified in the data file



# Copy the password to the user's clipboard (for ease-of-use, only if possible)



# Wait a few seconds, then clear the user's clipboard to clear the password data


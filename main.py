#########################################################
#  CS-47206: Data Security and Privacy - Course Project #
#  By: Cieara Pfeifer, Jayden Stearns, & Jarrett Woo    #
#########################################################



# Try to open file "PassData.dat" (or something like that)


    #if NOT opened: create new file of that name

        # Ask user for master password to use for file
        # Hash the master password
        # store the password to the new file



    #if opened: try to load info from the file into program

        # Ask the user for master password
        # Hash the master password
        # compare Hash to the hash stored in password data file

            # if NOT matching: ask for re-try until successful match




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


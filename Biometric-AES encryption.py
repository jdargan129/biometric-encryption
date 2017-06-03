
#usr/share/doc/python-fingerprint
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import tempfile
import time
from pyfingerprint.pyfingerprint import PyFingerprint
import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def enroll():
    
    ## Enrolls new finger
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)


    ## Gets some sensor information
    print('Currently stored templates: ' + str(f.getTemplateCount()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
        
  ## Gets new position number (the counting starts at 0, so we do not need to increment)
        #positionNumber = f.getTemplateCount()
        
        if ( positionNumber >= 0 ):
            f.loadTemplate(positionNumber, 0x01)
            characterics = str(f.downloadCharacteristics(0x01))
            passhashes = hashlib.sha256(characterics).hexdigest()
            passhash = passhashes[0:32]
            print('Template already exists at position #' + str(positionNumber))
            return passhash

            
        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers and creates a template
        f.createTemplate()

        ## Gets new position number (the counting starts at 0, so we do not need to increment)
        positionNumber = f.getTemplateCount()

        ## Saves template at new position number
        if ( f.storeTemplate(positionNumber) == True ):
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
            ## Hashes characteristics of template
            
            characterics = str(f.downloadCharacteristics(0x01))
            passhashes = hashlib.sha256(characterics).hexdigest()
            passhash = passhashes[0:32]
            ## Hashes characteristics of template
            print('SHA-2 hash of template: ' + passhash)
            return passhash
            
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
        #print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
            
    
def index():
    

    ## Shows the template index table
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently stored templates: ' + str(f.getTemplateCount()))

    ## Tries to show a template index table page
    try:
        page = raw_input('Please enter the index page (0, 1, 2, 3) you want to see: ')
        page = int(page)

        tableIndex = f.getTemplateIndex(page)

        for i in range(0, len(tableIndex)):
            print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
def fp_download():

    ## Reads image and download it

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently stored templates: ' + str(f.getTemplateCount()))

    ## Tries to read image and download it
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        print('Downloading image (this take a while)...')

        imageDestination =  tempfile.gettempdir() + '/fingerprint.bmp'
        f.downloadImage(imageDestination)

        print('The image was saved to "' + imageDestination + '".')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def delete():
        
    from pyfingerprint.pyfingerprint import PyFingerprint


    ## Deletes a finger from sensor
    ##


    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently stored templates: ' + str(f.getTemplateCount()))

    ## Tries to delete the template of the finger
    try:
        positionNumber = raw_input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def fp_search():
        
    """
    PyFingerprint
    Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
    All rights reserved.

    @author: Bastian Raschke <bastian.raschke@posteo.de>
    """


    ## Search for a finger
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently stored templates: ' + str(f.getTemplateCount()))

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01))

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
def get_decision():#initial message at the start at the program
    decision = ""
    print "encryption/decryption software: \nDesigned and developed by Joshua Dargan \nPlease choose any of the following options"
    print "1 - Start"
    print "2 - Quit"
    print "Decision"
    decision = raw_input()
    return decision

def AES_full(passhash):
    EncDec = passhash
    choice1 = ""
    while choice1 is not "1" and choice1 is not "2" :
        print "choose Encryption or Decryption" 
        print "1 - Encrypt/Decrypt"
        print "2 - Main Menu"
        print "\nDecision: "
        choice1 = raw_input()
   

    if choice1 == "1":
        print "\nEncryption/Decryption"
        AESmenu(EncDec)

    if choice1 == "2":
        print "\nMain Menu"
        main()
        
def encrypt(key, filename):
	chunksize = 64*1024
	#print filename
	#print "4th time: ", key
	outputFile = "(encrypted)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize)
			outfile.write(IV)
			
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]
	
	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)

"""def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()"""
def file_check(filename):
    try:
        open(filename, 'r')
        return 1
    except:
        print "This file doesnt exist"
        return 0
    


def AESmenu(EncDec):
    
    choice = raw_input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    f_in = raw_input("Insert the filename with extension: ")
    fileblob = file_check(f_in)
    while fileblob == 0:
        f_in = raw_input("insert the filename with extensions")
        fileblob = file_check(f_in)
    print f_in    
    #print "3rd time: ", EncDec
    if choice == 'E':
            #filename = raw_input("File to encrypt: ")
            encrypt(EncDec, f_in)
            print "Done."
    elif choice == 'D':
            decrypt(EncDec, f_in)
            print "Done."
    else:
            print "No Option selected, closing..."

        
def main ():


    decision = get_decision()
    while decision is not "quit" and decision is not "2":
        print "Please choose form the following."
        choice = ""
        while choice is not "1" and choice is not "2" and choice is not "3" and choice is not "4" and choice is not "5":
            print "Would you like to choose"
            print "1 - Enroll"
            print "2 - Show Finger Print Index"
            print "3 - Search Finger Print Index"
            print "4 - Download Finger Print Image File"
            print "5 - Delete Finger Print"
            print "\nDecision: "
            choice = raw_input()
        
        if choice == "1":
            print "\nBiometric Enrollment"
            hashcode = enroll()
            print hashcode
            AES_full(hashcode)
                
        if choice == "2":
            print "\nShow Biometric Index"
            index()
            
        if choice == "3":
            print "\nSearch Index Using Biometrics"
            fp_search()
            
        if choice == "4":
            print "\nDownload Biometric Image"
            fp_download()
            
        if choice == "5":
            print "\nDelete Biometric Image"
            delete()
    
    
            
       
            '''
            print "The message inserted was: %s " % message
            ciphertext = encrypt(message , m)
            print "Lets apply RC4 with salt for security"
            cipherplay = ''.join(ciphertext)
            RC = encryptRC(cipherplay, matrix_key)
            print "Message with RC4 with salt"
            print RC
            print "Do you want to save the message to a file? (Y/N)"
            answer = raw_input()
            while answer is not "Y" and answer is not "y" and answer is not "N" and answer is not "n":
                print "Do you want to save the message to a file? (Y/N)"
                answer = raw_input()
            if answer == "Y" or answer == "y":
                fout = open('Encrypted.txt', 'w')
                fout.write(RC)
                fout.close()
                print "Message save to file Encrypted.txt on the folder of this program\n"
                print "Press Enter to continue:"
                raw_input()
            else:
                print "Press enter to continue"
                raw_input()
            decision = get_decision()
        
        elif choice == "2":
            ch_enc = ""
            print "\nMessage Decryption:"
            print "1 - Open a custom file"
            print "2 - Copy the encrypted message"
            ch_enc = raw_input()
            if ch_enc == "1":
                print "Insert the filename with extension"
                f_in = raw_input()
                file = file_check(f_in)
                
                while file == 0:
                    print "Insert the filename with the extension"
                    f_in = raw_input()
                    file = file_check(f_in)
                    
                fin = open(f_in, 'U')
                RCmessage = fin.read()
                fin.close()

            elif ch_enc == "2":
                print "Insert the encripted message:"
                RCmessage = raw_input()
            
            print "You inserted ", RCmessage
            ms = decryptRC(RCmessage, matrix_key)
            message = get_message(ms)
            plaintext = decrypt(message, m)
            print "\nPress enter to continue"
            raw_input()
            decision = get_decision()
        
        else:
            print "Wrong Choice"
    print "Thanks for using the software \nGood Bye"    
    raw_input()
    '''        
if __name__ == "__main__":
    main()

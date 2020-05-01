import sys
import shutil
import os
import in_place

# customExit: Function for custom exit messages
def customExit(msg):
  print(msg)
  sys.exit(1)
  
  
# usage: Exit function with usage info
def usage():
  customExit('Usage:\n\
  python3 add_face.py -f <IMAGE_FILE_ADDRESS> [-n "<PERSON_NAME>"] \n')
  sys.exit(1)
  
  
# handleArguments: checks for correct number of arguments passed and parses file and person name accordingly
def handleArguments():
  # omit the script name itself from arguments
  args = sys.argv[1:]
  
  # empty args
  if not args:
    usage()
  
  # check for next flag
  if len(args) == 2:
    if args[0] != '-f':
      usage()
    
    else:
      fileName = args[1]
      pathParts = fileName.split('/')
      nameParts = pathParts[-1].split('.')
      personName = nameParts[0]
    
      # if more than 2 dots in the file name
      if len(nameParts) > 2:
        print('Unable to parse person name from file name. Type in the name manually. \n')
        usage()
    
  elif len(args) == 4:
    if args[0] != '-f' and args[0] != '-n':
      usage()
      
    elif args[0] == '-f' and args[2] == '-n':
      fileName = args[1]
      personName = args[3]
    
    elif args[2] == '-f' and args[0] == '-n':
      fileName = args[3]
      personName = args[1]
    
    else:
      usage()
    
  else:
    usage()
  
  if not os.path.isfile(fileName):
    customExit('File not found!\n')
    
  return fileName, personName
  

# moveFile: move image file from wherever it is, to the image folder for the face recognition code
def moveFile(filePath):
    ########## EDIT THE LINE BELOW TO CHANGE IMAGE DIRECTORY ##########
    destDirectory = ''
    
    pathParts = filePath.split('/')
    fileName = pathParts[-1]
    destLocation = os.path.join(destDirectory, fileName)
    fileNameParts = fileName.split('.')
    fileExtension = "." + fileNameParts[- 1]
    counter = 0
    
    # check if need to move file
    if os.path.realpath(filePath) == os.path.realpath(destLocation):
      print('WARNING: Image file already present in face recognition image directory. Possible double addition to face recognition code.\n')
      return filePath
      
    # check if the file already exists
    while os.path.isfile(destLocation) and counter < 3:
      counter += 1
      print("File with same name exists in the location directory!")
      userSays = input("Do you wish to rename the file at the destination?(Y/N)\n")
      
      if userSays == "Y" or userSays == "y":
        getNewName = input("New File Name (without extension): ")
        destLocation = os.path.join(destDirectory, getNewName + fileExtension)
        
      else:
        customExit("Could not move image file. Need to rename image file!\n")
        
    if os.path.exists(destLocation):
      customExit("Could not move image file. Need to rename image file!\n")
      
    # if everything else is successful
    shutil.copyfile(filePath, destLocation)
    return destLocation
    
    
# editFaceRecognitionCode: adds the required lines in the face recognition code
def editFaceRecognitionCode(imageFile, personName):
  ########## EDIT THE 2 LINES BELOW TO CHANGE IMAGE DIRECTORY OR SOURCE CODE LOCATION ##########
  sourceFile = 'face_recognition_webcam_mt.py'
  imageFileSource = ''
  
  imageFileParts = imageFile.split('/')
  imageFileName = imageFileParts[-1]
  
  # check if correct
  if os.path.exists(sourceFile):
    with in_place.InPlace(sourceFile, backup_ext=".bak") as file:
      for line in file:
        file.write(line)
        if line.startswith('    known_face_encodings = ['):
          file.write('        FaceRecognition.face_encodings(FaceRecognition.load_image("'+ os.path.join(imageFileSource, imageFileName) +'"))[0],\n')
        elif line.startswith('    known_face_names = ['):
          file.write('        "'+ personName +'",\n')
  else:
    customExit("Incorrect path for face recognition code source. \n Need to modify in editFaceRecognitionCode function.")

  print("Person successfully added to face recognition!\n")
  return


def main():
  # get the arguments
  filePath, personName = handleArguments()
  
  # move the file to the correct location
  newImageFile = moveFile(filePath)
  
  # edit the other code file
  editFaceRecognitionCode(newImageFile, personName)

# Call main() - entry point for the main program
main()

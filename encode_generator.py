# Import required libraries
import cv2  # OpenCV for image processing
import face_recognition  # For facial recognition tasks
import pickle  # For serializing and deserializing Python objects
import os  # For file and directory operations
import firebase_admin  # Firebase SDK for Python
from firebase_admin import credentials  # For Firebase authentication
from firebase_admin import db  # For Firebase Realtime Database
from firebase_admin import storage  # For Firebase Storage

# Initialize Firebase with credentials
cred = credentials.Certificate("YOUR FIREBASE CREDENTIALS")  # Load Firebase credentials from JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': "YOUR DATABASE URL",  # Firebase Realtime Database URL
    "storageBucket": "YOUR STORAGE CREDENTIALS"  # Firebase Storage bucket URL
})

# Set up image processing
folderPath = 'Files/Images'  # Path to folder containing student images
pathList = os.listdir(folderPath)  # Get list of all files in the folder
print(pathList)  # Print list of files

imgList = []  # List to store loaded images
studentIds = []  # List to store student IDs

# Process each image in the folder
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))  # Load image and add to imgList
    studentIds.append(os.path.splitext(path)[0])  # Extract student ID from filename (without extension)
    
    # Upload image to Firebase Storage
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)  # Print list of student IDs

def findEncodings(imagesList):
    """
    Generate facial encodings for all images in the provided list
    """
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        encode = face_recognition.face_encodings(img)[0]  # Generate facial encoding
        encodeList.append(encode)
    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)  # Generate encodings for all images
encodeListKnownWithIds = [encodeListKnown, studentIds]  # Combine encodings with student IDs
print("Encoding Complete")

# Save encodings to file
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

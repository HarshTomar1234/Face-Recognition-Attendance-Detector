# import os
# import pickle
# import numpy as np
# import cv2
# import face_recognition
# import cvzone
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
# import numpy as np
# from datetime import datetime


# cred = credentials.Certificate("face-attendence-detector-firebase-adminsdk-8dt17-8e428b10d6.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://face-attendence-detector-default-rtdb.firebaseio.com/",
#     "storageBucket" : "face-attendence-detector.appspot.com"
# })

# bucket = storage.bucket()

# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 4800)

# imgBackground = cv2.imread('Files/Resources/background.png')

# # Importing the mode images into a list
# folderModePath = 'Files/Resources/Modes'
# modePathList = os.listdir(folderModePath)
# imgModeList = []
# for path in modePathList:
#     imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# # print(len(imgModeList))

# # Load the encoding file
# print("Loading Encode File ...")
# file = open('EncodeFile.p', 'rb')
# encodeListKnownWithIds = pickle.load(file)
# file.close()
# encodeListKnown, studentIds = encodeListKnownWithIds
# # print(studentIds)
# print("Encode File Loaded")

# modeType = 0
# counter = 0
# id = -1
# imgStudent = []

# while True:
#     success, img = cap.read()

#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#     imgBackground[162:162 + 480, 55:55 + 640] = img
#     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#     if faceCurFrame:
#         for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             # print("matches", matches)
#             # print("faceDis", faceDis)

#             matchIndex = np.argmin(faceDis)
#             # print("Match Index", matchIndex)

#             if matches[matchIndex]:
#                 # print("Known Face Detected")
#                 # print(studentIds[matchIndex])
#                 y1, x2, y2, x1 = faceLoc
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                 bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#                 imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
#                 id = studentIds[matchIndex]
#                 if counter == 0:
#                     cvzone.putTextRect(imgBackground, "Loading", (275, 400))
#                     cv2.imshow("Face Attendance", imgBackground)
#                     cv2.waitKey(1)
#                     counter = 1
#                     modeType = 1

#         if counter != 0:

#             if counter == 1:
#                 # Get the Data
#                 studentInfo = db.reference(f'Students/{id}').get()
#                 print(studentInfo)
#                 # Get the Image from the storage
#                 blob = bucket.get_blob(f'Files/Images/{id}.png')
#                 array = np.frombuffer(blob.download_as_string(), np.uint8)
#                 imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
#                 # Update data of attendance
#                 datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
#                                                    "%Y-%m-%d %H:%M:%S")
#                 secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
#                 print(secondsElapsed)

#                 if secondsElapsed > 30:
#                     ref = db.reference(f'Students/{id}')
#                     studentInfo['total_attendance'] += 1
#                     ref.child('total_attendance').set(studentInfo['total_attendance'])
#                     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 else:
#                     modeType = 3
#                     counter = 0
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#             if modeType != 3:

#                 if 10 < counter < 20:
#                     modeType = 2

#                 imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#                 if counter <= 10:

#                     cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    
#                     cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    
#                     cv2.putText(imgBackground, str(id), (1006, 493),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    
#                     cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
#                     cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
#                     cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    


#                     (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
#                     offset = (414 - w) // 2
#                     cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

#                     imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

#                 counter += 1

#                 if counter >= 20:
#                         counter = 0
#                         modeType = 0
#                         studentInfo = []
#                         imgStudent = []
#                         imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#     else:
#         modeType = 0
#         counter = 0

#     # cv2.imshow("Webcam", img)
#     cv2.imshow("Face Attendance", imgBackground)
#     cv2.waitKey(1)



###############################################################################################




# import os
# import pickle
# import numpy as np
# import cv2
# import face_recognition
# import cvzone
# import firebase_admin
# from firebase_admin import credentials, db, storage
# from datetime import datetime

# # Initialize Firebase
# cred = credentials.Certificate("face-attendence-detector-firebase-adminsdk-8dt17-8e428b10d6.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://face-attendence-detector-default-rtdb.firebaseio.com/",
#     "storageBucket": "face-attendence-detector.appspot.com"
# })

# bucket = storage.bucket()

# # Initialize video capture
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)  # Set video width
# cap.set(4, 480)  # Set video height

# # Load the background image
# imgBackground = cv2.imread('Files/Resources/background.png')

# # Load mode images
# folderModePath = 'Files/Resources/Modes'
# modePathList = os.listdir(folderModePath)
# imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# # Load encoded faces
# print("Loading Encode File ...")
# with open('EncodeFile.p', 'rb') as file:
#     encodeListKnownWithIds = pickle.load(file)
# encodeListKnown, studentIds = encodeListKnownWithIds
# print("Encode File Loaded")

# # Initialize variables
# modeType = 0  # Mode type for different screens
# counter = 0  # Counter for time tracking
# id = -1  # ID for recognized student
# imgStudent = []  # Student image for display
# prev_frame = None  # For motion detection in liveness check

# def check_liveness(frame):
#     """
#     Enhanced liveness detection with multiple checks.
#     """
#     global prev_frame

#     # 1. Texture Analysis
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     texture_score = np.std(gray - blurred)  # Calculate texture score
    
#     # 2. Eye Detection
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#     eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)  # Detect eyes
    
#     # 3. Color Variance Check
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     color_variance = np.std(hsv[:, :, 1])  # Variance in saturation channel
    
#     # 4. Motion Detection
#     motion_score = 0
#     if prev_frame is not None:
#         # Ensure frames have the same dimensions for motion detection
#         if prev_frame.shape == gray.shape:
#             frame_diff = cv2.absdiff(prev_frame, gray)
#             motion_score = np.mean(frame_diff)  # Mean of the difference
#         else:
#             print("Warning: Frame sizes do not match for motion detection")
    
#     prev_frame = gray.copy()  # Update prev_frame

#     # Scoring system for liveness check
#     score = 0
#     if texture_score > 5:  # Check 1: Texture
#         score += 1
#     if len(eyes) >= 2:  # Check 2: Eye Detection
#         score += 1
#     if color_variance > 20:  # Check 3: Color Variance
#         score += 1
#     if motion_score > 0.5:  # Check 4: Motion
#         score += 1
    
#     return score >= 3  # Return true if enough checks pass

# # Main loop
# while True:
#     success, img = cap.read()  # Read current frame

#     # Resize image for faster processing
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
#     # Detect faces in current frame
#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
#     # Place current frame on background image
#     imgBackground[162:162 + 480, 55:55 + 640] = img
#     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
#     if faceCurFrame:  # If faces are detected
#         for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#             # Extract face for liveness check
#             y1, x2, y2, x1 = [coord * 4 for coord in faceLoc]
#             face_img = img[y1:y2, x1:x2]  # Get the face image
            
#             # Check liveness before proceeding
#             if not check_liveness(face_img):
#                 cvzone.putTextRect(imgBackground, "Spoof Detected!", (275, 400))
#                 modeType = 4  # Switch to "spoof detected" mode
#                 counter = 0
#                 imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Update the display
#                 cv2.imshow("Face Attendance", imgBackground)
#                 continue  # Skip further processing
            
#             # If liveness check passes, proceed with face recognition
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             matchIndex = np.argmin(faceDis)
            
#             if matches[matchIndex]:  # If a known face is detected
#                 # Draw bounding box around the face
#                 bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#                 imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
#                 id = studentIds[matchIndex]  # Get the ID of the recognized student
                
#                 if counter == 0:
#                     cvzone.putTextRect(imgBackground, "Loading", (275, 400))  # Show loading text
#                     cv2.imshow("Face Attendance", imgBackground)
#                     cv2.waitKey(1)
#                     counter = 1  # Start counting
#                     modeType = 1  # Switch to loading mode

#         if counter != 0:  # If a face was recognized
#             if counter == 1:  # First frame with a recognized face
#                 # Get student data from database
#                 studentInfo = db.reference(f'Students/{id}').get()
                
#                 # Get student image from storage
#                 blob = bucket.get_blob(f'Files/Images/{id}.png')
#                 array = np.frombuffer(blob.download_as_string(), np.uint8)
#                 imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)  # Decode student image
                
#                 # Update attendance time in database
#                 datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
#                 secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                
#                 if secondsElapsed > 30:  # Check if 30 seconds have passed since last attendance
#                     ref = db.reference(f'Students/{id}')
#                     studentInfo['total_attendance'] += 1  # Increment attendance count
#                     ref.child('total_attendance').set(studentInfo['total_attendance'])
#                     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 else:
#                     modeType = 3  # Set mode to show attendance already marked
#                     counter = 0
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#             if modeType != 3:  # If not in attendance already marked mode
#                 if 10 < counter < 20:
#                     modeType = 2  # Set mode to show processing

#                 imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#                 if counter <= 10:
#                     # Display student info on background
#                     cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), 
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(id), (1006, 493),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

#                     (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
#                     offset = (414 - w) // 2
#                     cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

#                     imgBackground[175:175 + 216, 909:909 + 216] = imgStudent  # Show student image

#                 counter += 1  # Increment the counter

#                 if counter >= 20:  # Reset after certain frames
#                     counter = 0
#                     modeType = 0  # Reset to initial mode
#                     studentInfo = []  # Clear student info
#                     imgStudent = []  # Clear student image
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Reset background mode
#     else:
#         modeType = 0  # Reset mode if no face detected
#         counter = 0  # Reset counter

#     cv2.imshow("Face Attendance", imgBackground)  # Show updated background
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
#         break

# cap.release()  # Release video capture
# cv2.destroyAllWindows()  # Close all OpenCV windows





############################################################################
############################################################################




import os  # For interacting with the operating system
import pickle  # For reading the encoded face data
import numpy as np  # For numerical operations
import cv2  # For computer vision tasks
import face_recognition  # For recognizing faces
import cvzone  # For easier OpenCV functions (like drawing text)
import firebase_admin  # For interacting with Firebase
from firebase_admin import credentials  # For managing credentials
from firebase_admin import db  # For accessing the Firebase database
from firebase_admin import storage  # For accessing Firebase storage
from datetime import datetime  # For handling date and time

# Initialize Firebase with the given credentials
cred = credentials.Certificate("YOUR FIREBASE CREDENTIALS")
firebase_admin.initialize_app(cred, {
    'databaseURL': "YOUR DATABASE URL",
    "storageBucket": "YOUR STORAGE CREDENTIALS"
})

# Reference to the Firebase storage bucket
bucket = storage.bucket()

# Start video capture from the default camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set video width to 640 pixels
cap.set(4, 480)  # Set video height to 480 pixels

# Load the background image for the display
imgBackground = cv2.imread('Files/Resources/background.png')

# Load mode images into a list for different display modes
folderModePath = 'Files/Resources/Modes'
modePathList = os.listdir(folderModePath)  # Get list of all mode images
imgModeList = []  # Initialize a list to hold the mode images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))  # Read each mode image

# Load the encoding file containing known face encodings and their corresponding IDs
print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:  # Use context manager to open file
    encodeListKnownWithIds = pickle.load(file)  # Load the encoded faces from the file
encodeListKnown, studentIds = encodeListKnownWithIds  # Unpack the loaded data
print("Encode File Loaded")

# Initialize variables for tracking modes, counters, and student info
modeType = 0  # Current mode of operation
counter = 0  # Counter for managing display timing
id = -1  # Placeholder for recognized student's ID
imgStudent = []  # Placeholder for the student's image

# Main loop for capturing frames and processing them
while True:
    success, img = cap.read()  # Capture a frame from the webcam

    # Resize the captured image for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB

    # Detect faces in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)  # Get locations of faces
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # Get encodings of detected faces

    # Overlay the captured image on the background image
    imgBackground[162:162 + 480, 55:55 + 640] = img  
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Display current mode image

    # Process detected faces
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):  # Iterate through detected faces
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # Compare with known faces
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # Calculate distance from known faces

            # Find the index of the closest match
            matchIndex = np.argmin(faceDis)  # Get the index of the closest match

            if matches[matchIndex]:  # If a match is found
                y1, x2, y2, x1 = faceLoc  # Get the face location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale face location back to original size
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1  # Define bounding box for the face
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)  # Draw rectangle around the face
                id = studentIds[matchIndex]  # Get the ID of the recognized student
                if counter == 0:  # If it's the first time the face is recognized
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))  # Display loading text
                    cv2.imshow("Face Attendance", imgBackground)  # Show the image
                    cv2.waitKey(1)  # Wait for a brief moment
                    counter = 1  # Set counter to 1
                    modeType = 1  # Switch to loading mode

        if counter != 0:  # If a face was recognized
            if counter == 1:  # If it's the first counter increment
                # Get student data from the database using the recognized ID
                studentInfo = db.reference(f'Students/{id}').get()  
                print(studentInfo)  # Print the student information for debugging

                # Get the student's image from Firebase storage
                blob = bucket.get_blob(f'Files/Images/{id}.png')  
                array = np.frombuffer(blob.download_as_string(), np.uint8)  # Convert the blob to an array
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)  # Decode the image

                # Update attendance data
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")  # Parse last attendance time
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()  # Calculate time since last attendance
                print(secondsElapsed)  # Print elapsed time for debugging

                # If more than 30 seconds have passed, update attendance
                if secondsElapsed > 60:  
                    ref = db.reference(f'Students/{id}')  # Reference the student's data
                    studentInfo['total_attendance'] += 1  # Increment the attendance count
                    ref.child('total_attendance').set(studentInfo['total_attendance'])  # Update in Firebase
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Update last attendance time
                else:  # If attendance was marked too recently
                    modeType = 3  # Switch to mode indicating attendance already marked
                    counter = 0  # Reset counter
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Update background image

            # Update the display for attendance information
            if modeType != 3:  # If we are not in attendance already marked mode
                if 10 < counter < 20:  # Switch to processing mode after some frames
                    modeType = 2  

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Update the mode image

                if counter <= 10:  # During the initial frames of display
                    # Display various student information on the background
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    # Center the name text on the display
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)  # Get text size
                    offset = (414 - w) // 2  # Calculate offset for centering
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # Display the student's image on the background
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1  # Increment counter for display timing

                if counter >= 20:  # Reset after a certain number of frames
                    counter = 0  # Reset the counter
                    modeType = 0  # Reset to initial mode
                    studentInfo = []  # Clear student info
                    imgStudent = []  # Clear student image
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Reset background mode
    else:  # If no face is detected
        modeType = 0  # Reset mode if no face detected
        counter = 0  # Reset counter

    # Show the updated background image with attendance info
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)  # Wait for 1 millisecond before the next frame


####################################################################

###############################################################33

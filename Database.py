import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase Admin with credentials
cred = credentials.Certificate("face-attendence-detector-firebase-adminsdk-8dt17-8e428b10d6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendence-detector-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendence-detector.appspot.com"  # Specify the storage bucket
})

# Set up the storage bucket for Firebase
bucket = storage.bucket()

ref = db.reference('Students')

data = {
    "123":
        {
            "name": "Harsh Tomar",
            "major": "AIDS",
            "starting_year": 2023,
            "total_attendance": 17,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "036912":
        {
            "name": "Eminem",
            "major": "Literature",
            "starting_year": 2016,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "098456":
        {
            "name": "Christopher Nolan",
            "major": "Literature",
            "starting_year": 2013,
            "total_attendance": 54,
            "standing": "G",
            "year": "6",
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "0123021":
        {
            "name": "Nick Vujicic",
            "major": "Commerce and Finance",
            "starting_year": 2015,
            "total_attendance": 27,
            "standing": "G",
            "year": "7",
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "123654":
        {
            "name": "Leonardo DiCaprio",
            "major": "Arts, Acting",
            "starting_year": 2012,
            "total_attendance": 37,
            "standing": "G",
            "year": "15",
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "147852":
        {
            "name": "Ana de Armas",
            "major": "Arts, Acting",
            "starting_year": 2018,
            "total_attendance": 7,
            "standing": "G",
            "year": 14,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "369852":
        {
            "name": "Cillian Murphy",
            "major": "Law and Political Science",
            "starting_year": 2014,
            "total_attendance": 7,
            "standing": "G",
            "year": "6",
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "789456":
        {
            "name": "Monica Bellucci",
            "major": "Law and Political Science",
            "starting_year": 2015,
            "total_attendance": 7,
            "standing": "G",
            "year": "8",
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "852741":
        {
            "name": "Emily Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Robotics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)

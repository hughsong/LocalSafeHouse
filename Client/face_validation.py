# SOURCE FILE:    face_validation.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      1. extract & decrypt the user photo
#                 2. identify face from real-time face recognition
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import face_recognition
#from encrypt_photo import *
from stego_photo import *
import time

# Get a reference to webcam #0 (the default one)
def check_face():
    # decode user image
    path = get_path()
    user_photo_name = path+"/image/User_org.png"
    load_decode_image()
    video_capture = cv2.VideoCapture(0)
    user_image = []
    user_face_encoding = []
    # Load a sample picture and learn how to recognize it.
    user_image.append(face_recognition.load_image_file(user_photo_name))
    user_face_encoding.append(face_recognition.face_encodings(user_image[0])[0])
    # user_image.append(face_recognition.load_image_file("/Users/hughsong/Comp8047/image/bidden2.jpg"))
    # user_face_encoding.append(face_recognition.face_encodings(user_image[0])[0])

    # Load a second sample picture and learn how to recognize it.
    # user_image.append(face_recognition.load_image_file("/Users/hughsong/Comp8047/image/baby.JPG"))
    # user_face_encoding.append(face_recognition.face_encodings(user_image[1])[0])

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        user_face_encoding[0],
        # user_face_encoding[1]
    ]
    known_face_names = [
        "Hugh Song"
        # "Caitlyn"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    match = False
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        font = cv2.FONT_HERSHEY_DUPLEX
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    match = True

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if match:
            time.sleep(2)
            break

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    command = "rm "+ user_photo_name
    os.system(command)
    if match:
        return True
    else:
        return False
import face_recognition

# Load employee images and encode them
known_face_encodings = []
known_face_names = []

# Example: Load employee images and encode them
# for employee_image in employee_images:
#     img = face_recognition.load_image_file(employee_image)
#     encoding = face_recognition.face_encodings(img)[0]
#     known_face_encodings.append(encoding)
#     known_face_names.append(employee_name)

# Load attendance image
attendance_image = face_recognition.load_image_file('attendance_image.jpg')
attendance_encodings = face_recognition.face_encodings(attendance_image)

# Recognize employees in attendance image
for encoding in attendance_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, encoding)
    if True in matches:
        matched_employee = known_face_names[matches.index(True)]
        print(f'{matched_employee} is present.')
    else:
        print('Unknown person detected.')

from turtle import pen
import cv2
import face_recognition
import os
import numpy as np
import pickle


def add_file(file, name):
    dbfile = open("encoded_pics", "rb")
    try:
        lb = pickle.load(dbfile)
    except EOFError:
        lb = []
    dbfile.close()
    image = cv2.imread(file)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encoded_face = face_recognition.face_encodings(img)

    lb = lb + [encoded_face[0]]

    file = open("encoded_pics", "wb")
    pickle.dump(lb, file)
    file.close()
    file = open("names.txt", "a")
    file.write(name + "\n")


def predict(inputf):
    file = open("names.txt", "r")
    names = file.readlines()
    file.close()
    pred = []

    dbfile = open("encoded_pics", "rb")
    try:
        lb: dict = pickle.load(dbfile)
    except EOFError:
        lb = []
    img = cv2.imread(inputf)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, _ in zip(encoded_faces, faces_in_frame):
        matches = face_recognition.compare_faces(lb, encode_face)
        faceDist = face_recognition.face_distance(lb, encode_face)
        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            name = names[matchIndex].upper().lower()
            pred.append(name[:-1])
    return pred


# add_file("faces/namah.jpg", "Namah")
# add_file("faces/porwal.jpg", "Yash")
# add_file("faces/mehta.jpg", "Mehta")


# print(predict("./test.jpg"))

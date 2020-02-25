import json
from flask import Flask, escape, request, jsonify

student = [
    {
        "student_id": 1,
        "first_name": "Archit",
        "last_name": "Dhingra",
        "course": "SE"
    },
    {
        "student_id": 2,
        "first_name": "Poojitha",
        "last_name": "Vaddey",
        "course": "SE"
    }
]

classes = [
    {
        "class_id": 112233,
        "class_name": "CMPE273",
        "instructor": "Prof",
        "students": [
        {
            "student_id": 2,
            "first_name": "Poojitha",
            "last_name": "Vaddey",
            "course": "SE"
        }
        ]
    }
]


def student_details(_, info, student_id):
    studs = [stud for stud in student if stud["student_id"] == int(student_id)]    
    return studs[0]

def add_student(_, info, student_id, first_name, last_name, course):
    global student
    student.append({'student_id' : student_id, 'first_name': first_name, 'last_name': last_name, 'course':course})
    #studs = [stud for stud in student if stud["student_id"] == student_id]    
    return student

def class_details(_, info, class_id):
    cl = [cl for cl in classes if cl["class_id"] == int(class_id)]    
    return cl[0]

def add_class(_, info, class_id, class_name, instructor, student_id):
    global classes
    studs = [stud for stud in student if stud["student_id"] == int(student_id[0])]    
    classes.append({"class_id":class_id, "class_name":class_name, "instructor": instructor, "students": studs})
    return classes

def update_class(_, info, class_id, student_id):
    global classes
    index = 0
    studs = [stud for stud in student if stud["student_id"] == int(student_id)]
    for x in classes:
        index = index+1
        if x["class_id"] == int(class_id):
            cl = x
            break
    cl["students"].append(studs[0])
    return cl
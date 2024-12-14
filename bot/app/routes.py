from flask import Blueprint, render_template, jsonify
from Circle import Circle
from .models import *
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    students = get_students()
    labs = get_labs()

    # Organize labs by subject for easy grouping in status_groups
    labs_by_subject = {}
    for lab in labs:
        labs_by_subject.setdefault(lab.subject, []).append(lab)

    queue_items = []
    for student in students:
        # Fetch lab progress for the student
        lab_progress = get_labs_for_student(student_id=student.id)
        lab_progress_dict = {progress.lab_id: progress for progress in lab_progress}

        status_groups = []
        for subject, subject_labs in labs_by_subject.items():
            subject_status = []
            for lab in subject_labs:
                progress = lab_progress_dict.get(lab.id)
                if progress and progress.status == '1':  # Assuming '1' indicates solved
                    status = {'class': Circle.Solved}
                else:
                    status = {'class': Circle.Not_solved}
                subject_status.append(status)
            status_groups.append(subject_status)

        # Append student's queue item
        queue_items.append({
            'number': student.id,
            'name': f"{student.name} {student.surname}",
            'status_groups': status_groups
        })

    return render_template('queue.html', queue_items=queue_items)

def get_students():
    students = Student.query.all()
    return students

def get_labs_for_student(student_id):
    labs = LabProgress.query.filter_by(student_id=student_id).all()
    return labs

def get_labs():
    labs = LabProgress.query.all()
    return labs

def get_lab_by_id(lab_id):
    lab = Lab.query.get(lab_id)
    return lab
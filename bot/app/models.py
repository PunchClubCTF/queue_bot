from datetime import datetime
from . import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    member1_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=True, nullable=False)
    member2_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lab(db.Model):
    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

class LabProgress(db.Model):
    __tablename__ = 'lab_progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'lab_id', name='unique_student_lab'),
    )

class LabQueue(db.Model):
    __tablename__ = 'lab_queue'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    queue_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    priority = db.Column(db.Integer, default=0)  # Added priority field

    __table_args__ = (
        db.CheckConstraint(
            "(student_id IS NOT NULL AND group_id IS NULL) OR (group_id IS NOT NULL AND student_id IS NULL)",
            name='check_student_or_group'
        ),
    )

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Student', backref='audit_logs')  # Relationship for reverse lookup

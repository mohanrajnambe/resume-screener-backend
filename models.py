from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    openingCount = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, nullable=True, default=False)


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    number = db.Column(db.String(255), unique=True, nullable=False)
    isDeleted = db.Column(db.Boolean, nullable=True, default=False)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    jobId = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    relevancyScore = db.Column(db.Integer, nullable=True, default=-1)
    isClosed = db.Column(db.Boolean, nullable=True, default=False)
    acceptStatus = db.Column(db.Boolean, nullable=True, default=False)
    isDeleted = db.Column(db.Boolean, nullable=True, default=False)

    # Define relationships with Job and Candidate models
    job = db.relationship('Job', backref='applications')
    candidate = db.relationship('Candidate', backref='applications')
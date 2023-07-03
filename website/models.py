from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Doctor(db.Model):
    #doctor_id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    tc = db.Column(db.Integer, primary_key=True, nullable = False)
    email = db.Column(db.Integer, unique=True, nullable = False)
    branch = db.Column(db.String(150), nullable = False)
    #birth_date = db.Column(db.DateTime(timezone=True))
    tel_no= db.Column(db.Integer, unique=True)
    hospital= db.Column(db.String(150))

class Patient(db.Model):
    #patient_id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(150))
    email=db.Column(db.String(150),unique=True)
    last_name = db.Column(db.String(160))
    tc = db.Column(db.Integer, primary_key=True, nullable = False)
    #birth_date = db.Column(db.DateTime(timezone=True))
    tel_no = db.Column(db.Integer, unique=True)
    
class Prescription(db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    doctor_tc= db.Column(db.Integer, db.ForeignKey(Doctor.tc))
    patient_tc = db.Column(db.Integer,db.ForeignKey(Patient.tc))
    prescription_date = db.Column(db.String(150), nullable = False, default=func.now())
    valid_time = db.Column(db.Integer , nullable = False)

class Drug(db.Model):
    drug_id= db.Column(db.Integer, primary_key=True)
    usage_content= db.Column(db.String(500), nullable = False)
    name=db.Column(db.String(150),unique=True, nullable = False)
    
class Prescription_content(db.Model):
    prescription_id = db.Column(db.Integer,db.ForeignKey(Prescription.prescription_id), primary_key=True)
    drug_id = db.Column(db.Integer,db.ForeignKey(Drug.drug_id), primary_key=True)
    drug_amount = db.Column(db.Integer , nullable = False)
       
class Id_table(db.Model):
    name = db.Column(db.String(160), primary_key=True)
    id = db.Column(db.Integer, nullable=False)
  



    


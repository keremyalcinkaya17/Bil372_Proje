from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Note, Doctor, Patient, Prescription, Prescription_content, Drug, Id_table
from . import db
import json
from sqlalchemy.sql.expression import select, exists

views = Blueprint('views', __name__)




"""@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})"""

@views.route('/base1', methods=['GET', 'POST'])
def base1():
    return render_template("base1.html")

@views.route('/', methods=['GET', 'POST'])
def home1():
    return render_template("home1.html")

@views.route('/silme', methods=['GET', 'POST'])
def silme():
    if request.method == 'POST':
        hasta_tc=request.form.get('hasta_tc')
        doktor_tc=request.form.get('doktor_tc')
        ilac=request.form.get('ilac')
        recete=request.form.get('recete')
        receteler=[]
        recete_icerikleri=[]
        recete_icerikleri2=[]
        ilaclar=[]
        if recete is not "":
            receteler= Prescription.query.filter_by(prescription_id=recete).first()
            if receteler is not None:
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=receteler.prescription_id).all()
                for row in recete_icerikleri:
                    db.session.delete(row)
                db.session.delete(receteler)
                db.session.commit()
            return render_template("home1.html")
        elif doktor_tc is  not "":
            dk=Doctor.query.filter_by(tc=doktor_tc).first()
            if dk is not None:
                dk1=Prescription.query.filter_by(doctor_tc=doktor_tc).all()
                for row in dk1:
                    recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                    for a in recete_icerikleri:
                        db.session.delete(a)
                    db.session.delete(row)
                db.session.delete(dk)
                db.session.commit()
        elif ilac is not "":
            print(ilac)
            ilaclar=Drug.query.filter_by(drug_id=ilac).all()
            for row in ilaclar:
                icerikler = Prescription_content.query.filter_by(drug_id=ilac)
                for row2 in icerikler:
                    db.session.delete(row2)
                db.session.delete(row)
                db.session.commit()
            
            return render_template("home1.html")
        elif hasta_tc is not "": 
            dk=Patient.query.filter_by(tc=hasta_tc).first()
            if dk is not None:
                dk1=Prescription.query.filter_by(patient_tc=hasta_tc).all()
                for row in dk1:
                    recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                    for a in recete_icerikleri:
                        db.session.delete(a)
                    db.session.delete(row)
                db.session.delete(dk)
                db.session.commit()
            
    return render_template("silme.html")

@views.route('/guncelle', methods=['GET', 'POST'])
def guncelle():
    return render_template("guncelle.html")

@views.route('/hasta_guncelle', methods=['GET', 'POST'])
def hasta_guncelle():
    if request.method == 'POST':
        name=request.form.get('name')
        surname=request.form.get('surname')
        email=request.form.get('email')
        tc=request.form.get('tc')
        tel_no=request.form.get('tel')
        if tc is not "":
            a1 = Patient.query.filter_by(tc =tc).first()
            if a1 is not None:
                if name is not "":
                    a1.name=name
                if surname is not "":
                    a1.last_name = surname
                if email is not "":
                    a2 = Patient.query.filter(Patient.email==email,Patient.tc!=tc).first()
                    if a2 is not None:
                        return render_template("hata9.html") 
                    else:
                        a1.email=email    
                if tel_no is not "":  
                    a3 = Patient.query.filter(Patient.tel_no==tel_no,Patient.tc!=tc).first()
                    if a3 is not None:
                        return render_template("hata10.html") 
                    else:
                        a1.tel_no=tel_no 
                db.session.commit()
                return render_template("home1.html")
            else:
                return render_template("hata1.html")
        else:
            return render_template("hata0.html")
                   
    return render_template("hasta_guncelle.html")

@views.route('/doktor_guncelle', methods=['GET', 'POST'])
def doktor_guncelle():
    if request.method == 'POST':
        name=request.form.get('name')
        surname=request.form.get('surname')
        branch=request.form.get('brans')
        email=request.form.get('email')
        hospital=request.form.get('hospital')
        tc=request.form.get('tc')
        tel_no=request.form.get('tel')
        if tc is not "":
            a1 = Doctor.query.filter_by(tc=tc).first()
            if a1 is not None:
                if email is not "":
                    a2 = Doctor.query.filter(Doctor.email==email,Doctor.tc!=tc).first()
                    if a2 is not None:
                        return render_template("hata7.html") 
                    else:
                        a1.email=email    
                if tel_no is not "":  
                    a3 = Doctor.query.filter(Doctor.tel_no==tel_no,Doctor.tc!=tc).first()
                    if a3 is not None:
                        return render_template("hata8.html") 
                    else:
                        a1.tel_no=tel_no
                if name is not "":
                    a1.name = name
                if surname is not "":
                    a1.last_name = surname
                if branch is not "":
                    a1.branch = branch
                if hospital is not "":
                    a1.hospital = hospital
                db.session.commit()
                return render_template("home1.html") 
            else:
                return render_template("hata6.html")    
        else:
            return render_template("hata5.html") 
    return render_template("doktor_guncelle.html")

@views.route('/ilac_guncelle', methods=['GET', 'POST'])
def ilac_guncelle():
    if request.method == 'POST':
        ilac_id=request.form.get('ilac')
        name=request.form.get('name')
        usage_content=request.form.get('aciklama')
        if ilac_id is not "":
            a1 = Drug.query.filter_by(drug_id=ilac_id).first()
            if a1 is not None:
                if name is not "":
                    a2 = Drug.query.filter(Drug.name==name, Drug.drug_id != ilac_id).first()
                    if a2 is not None:
                        return render_template("hata4.html")
                    else:
                        a1.name=name
                if usage_content is not "":
                    a1.usage_content=usage_content 
                db.session.commit()
                return render_template("home1.html")       
            else:
                return render_template("hata3.html")
        else:
            return render_template("hata2.html")          
    return render_template("ilac_guncelle.html")

@views.route('/recete_guncelle', methods=['GET', 'POST'])
def recete_guncelle():
    if request.method == 'POST':
        recete_id=request.form.get('recete_id')
        doctor_id=request.form.get('doktor_id')
        hasta_id=request.form.get('hasta_id')
        tarih=request.form.get('tarih')
        time=request.form.get('tarih2')
        ilac_id1=request.form.get('ilac_id1')
        sayi1=request.form.get('sayi1')
        ilac_id2=request.form.get('ilac_id2')
        sayi2=request.form.get('sayi2')
        ilac_id3=request.form.get('ilac_id3')
        sayi3=request.form.get('sayi3')
        ilac_id4=request.form.get('ilac_id4')
        sayi4=request.form.get('sayi4')
        ilac_id5=request.form.get('ilac_id5')
        sayi5=request.form.get('sayi5')
        
        if recete_id is not "":
            a0 = Prescription.query.filter_by(prescription_id=recete_id).first()
            if a0 is not None:
                if doctor_id is not "":
                    a0.doctor_tc=doctor_id
                if hasta_id is not "":
                    a0.patient_tc=hasta_id
                if tarih is not "":
                    a0.prescription_date=tarih
                if time is not "":
                    a0.vali_time=time
                
                if ilac_id1 is not "" and sayi1 is not "":
                    a1 = Prescription_content.query.filter_by(prescription_id=recete_id).all()
                    for row in a1:
                        db.session.delete(row)
                    db.session.commit()
                    new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id1,drug_amount=sayi1)
                    try:
                        db.session.add(new_prescription1)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        print("eklenemiyor")
                    finally:
                        db.session.close_all()
                    
                if ilac_id2 is not "" and sayi2 is not "":
                    new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id2,drug_amount=sayi2)
                    try:
                        db.session.add(new_prescription1)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close_all()
                if ilac_id3 is not "" and sayi3 is not "":
                    new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id3,drug_amount=sayi3)
                    try:
                        db.session.add(new_prescription1)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close_all()
                if ilac_id4 is not "" and sayi4 is not "":
                    new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id4,drug_amount=sayi4)
                    try:
                        db.session.add(new_prescription1)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close_all()
                if ilac_id5 is not "" and sayi5 is not "":
                    new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id5,drug_amount=sayi5)
                    try:
                        db.session.add(new_prescription1)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close_all()
                return render_template("home1.html")  

            else:
                return render_template("hata12.html")
        else:
            return render_template("hata11.html")
        
    return render_template("recete_guncelle.html")

@views.route('/sorgu', methods=['GET', 'POST'])
def sorgu():
    if request.method == 'POST':
        hasta_tc=request.form.get('hasta_tc')
        doktor_tc=request.form.get('doktor_tc')
        ilac=request.form.get('ilac')
        recete=request.form.get('recete')
        receteler=[]
        recete_icerikleri=[]
        recete_icerikleri2=[]
        ilaclar=[]
        if recete is not "":
            receteler= Prescription.query.filter_by(prescription_id=recete).all()
            for row in receteler:
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    recete_icerikleri2.append(a)
            return render_template("recete_output.html",receteler=receteler,recete_icerikleri2=recete_icerikleri2,hasta=0,sec=2)
        elif doktor_tc is  not "":
            dk=Doctor.query.filter_by(tc=doktor_tc).first()
            receteler= Prescription.query.filter_by(doctor_tc=doktor_tc).all()
            for row in receteler:
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    recete_icerikleri2.append(a)
            return render_template("recete_output.html",receteler=receteler,recete_icerikleri2=recete_icerikleri2,hasta=0,sec=0,dk=dk)
        elif ilac is not "":
            #print(ilac)
            ilaclar=Drug.query.filter_by(drug_id=ilac).all()
            
            return render_template("recete_output.html",ilaclar=ilaclar,hasta=0,sec=1)
        elif hasta_tc is not "": 
            dk=Patient.query.filter_by(tc=hasta_tc).first()
            receteler= Prescription.query.filter_by(patient_tc=hasta_tc).all()
            for row in receteler:
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    recete_icerikleri2.append(a)
            return render_template("recete_output.html",receteler=receteler,recete_icerikleri2=recete_icerikleri2,hasta=1,sec=0,dk=dk)       
            
            
    return render_template("sorgu.html")

@views.route('/recete_output', methods=['GET', 'POST'])
def recete_output():
    return render_template("recete_output.html")
#doctor_id_generator=0

@views.route('/doktor_kayit', methods=['GET', 'POST'])
def doktor_kayit():
    #global doctor_id_generator
    
    if request.method == 'POST':
        name=request.form.get('name')
        surname=request.form.get('surname')
        branch=request.form.get('brans')
        email=request.form.get('email')
        hospital=request.form.get('hospital')
        tc=request.form.get('tc')
        tel_no=request.form.get('tel')
        
        a1 = Doctor.query.filter_by(tc=tc).first()
        a2 = Doctor.query.filter_by(email=email).first()
        a3 = Doctor.query.filter_by(tel_no=tel_no).first()

        if a1:
            return render_template("hata16.html")
        elif a2:
            return render_template("hata17.html")
        elif a3:
            return render_template("hata18.html")
        else:
            new_doctor= Doctor(name=name,last_name=surname,tc=tc,branch=branch,tel_no=tel_no,email=email,hospital=hospital)
            try:
                db.session.add(new_doctor)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
             
            return redirect(url_for('views.home1'))
    return render_template("doktor_kayit.html")


@views.route('/recete_kayit', methods=['GET', 'POST'])
def recete_kayit():
    if request.method == 'POST':
        recete_id=request.form.get('recete_id')
        doctor_id=request.form.get('doktor_id')
        hasta_id=request.form.get('hasta_id')
        tarih=request.form.get('tarih')
        time=request.form.get('tarih2')
        ilac_id1=request.form.get('ilac_id1')
        sayi1=request.form.get('sayi1')
        ilac_id2=request.form.get('ilac_id2')
        sayi2=request.form.get('sayi2')
        ilac_id3=request.form.get('ilac_id3')
        sayi3=request.form.get('sayi3')
        ilac_id4=request.form.get('ilac_id4')
        sayi4=request.form.get('sayi4')
        ilac_id5=request.form.get('ilac_id5')
        sayi5=request.form.get('sayi5')
        
            
        a1 = Doctor.query.filter_by(tc =doctor_id).first()
        a2 = Patient.query.filter_by(tc =hasta_id).first()
        a3 = Drug.query.filter_by(drug_id = ilac_id1).first()
        a4 = Drug.query.filter_by(drug_id = ilac_id2).first()
        a5 = Drug.query.filter_by(drug_id = ilac_id3).first()
        a6 = Drug.query.filter_by(drug_id = ilac_id4).first()
        a7 = Drug.query.filter_by(drug_id = ilac_id5).first()
        a8 = Prescription.query.filter_by(prescription_id = recete_id).first()
        if a1 is None:
            #print("Doktor TC'si kayıtlı değil")
            return render_template("hata22.html")               
        elif a2 is None:
            #print("Hasta TC'si kayıtlı değil")
            return render_template("hata23.html")     
        elif (a3 is None) and ilac_id1!="":
            #print("İlaç 1 kayıtlı değil")
            return render_template("hata24.html")     
        elif (a4 is None) and ilac_id2!="":
            #print("İlaç 2 kayıtlı değil")
            return render_template("hata25.html") 
        elif (a5 is None) and ilac_id3!="":
            #print("İlaç 3 kayıtlı değil")
            return render_template("hata26.html") 
        elif (a6 is None) and ilac_id4!="":
            #print("İlaç 4 kayıtlı değil")
            return render_template("hata27.html") 
        elif (a7 is None) and ilac_id5!="":
            #print("İlaç 5 kayıtlı değil")
            return render_template("hata28.html") 
        elif a8 is not None:
            return render_template("hata21.html") 
        else:
            new_prescription= Prescription(prescription_id=recete_id,doctor_tc=doctor_id,patient_tc=hasta_id,prescription_date=tarih,valid_time=time)
            try:
                db.session.add(new_prescription)
                db.session.commit()
            except:
                #print(5555555)
                db.session.rollback()
            finally:
                db.session.close_all()
            if ilac_id1!="":
                new_prescription1= Prescription_content(prescription_id=recete_id,drug_id=ilac_id1,drug_amount=sayi1)
            if ilac_id2!="":    
                new_prescription2= Prescription_content(prescription_id=recete_id,drug_id=ilac_id2,drug_amount=sayi2)
            if ilac_id3!="":    
                new_prescription3= Prescription_content(prescription_id=recete_id,drug_id=ilac_id3,drug_amount=sayi3)
            if ilac_id4!="":    
                new_prescription4= Prescription_content(prescription_id=recete_id,drug_id=ilac_id4,drug_amount=sayi4)
            if ilac_id5!="":    
                new_prescription5= Prescription_content(prescription_id=recete_id,drug_id=ilac_id5,drug_amount=sayi5)
            try:
                db.session.add(new_prescription1)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            try:
                db.session.add(new_prescription2)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            try:
                db.session.add(new_prescription3)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            try:
                db.session.add(new_prescription4)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            try:
                db.session.add(new_prescription5)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            
            return render_template("home1.html")             
    return render_template("recete_kayit.html")


#patient_id_generator=0
@views.route('/hasta_kayit', methods=['GET', 'POST'])
def hasta_kayit():
    #global patient_id_generator
    if request.method == 'POST':
        name=request.form.get('name')
        surname=request.form.get('surname')
        email=request.form.get('email')
        tc=request.form.get('tc')
        tel_no=request.form.get('tel')
        a1 = Patient.query.filter_by(tc =tc).first()
        a2 = Patient.query.filter_by(email =email).first()
        a3 = Patient.query.filter_by(tel_no =tel_no).first()
        if a1:
            return render_template("hata13.html")
        elif a2:
            return render_template("hata14.html")
        elif a3:
            return render_template("hata15.html")
        else:
            new_patient= Patient(name=name,last_name=surname,tc=tc,tel_no=tel_no,email=email)
            try:
                db.session.add(new_patient)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            
            #patient_id_generator+=1
            dd=db.engine.execute("SELECT * FROM Patient").fetchall()
            #for row in dd:
                #print(row)   
            return redirect(url_for('views.home1'))   
        
    return render_template("hasta_kayit.html")

@views.route('/ilac_kayit', methods=['GET', 'POST'])
def ilac_kayit():
    if request.method == 'POST':
        drug_id=request.form.get('ilac')
        name=request.form.get('name')
        usage_content=request.form.get('aciklama')
        a1 = Drug.query.filter_by(drug_id=drug_id).first()
        a2 = Drug.query.filter_by(name=name).first()
        if a1:
            return render_template("hata19.html")
        elif a2:
            return render_template("hata20.html")
        else:
            new_drug= Drug(drug_id=drug_id,name=name,usage_content=usage_content)
            try:
                db.session.add(new_drug)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            dd=db.engine.execute("SELECT * FROM Drug").fetchall()
            #for row in dd:
                #print(row)
            flash('İlaç kaydı başarılı.', category='Success')   
            return redirect(url_for('views.home1'))   
        
    return render_template("ilac_kayit.html")



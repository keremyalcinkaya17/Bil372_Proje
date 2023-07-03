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

@views.route('/sorgu', methods=['GET', 'POST'])
def sorgu():
    if request.method == 'POST':
        hasta_tc=request.form.get('hasta_tc')
        doktor_tc=request.form.get('doktor_tc')
        ilac=request.form.get('ilac')
        recete=request.form.get('recete')
        #print(recete is "")
        #print(hasta_tc is "")
        #print(ilac is "")
        #print(doktor_tc is "")
        receteler=[]
        recete_icerikleri=[]
        recete_icerikleri2=[]
        ilaclar=[]
        if recete is not "":
            #print(doktor_tc)
            receteler= Prescription.query.filter_by(prescription_id=recete).all()
            for row in receteler:
                #print(row.prescription_id)
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    #print(a.drug_id)
                    recete_icerikleri2.append(a)
            return render_template("recete_output.html",receteler=receteler,recete_icerikleri2=recete_icerikleri2,hasta=0,sec=2)
        elif doktor_tc is  not "":
            #print(doktor_tc)
            dk=Doctor.query.filter_by(tc=doktor_tc).first()
            #print(dk.name)
            receteler= Prescription.query.filter_by(doctor_tc=doktor_tc).all()
            for row in receteler:
                #print(row.doctor_tc)
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    #print(a.drug_id)
                    recete_icerikleri2.append(a)
            return render_template("recete_output.html",receteler=receteler,recete_icerikleri2=recete_icerikleri2,hasta=0,sec=0,dk=dk)
        elif ilac is not "":
            #print(ilac)
            ilaclar=Drug.query.filter_by(drug_id=ilac).all()
            
            return render_template("recete_output.html",ilaclar=ilaclar,hasta=0,sec=1)
        elif hasta_tc is not "": 
            #print(hasta_tc)
            dk=Patient.query.filter_by(tc=hasta_tc).first()
            #print(dk.name)
            receteler= Prescription.query.filter_by(patient_tc=hasta_tc).all()
            for row in receteler:
                #print(row.doctor_tc)
                recete_icerikleri=Prescription_content.query.filter_by(prescription_id=row.prescription_id).all()
                for a in recete_icerikleri:
                    #print(a.drug_id)
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
        #result = db.session.query(Id_table).with_entities(Id_table.id).filter(Id_table.name=='Doctor').all()
        #a=result.pop(0)
        #print(a)
        if a1:
            print("Kullanilmamis bit tc giriniz")
            flash('Kullanılmamaş bir tc giriniz.', category='error')
        elif a2:
            flash('Kullanılmamaş bir mail giriniz.', category='error')
        elif a3:
            flash('Kullanılmamaş bir telefon numarası giriniz.', category='error')
        else:
            new_doctor= Doctor(name=name,last_name=surname,tc=tc,branch=branch,tel_no=tel_no,email=email,hospital=hospital)
            try:
                db.session.add(new_doctor)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            
             #doctor_id_generator+=1
            #db.session.query(Id_table).filter(Id_table.name=="Doctor").update({Id_table.id: (a+1)},synchronize_session = False)
            
            dd=db.engine.execute("SELECT * FROM Doctor").fetchall()
            #for row in dd:
                #print(row)   
            return redirect(url_for('views.home1'))
    return render_template("doktor_kayit.html")

prescription_id_generator=0
@views.route('/recete_kayit', methods=['GET', 'POST'])
def recete_kayit():
    global prescription_id_generator
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
            flash("Doktor TC'si kayıtlı değil", category="error")               
        elif a2 is None:
            #print("Hasta TC'si kayıtlı değil")
            flash("Hasta TC'si kayıtlı değil", category="error")     
        elif (a3 is None) and ilac_id1!="":
            #print("İlaç 1 kayıtlı değil")
            flash("İlaç 1 kayıtlı değil", category="error")      
        elif (a4 is None) and ilac_id2!="":
            #print("İlaç 2 kayıtlı değil")
            flash("İlaç 2 kayıtlı değil", category="error") 
        elif (a5 is None) and ilac_id3!="":
            #print("İlaç 3 kayıtlı değil")
            flash("İlaç 3 kayıtlı değil", category="error") 
        elif (a6 is None) and ilac_id4!="":
            #print("İlaç 4 kayıtlı değil")
            flash("İlaç 4 kayıtlı değil", category="error") 
        elif (a7 is None) and ilac_id5!="":
            #print("İlaç 5 kayıtlı değil")
            flash("İlaç 5 kayıtlı değil", category="error")
        elif a8 is not None:
            #print("Recete kodu kullanilmis")
            flash("Recete kodu kullanilmis", category="error")  
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
            
            dd=db.engine.execute("SELECT * FROM Prescription").fetchall()
            #for row in dd:
                #print(row)
            dd=db.engine.execute("SELECT * FROM Prescription_content").fetchall()
            #for row in dd:
                #print(row)
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
            #print('Kullanılmamaş bir tc giriniz.')
            flash('Kullanılmamaş bir tc giriniz.', category='error') 
        elif a2:
            #print('Kullanılmamaş bir mail giriniz.')
            flash('Kullanılmamaş bir mail giriniz.', category='error')
        elif a3:
            #print('Kullanılmamaş bir telefon numarası giriniz.')
            flash('Kullanılmamaş bir telefon numarası giriniz.', category='error')
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

drug_number_generator=0
@views.route('/ilac_kayit', methods=['GET', 'POST'])
def ilac_kayit():
    global drug_number_generator
    if request.method == 'POST':
        drug_id=request.form.get('ilac')
        name=request.form.get('name')
        usage_content=request.form.get('aciklama')
        a1 = Drug.query.filter_by(drug_id=drug_id).first()
        a2 = Drug.query.filter_by(name=name).first()
        #print(drug_number_generator)
        if a1:
            #print('Kullanılmamaş bir ilaç numarası giriniz.')
            flash('Kullanılmamaş bir ilaç numarası giriniz.', category='error') 
        elif a2:
            #print('Kullanılmamaş bir ilaç adı giriniz.')
            flash('Kullanılmamaş bir ilaç adı giriniz.', category='error')
        else:
            new_drug= Drug(drug_id=drug_id,name=name,usage_content=usage_content)
            try:
                db.session.add(new_drug)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close_all()
            drug_number_generator+=1
            dd=db.engine.execute("SELECT * FROM Drug").fetchall()
            #for row in dd:
                #print(row)
            flash('İlaç kaydı başarılı.', category='Success')   
            return redirect(url_for('views.home1'))   
        
    return render_template("ilac_kayit.html")



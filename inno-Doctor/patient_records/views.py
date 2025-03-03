from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response

from django.shortcuts import redirect

from django.shortcuts import render

from .forms import (MedicationItemForm, PatientForm,
                    SocialHistoryForm, VitalSignForm,
                    ProblemListForm,
                    MedicationStatementFormSet,
                    )

from .models import (MedicationItem, Patient,
                     ProblemList,
                     VitalSign, SocialHistory, MedicationStatement, )

from django.contrib import messages


# Create your views here.
def eprescriptionList(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    medicationstatements = MedicationStatement.objects.filter(patient = patient)
    medicationitems = {}
    for medicationstatement in medicationstatements :
        medicationitem = MedicationItem.objects.filter(
            medication_statement = medicationstatement
            )
        if medicationitem is not None:
            medicationitems[medicationstatement.id] = medicationitem
    for a, b in medicationitems.items():
        print(a)
        for x in b:
            print(x.name)
    context = {"medicationitems": medicationitems, 'aadhaarId': id}
    return render(
        request, "patient_records/eprescription.html", context = context
        )

    # return redirect('/patient_records/patient-detail/{}'.format(id))


@login_required()
def patientDetails(request):
    if request.method == "POST":
        try:
            id = request.POST['aadhaarId']
            patient = get_object_or_404(Patient, aadhaarId = id)
            return render(
                request, "patient_records/patient-details.html",
                context = {'patient': patient}
                )
        except:
            messages.error(request, 'patient record not found')
    return redirect('/patient_records/patient-check')


@login_required()
def patientDetail(request, id):
    try:
        patient = get_object_or_404(Patient, aadhaarId = id)
        return render(
            request, "patient_records/patient-details.html",
            context = {'patient': patient}
            )
    except:
        messages.error(request, 'patient record found')

    return redirect('/patient_records/patient-check')


@login_required()
def patientCheck(request):
    patients = Patient.objects.all()
    return render(
        request, "patient_records/patient-check.html", {'patients': patients}
        )


@login_required()
def patientCreate(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        id = request.POST['aadhaarId']
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'New Patient is successfully added.!')
                model = form.instance
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(request, 'failed to add patient')
    else:
        form = PatientForm()
    return render(
        request, 'patient_records/patient-create.html', {'form': form}
        )


@login_required()
def patientUpdate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    form = PatientForm(
        initial = {'name': patient.name, 'aadhaarId': patient.aadhaarId,
                   'date_of_birth': patient.date_of_birth,
                   'gender': patient.gender}
        )
    if request.method == "POST":
        form = PatientForm(request.POST, instance = patient)
        if form.is_valid():
            try:
                form.save()
                # model = form.instance
                messages.success(request, 'patient updated!')
                return redirect('/patient_records/patient-check')
            except Exception as e:
                messages.error(request, 'update error!')
    return render(
        request, 'patient_records/patient-update.html', {'form': form}
        )


def PatientView(request):
    return render(request, "patient_records/patient_record_form.html")


def PatientList(request):
    aadhaarId = request.POST.get('aadharid')
    date_of_birth = request.POST.get('bdate')
    if (Patient.objects.filter(aadhaarId = aadhaarId).exists()) and (
    Patient.objects.filter(date_of_birth = date_of_birth).exists()):
        medication_id = MedicationStatement.objects.filter(
                patient_id = aadhaarId
        ).values_list('id', flat = True).order_by(
                '-timestamp'
        )[:1]
        medication_items = MedicationItem.objects.filter(
                medication_statement_id = medication_id
        )
        my_values = [item.dose_amount for item in medication_items]
        args = {'medication_items': medication_items}
        return render(request, "patient_records/patient_record_list.html", args)
    else:
        messages.error(request, 'Patient is not registered')
        # return render(request, "patient_records/patient_record_form.html")
        return redirect('/patient_records/patient_record_form')


@login_required()
def patientProblemListCreate(request, id):
    patient = Patient.objects.get(aadhaarId = id)

    if request.method == "POST":
        form = ProblemListForm(request.POST, initial = {'patient': patient})
        if form.is_valid():
            try:
                obj = form.save(commit = False)
                obj.patient = Patient.objects.get(aadhaarId = id)
                obj.save()
                messages.success(
                    request,
                    'New Problem is successfully added to the problem list!'
                    )
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(
                    request, 'Failed to add problem to the problem list'
                    )
    else:
        form = ProblemListForm(initial = {'patient': patient})
    return render(
        request, 'patient_records/patient-problem-list.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientSocialHistoryCreate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    try:
        social_history = SocialHistory.objects.get(patient = patient)
    except:
        social_history = None
    if social_history:
        messages.error(request, 'Social History record already exists')
        return redirect('/patient_records/patient-detail/{}'.format(id))
    if request.method == "POST":
        form = SocialHistoryForm(request.POST, initial = {'patient': patient})
        if form.is_valid():
            try:
                obj = form.save(commit = False)
                obj.patient = Patient.objects.get(aadhaarId = id)
                obj.save()
                messages.success(
                    request, 'New Social History is successfully added.!'
                    )
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(request, 'failed to add Social History list')
    else:
        form = SocialHistoryForm(initial = {'patient': patient})
    return render(
        request, 'patient_records/patient-social-history-list.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientVitalSignCreate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    try:
        vital_sign = VitalSign.objects.get(patient = patient)
    except:
        vital_sign = None
    if vital_sign:
        messages.error(request, 'Vital Signs records already exists')
        return redirect('/patient_records/patient-detail/{}'.format(id))
    if request.method == "POST":
        form = VitalSignForm(request.POST, initial = {'patient': patient})
        if form.is_valid():
            try:
                obj = form.save(commit = False)
                obj.patient = Patient.objects.get(aadhaarId = id)
                obj.save()
                messages.success(
                    request, 'New Vital Sign is successfully added.!'
                    )
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(request, 'failed to add vital sign')
    else:
        form = VitalSignForm(initial = {'patient': patient})
    return render(
        request, 'patient_records/patient-vital-sign.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientSocialHistoryUpdate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    socialhistory = SocialHistory.objects.get(patient = patient)
    form = SocialHistoryForm(
        initial = {'patient': patient,
                   'tobacco_smoking_status': 
                       socialhistory.tobacco_smoking_status,
                   'alcohol_consumption_status': socialhistory,
                   'alcohol_consumption_unit': 
                       socialhistory.alcohol_consumption_unit,
                   'alcohol_consumption_frequency': 
                       socialhistory.alcohol_consumption_frequency}
        )
    if request.method == "POST":
        form = SocialHistoryForm(request.POST, instance = socialhistory)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, 'New Social History is successfully Updated.!'
                    )
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(request, 'failed to Update Social History list')
    return render(
        request, 'patient_records/patient-social-history-list.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientVitalSignUpdate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    vitalsign = VitalSign.objects.get(patient = patient)
    form = VitalSignForm(
        initial = {'patient': patient, 'body_weight': vitalsign.body_weight,
                   'height': vitalsign.height,
                   'respiration_rate': vitalsign.respiration_rate,
                   'pulse_rate': vitalsign.pulse_rate,
                   'body_temperature': vitalsign.body_temperature,
                   'head_circumference': vitalsign.head_circumference,
                   'pulse_oximetry': vitalsign.pulse_oximetry,
                   'body_mass_index': vitalsign.body_mass_index,
                   'blood_pressure_systolic': vitalsign.blood_pressure_systolic,
                   'blood_pressure_diastolic': 
                       vitalsign.blood_pressure_diastolic}
        )
    if request.method == "POST":
        form = VitalSignForm(request.POST, instance = vitalsign)
        if form.is_valid():
            try:
                obj = form.save(commit = False)
                obj.patient = Patient.objects.get(aadhaarId = id)
                obj.save()
                messages.success(
                    request, 'New Vital Sign is successfully updated.!'
                    )
                # model = form.instance
                return redirect('/patient_records/patient-detail/{}'.format(id))
            except:
                messages.error(request, 'failed to update vital sign')

    return render(
        request, 'patient_records/patient-vital-sign.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def medicationStatementCreate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    medication_statement = MedicationStatement(patient = patient)
    formset = MedicationStatementFormSet(instance = medication_statement)

    if request.method == "POST":
        formset = MedicationStatementFormSet(
            request.POST, instance = medication_statement
            )
        if formset.is_valid():
            try:
                medication_statement.save()
                formset.save()
                messages.success(
                    request, 'New E-Prescription is successfully added.!'
                    )
            except:
                messages.error(request, 'Failed to create new E-Prescription')
            return redirect('/patient_records/patient-detail/{}'.format(id))

    return render(
        request, 'patient_records/patient-medication-item-1.html',
        {'formset': formset, 'patient': patient}
        )


@login_required()
def eprescriptionCreate(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    meditcation_statement = MedicationStatement.objects.filter(
        patient = patient
        )
    print("aaa", meditcation_statement)
    if request.method == "POST":
        form = MedicationItemForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, 'New epresciption  is successfully added.!'
                    )
            except:
                messages.error(request, 'failed to Add New E-prescription  ')
            return redirect('/patient_records/patient-detail/{}'.format(id))
    else:
        form = MedicationItemForm()
    return render(
        request, 'patient_records/genralForm.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientProblemListView(request, id):
    patient = Patient.objects.get(aadhaarId = id)
    forms = ProblemList.objects.filter(patient = patient)
    allforms = forms
    forms = []
    for form in allforms:
        if form:
            print(form)
            print(form.problem)
            forms.append(form)
    print(forms)
    return render(
        request, 'patient_records/patient-problem-list-view.html',
        {'problemLists': forms, 'patient': patient}
        )


@login_required()
def patientSocialHistoryView(request, id):
    try:
        patient = Patient.objects.get(aadhaarId = id)
        form = SocialHistory.objects.get(patient = patient)
    except:
        messages.error(request, "No Social History found ! ")
        return redirect(f'/patient_records/patient-social-history-create/{id}')
    return render(
        request, 'patient_records/patient-social-history-view.html',
        {'form': form, 'patient': patient}
        )


@login_required()
def patientVitalSignView(request, id):
    try:
        patient = Patient.objects.get(aadhaarId = id)
        form = get_object_or_404(VitalSign, patient = patient)
    except:
        messages.error(request, "No vital sign found ! ")
        return redirect(f'/patient_records/patient-detail/{id}')
    return render(
        request, 'patient_records/patient-vital-sign-view.html',
        {'form': form, 'patient': patient}
        )

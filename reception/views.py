from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
# from datetime import datetime, timedelta
from django.utils import timezone

from .models import *
from .forms import NameForm


WORK_START_TIME = timezone.datetime.strptime("09:00", "%H:%M").time()  # 09:00
WORK_END_TIME = timezone.datetime.strptime("18:00", "%H:%M").time()  # 18:00


def index(request):
    # get all doctors
    doctors = Doctor.get_all()
    # create template and set doctor list
    template = loader.get_template('reception/index.html')
    context = RequestContext(request, {
        'doctor_list': doctors,
    })

    return HttpResponse(template.render(context))


def error_response(request, msg):
    doctors = Doctor.get_all()
    return render(request, 'reception/index.html', {'error_message': msg, 'doctor_list': doctors})


def is_weekend(date):
    return date.weekday() in [5, 6]


def is_work_time(time):
    return WORK_START_TIME <= time < WORK_END_TIME


def submit(request):
    # create a form
    form = NameForm(request.POST)
    # checks for valid
    if not form.is_valid():
        return error_response(request, 'Введите данные')

    # find doctor by id
    try:
        doctor = Doctor.objects.get(pk=form.cleaned_data['doctor_list'])
    except (KeyError, Doctor.DoesNotExist):
        return error_response(request, 'Врач не найден')

    accept_day = form.cleaned_data['accept_day']
    accept_time = form.cleaned_data['accept_time']
    accept_datetime = timezone.datetime.combine(accept_day, accept_time)

    # checking for weekend and work time
    if is_weekend(accept_day) or not is_work_time(accept_time):
        return error_response(request, 'нерабочая время!')

    # checking for current date and time
    if timezone.now().date() != accept_day or accept_time < timezone.now().time():
        return error_response(request, 'укажите правильную дату и время')

    # checking for enough time
    if (accept_datetime + timezone.timedelta(hours=1)).time() > WORK_END_TIME:
        return error_response(request, 'Время не хватит для приема!')

    # find a doctor and checks for free.
    try:
        record = Record.objects.filter(doctor_id=doctor.pk).filter(
            accept_time__year=timezone.now().year,
            accept_time__month=timezone.now().month,
            accept_time__day=timezone.now().day,
        ).order_by('-accept_time')[:1].get()

        is_free = accept_time > record.finish_time.time()

    except Record.DoesNotExist:
        is_free = True

    if not is_free:
        return error_response(request, 'Врач занят.')

    # register patient
    patient = Patient(first_name=form.cleaned_data['firstname'],
                      last_name=form.cleaned_data['lastname'],
                      patronymic=form.cleaned_data['patronymic'])
    patient.save()

    # register new record
    doctor.record_set.create(accept_time=accept_datetime, patient=patient)
    doctor.save()

    return render(request, 'reception/index.html', {'success_message': 'Успешно', 'doctor_list': Doctor.get_all()})
from django import forms


class NameForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    patronymic = forms.CharField(max_length=100)
    accept_day = forms.DateField()
    accept_time = forms.TimeField()
    doctor_list = forms.IntegerField()
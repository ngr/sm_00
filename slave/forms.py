from django import forms


class AssignToTaskForm(forms.Form):
    slave = forms.CharField(label='Slave id', max_length=11)
    task  = forms.CharField(label='Task id', max_length=11)


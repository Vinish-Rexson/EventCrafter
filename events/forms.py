from django import forms
from betterforms.multiform import MultiModelForm

from .models import Event, EventImage, EventAgenda


class EventForm(forms.ModelForm):


    class Meta:
        model = Event
        fields = ['category', 'name', 'user', 'description', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EventImageForm(forms.ModelForm):


    class Meta:
        model = EventImage
        fields = ['image']



class EventAgendaForm(forms.ModelForm):


    class Meta:
        model = EventAgenda
        fields = ['speaker_name', 'start_time', 'end_time', 'venue_name']

        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class EventCreateMultiForm(MultiModelForm):
    form_classes = {
        'event': EventForm,
        'event_image': EventImageForm,
        'event_agenda': EventAgendaForm,
    }

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'assigned_person', 'start_datetime', 'end_datetime', 'completed']

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from dotenv import load_dotenv

import qrcode
import os
import pandas as pd
import matplotlib.pyplot as plt

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from twilio.rest import Client
import google.generativeai as genai

from django.contrib.auth.models import User
from django import forms

from .models import *
from .forms import *


# Event Category List View
class EventCategoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventCategory
    template_name = 'events/event_category.html'
    context_object_name = 'event_categories'

    def get_queryset(self):
        return EventCategory.objects.filter(created_user=self.request.user)


# Event Category Create View
class EventCategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'status']
    template_name = 'events/create_event_category.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


# Event Category Update View
class EventCategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'code', 'status']
    template_name = 'events/edit_event_category.html'


# Event Category Delete View
class EventCategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventCategory
    template_name = 'events/event_category_delete.html'
    success_url = reverse_lazy('event-category-list')


# QR Code Generation for Event Category
def generate_qr_code(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    url = request.build_absolute_uri(f'/join/{category.code}/')
    qr = qrcode.make(url)
    response = HttpResponse(content_type='image/png')
    qr.save(response, 'PNG')
    return response


# Join Event Category View
@login_required
def your_join_view(request, code):
    category = get_object_or_404(EventCategory, code=code)
    user = request.user

    # Check if the user is already part of this category
    try:
        category_user = EventCategoryUser.objects.get(user=user, category=category)
        return HttpResponse('You are already part of this category.', content_type='text/plain')
    except EventCategoryUser.DoesNotExist:
        pass  # User is not part of the category yet

    # Handle POST request to join the category
    if request.method == 'POST':
        EventCategoryUser.objects.create(user=user, category=category, approved=True)  # Auto-approve
        return HttpResponse('You have successfully joined the category!', content_type='text/plain')

    context = {'category': category}
    return render(request, 'join_category.html', context)
  # Adjust the template as needed


@login_required(login_url='login')
def create_event(request):
    event_form = EventForm()
    event_image_form = EventImageForm()
    event_agenda_form = EventAgendaForm()
    catg = EventCategory.objects.all()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_image_form = EventImageForm(request.POST, request.FILES)
        event_agenda_form = EventAgendaForm(request.POST)
        if event_form.is_valid() and event_image_form.is_valid() and event_agenda_form.is_valid():
            ef = event_form.save()
            created_updated(Event, request)
            event_image_form.save(commit=False)
            event_image_form.event_form = ef
            event_image_form.save() 
            
            event_agenda_form.save(commit=False)
            event_agenda_form.event_form = ef
            event_agenda_form.save()
            return redirect('event-list')
    context = {
        'form': event_form,
        'form_1': event_image_form,
        'form_2': event_agenda_form,
        'ctg': catg
    }
    return render(request, 'events/create.html', context)

# Event Views
class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = EventCreateMultiForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        evt = form['event'].save()
        event_image = form['event_image'].save(commit=False)
        event_image.event = evt
        event_image.save()

        event_agenda = form['event_agenda'].save(commit=False)
        event_agenda.event = evt
        event_agenda.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctg'] = EventCategory.objects.all()
        return context


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add any additional context variables here
        return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['category', 'name', 'uid', 'description', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
    template_name = 'events/edit_event.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('event-list')


class AddEventMemberCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventMember
    fields = ['event', 'user', 'email', 'college']
    template_name = 'events/add_event_member.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class JoinEventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/joinevent_list.html'
    context_object_name = 'eventmember'


class RemoveEventMemberDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/remove_event_member.html'
    success_url = reverse_lazy('join-event-list')




class UpdateEventStatusView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['status']
    template_name = 'events/update_event_status.html'


class CompleteEventList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/complete_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(status='completed')




class CreateUserMark(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = UserCoin
    fields = ['user', 'event', 'status']
    template_name = 'events/create_user_mark.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class UserMarkList(ListView):
    # login_url = 'login'
    model = UserCoin
    template_name = 'events/user_mark_list.html'
    context_object_name = 'usermark'


@login_required(login_url='login')
def search_event_category(request):
    if request.method == 'POST':
       data = request.POST['search']
       event_category = EventCategory.objects.filter(name__icontains=data)
       context = {
           'event_category': event_category
       }
       return render(request, 'events/event_category.html', context)
    return render(request, 'events/event_category.html')


def search_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       events = Event.objects.filter(name__icontains=data)
       context = {
           'events': events
       }
       return render(request, 'events/event_list.html', context)
    return render(request, 'events/event_list.html')


def event_catogery(request):
    return render(request, 'event_catogery.html')


def events_dashboard(request):
    return render(request, 'events_dashboard.html')


@login_required
def join_event_category(request, code):
    # Get the category by its code
    category = get_object_or_404(EventCategory, code=code)
    
    # Check if the user has already joined
    if EventCategoryUser.objects.filter(user=request.user, category=category).exists():
        # Redirect if already joined or show a message
        return redirect('event-category-list')  # or some message that user is already part of this category

    # Create an EventCategoryUser to store the user and category
    EventCategoryUser.objects.create(user=request.user, category=category, approved=True)  # You can change approved to False for admin approval

    return redirect('event-category-list')  # Redirect after joining


# Google Gemini API Integration
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def gemini(request):
    response_text = ""
    if request.method == "POST":
        event_name = request.POST.get("event_name", "")
        event_date = request.POST.get("event_date", "")
        event_location = request.POST.get("event_location", "")
        event_budget = request.POST.get("event_budget", "")
        special_requirements = request.POST.get("special_requirements", "")

        user_input = f"Plan an event with the following details:\nName: {event_name}\nDate: {event_date}\nLocation: {event_location}\nBudget: {event_budget}\nSpecial Requirements: {special_requirements} Be detailed"
        
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        response_text = response.text

    context = {'response': response_text}
    return render(request, 'gemini.html', context)


def group_discussion(request):
    return render(request, 'group_discussion.html')


# Email Invitations Upload and Sending
def upload_invitation(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        invitation_file = request.FILES.get('invitation_file')
        email_subject = request.POST.get('email_subject')
        email_body_template = request.POST.get('email_body')

        if not excel_file or not invitation_file or not email_subject or not email_body_template:
            return HttpResponse("Please upload all required fields and provide email content.")

        fs = FileSystemStorage()
        excel_path = fs.save(excel_file.name, excel_file)
        invitation_path = fs.save(invitation_file.name, invitation_file)

        try:
            df = pd.read_excel(
                os.path.join(settings.MEDIA_ROOT, excel_path),
                sheet_name="Guests",
                na_values="",
                parse_dates=["Invitation Date"]
            )
        except Exception as e:
            return HttpResponse(f"Error reading Excel file: {e}")

        for _, row in df.iterrows():
            try:
                guest_name = row['Guest Name']
                guest_email = row['Guest Email ID']
                invitation_date = row['Invitation Date'].strftime('%d-%m-%Y')
                venue = row['Venue']
                time = row['Time']

                email_body = email_body_template.format(
                    guest_name=guest_name,
                    invitation_date=invitation_date,
                    venue=venue,
                    time=time
                )

                html_body = f"""
                <html>
                <body>
                    <p>{email_body}</p>
                    <table style="border: 1px solid #ddd; padding: 8px; border-collapse: collapse;">
                        <tr><td style="padding: 8px;"><strong>Date:</strong></td><td style="padding: 8px;">{invitation_date}</td></tr>
                        <tr><td style="padding: 8px;"><strong>Time:</strong></td><td style="padding: 8px;">{time}</td></tr>
                        <tr><td style="padding: 8px;"><strong>Venue:</strong></td><td style="padding: 8px;">{venue}</td></tr>
                    </table>
                    <br><p>Best Regards,<br><strong>The Event Team</strong></p>
                </body>
                </html>
                """

                email = EmailMessage(
                    email_subject,
                    html_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [guest_email],
                )
                email.content_subtype = 'html'
                email.attach_file(os.path.join(settings.MEDIA_ROOT, invitation_path))
                email.send()
                print(f"Invitation sent to {guest_email}")
            except Exception as e:
                print(f"Failed to send email to {guest_email}: {e}")

        return HttpResponse("Invitations sent successfully!")
    
    return render(request, 'upload_invitation.html')


# Excel Template Download
def download_excel_template(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'standard_invitation.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='standard_invitation.xlsx')


# Define your scopes and service account file
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'drive.json'
PARENT_FOLDER_ID = "1-znjTCTeW_Us22GqyvYMlys0AbDi-BMR"


# Function to authenticate user (service account for simplicity)
def authenticate_user():
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


# Function to create a new folder on Google Drive
def create_folder(folder_name, parent_folder_id=PARENT_FOLDER_ID):
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id] if parent_folder_id else None
    }

    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
        return folder.get('id')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


# Fetch folders from Google Drive
def list_folders():
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    folders = results.get('files', [])
    return folders


# Upload a photo to the selected folder
def upload_photo_to_drive(file_path, file_name, folder_id):
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype='image/png')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')


# View to handle both folder creation and file upload
def upload_photo(request):
    folders = list_folders()

    if request.method == 'POST':
        if 'create_folder' in request.POST:
            folder_name = request.POST['folder_name']
            create_folder(folder_name)
            return redirect('upload_photo')

        elif 'upload_file' in request.POST:
            selected_folder = request.POST['folder_id']
            uploaded_files = request.FILES.getlist('file')

            for uploaded_file in uploaded_files:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)

                drive_file_id = upload_photo_to_drive(file_path, uploaded_file.name, selected_folder)

                os.remove(file_path)

            return redirect('upload_photo')

    return render(request, 'upload_photo.html', {'folders': folders})


# Functionality to list files in a specific folder
def view_folder_contents(request, folder_id):
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])
    return render(request, 'folder_contents.html', {'files': files, 'folder_id': folder_id})


# Task-related views
def task_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tasks = event.tasks.all()
    return render(request, 'task_list.html', {'event': event, 'tasks': tasks})


def create_task(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            return redirect('event-tasks', event_id=event.id)
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form, 'event': event})


def update_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
        return redirect('event-tasks', event_id=task.event.id)

def task_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request,'tasks_view.html')
def task_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request,'tasks_view.html')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})
@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        completed = request.POST.get('completed') == 'on'
        task.completed = completed
        task.save()

        if completed:
            account_sid = os.environ["account_sid"]
            auth_token = os.environ["auth_token"]
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to='+919137796495',
                from_='+18577676358',
                body=f'Task "{task.task_name}" has been marked as completed.'
            )
            print(f"Message SID: {message.sid}")

        return redirect('event-list')

    return HttpResponse("Task not updated")


def event_tasks(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tasks = event.tasks.all()  # Access tasks using the related name 'tasks'
    return render(request, 'task_list.html', {'event': event, 'tasks': tasks})


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'assigned_person', 'start_datetime', 'end_datetime']

    assigned_person = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Assign to User"
    )


def update_task_view(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.completed = 'completed' in request.POST
        task.save()

        if task.completed:
            account_sid = 'account_sid'
            auth_token = 'auth_token'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to= '+919137796495',
                from_='+18577676358',
                body=f'MEDSAFE\nDear {task.assigned_person.name}, Your task "{task.task_name}" has been marked as completed!',
            )
            print(message.sid)

    return redirect('event-tasks', event_id=task.event.id)




# Graph generation
def generate_task_graphs(task_counts):
    plt.figure(figsize=(10, 6))
    plt.bar(task_counts.index, task_counts.values, color=['skyblue', 'lightcoral'])
    plt.title('Task Completion Status')
    plt.xlabel('Status')
    plt.ylabel('Number of Tasks')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join('static', 'images', 'task_completion_bar_chart.png'))
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.pie(task_counts, labels=task_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Task Completion Distribution')
    plt.axis('equal')
    plt.savefig(os.path.join('static', 'images', 'task_completion_pie_chart.png'))
    plt.close()


def task_progress_view(request):
    event_names = ['Event A', 'Event B', 'Event C', 'Event D']
    registrations = [15, 30, 45, 25]
    attendance_over_time = [10, 20, 35, 40, 50]
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']

    context = {
        'event_names': event_names,
        'registrations': registrations,
        'attendance_over_time': attendance_over_time,
        'days': days,
    }
    return render(request, 'task_progress.html', context)


# Miscellaneous views
def budget(request):
    return render(request, 'budget.html')


def progress(request):
    return redirect('/events/tasks/progress/')


def vendor(request):
    return render(request, 'vendor.html')


def download_quote(request):
    pdf_path = os.path.join('media', 'event_quote.pdf')
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf', as_attachment=True, filename='event_quote.pdf')

from django.db import models
from django.urls import reverse
from mapbox_location_field.models import LocationField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string


from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, unique=True, blank=True)  # Auto-generated numeric code
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_event_categories')
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_event_categories')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    status_choice = (
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-category-list')

    def save(self, *args, **kwargs):
        if not self.pk:  # Generate code only on creation
            self.code = self.generate_unique_code()
        super(EventCategory, self).save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = get_random_string(length=6, allowed_chars='0123456789')
            if not EventCategory.objects.filter(code=code).exists():
                return code

    def generate_join_link(self):
        """Generate a unique shareable join link"""
        return reverse('event-category-join', kwargs={'code': self.code})


class EventCategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_categories')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='approved_users')
    approved = models.BooleanField(default=False)  # Admin can approve later or auto-approve

    def __str__(self):
        return f'{self.user.username} in {self.category.name}'


class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = RichTextUploadingField()

    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = LocationField()
    points = models.PositiveIntegerField()
    maximum_attende = models.PositiveIntegerField()
    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='event_created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='event_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('event-list')
    
    def created_updated(model, request):
        obj = model.objects.latest('pk')
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

class EventImage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')


class EventAgenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker_name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_name = models.CharField(max_length=255)


class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=100, null=True)
    college = models.CharField(max_length=500, null=True)
    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='eventmember_created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='eventmember_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)



    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('join-event-list')




class UserCoin(models.Model):
    user = models.CharField(max_length=255, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='usercoin_created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='usercoin_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('Winner', 'Winner'),
        ('1st Runner up', '1st Runner Up'),
        ('2nd Runnerup', '2nd Runner Up'),
    )
    status = models.CharField(choices=status_choice, max_length=20)

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('user-mark')




class Task(models.Model):
    event = models.ForeignKey(Event, related_name='tasks', on_delete=models.CASCADE)  # Link to the Event model
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_person = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name






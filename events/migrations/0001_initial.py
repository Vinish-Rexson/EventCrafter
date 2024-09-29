# Generated by Django 5.1.1 on 2024-09-27 21:02

import ckeditor_uploader.fields
import django.db.models.deletion
import mapbox_location_field.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('venue', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', mapbox_location_field.models.LocationField(map_attrs={})),
                ('points', models.PositiveIntegerField()),
                ('maximum_attende', models.PositiveIntegerField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('completed', 'Completed'), ('cancel', 'Cancel')], max_length=10)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_updated_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speaker_name', models.CharField(max_length=120)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('venue_name', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(blank=True, max_length=6, unique=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('deleted', 'Deleted'), ('completed', 'Completed')], max_length=10)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_event_categories', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_event_categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcategory'),
        ),
        migrations.CreateModel(
            name='EventCategoryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_users', to='events.eventcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined_categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='event_image/')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='UserCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Winner', 'Winner'), ('1st Runner up', '1st Runner Up'), ('2nd Runnerup', '2nd Runner Up')], max_length=20)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercoin_created_user', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercoin_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('college', models.CharField(max_length=500, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventmember_created_user', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventmember_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('event', 'user')},
            },
        ),
    ]

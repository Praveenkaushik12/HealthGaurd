# Generated by Django 5.0 on 2024-05-03 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_request_patient_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='hospital_affiliation',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='doctor',
            name='years_of_experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]

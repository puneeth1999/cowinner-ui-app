# Generated by Django 3.2.3 on 2021-06-02 16:18

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True)),
            ],
        ),
    ]
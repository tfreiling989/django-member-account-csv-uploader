# Generated by Django 4.0.4 on 2022-05-30 18:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MemberAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=25)),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9999999999'. Exactly 10 digits are required.", regex='^\\d{10}$')])),
                ('client_member_id', models.CharField(max_length=7)),
                ('account_id', models.CharField(max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='memberaccount',
            constraint=models.UniqueConstraint(fields=('client_member_id', 'account_id'), name='unique client_member per account'),
        ),
        migrations.AddConstraint(
            model_name='memberaccount',
            constraint=models.UniqueConstraint(fields=('phone_number', 'account_id'), name='unique phone_number per account'),
        ),
    ]

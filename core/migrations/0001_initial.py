# Generated by Django 4.2.5 on 2023-09-08 07:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_emp_id', message='Employee ID must be Alphanumeric', regex='/^PSI-\\d{4}$/')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='KBDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('tools', models.CharField(choices=[('pyats', 'pyATS'), ('xpresso', 'Xpresso'), ('earms', 'Earms'), ('trade', 'Trade'), ('laas', 'LaaS'), ('adsrsvp', 'ADSRSVP'), ('ssr', 'SSR')], default='pyats', max_length=100)),
                ('reporter', models.CharField(max_length=255)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('closed_datetime', models.DateTimeField()),
                ('source_of_ticket', models.CharField(choices=[('sts', 'STS'), ('piestack', 'Piestack'), ('github', 'Github'), ('webex', 'Webex'), ('mall', 'Mall')], default='sts', max_length=100)),
                ('ticket_link', models.CharField(max_length=255)),
                ('issue_type', models.CharField(max_length=100)),
                ('issue_title', models.TextField()),
                ('issue_description', models.TextField()),
                ('category', models.CharField(choices=[('configmiss', 'Config Miss'), ('sysadmin', 'Sys Admin'), ('bugfix', 'Bug Fix'), ('enhancement', 'Enhancement'), ('monitoring', 'Monitoring'), ('testingonly', 'Testing Only'), ('documentation', 'Documentation')], default='sysadmin', max_length=100)),
                ('help_links', models.TextField(blank=True, null=True)),
                ('resolutions', models.TextField()),
                ('workaround', models.TextField()),
                ('others', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('udpated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kbdocs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'KB Docs',
                'verbose_name_plural': 'KB Docs',
            },
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-24 20:59

from ..constants import *
from antares.apps.core.constants import *
import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.user.models.user.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.user.models.user.id')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.user.table_name',
                'verbose_name_plural': 'antares.apps.user.models.user.table_name_plural',
                'db_table': 'user_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('application_name', models.CharField(max_length=200)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('route', models.CharField(blank=True, max_length=300, null=True)),
                ('scope', enumfields.fields.EnumField(default='Self', enum=ApplicationScopeType, max_length=30)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='user_application_author_set', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.Application')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
                'db_table': 'user_application',
            },
        ),
        migrations.CreateModel(
            name='ApplicationParameter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.user.models.application_parameter.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.user.models.application_parameter.id')),
                ('parameter_name', models.CharField(help_text='antares.apps.user.models.application_parameter.parameter_name_help', max_length=255, verbose_name='antares.apps.user.models.application_parameter.parameter_name')),
                ('value', models.CharField(help_text='antares.apps.user.models.application_parameter.value_help', max_length=200, verbose_name='antares.apps.user.models.application_parameter.value_type')),
                ('is_route_parameter', models.BooleanField(default=False, help_text='antares.apps.user.models.application_parameter.is_route_parameter_help', verbose_name='antares.apps.user.models.application_parameter.is_route_parameter')),
                ('is_named_route_parameter', models.BooleanField(default=False, help_text='antares.apps.user.models.application_parameter.is_named_route_parameter_help', verbose_name='antares.apps.user.models.application_parameter.is_named_route_parameter')),
                ('application', models.ForeignKey(db_column='action_definition', help_text='antares.apps.user.models.application_parameter.action_definition_help', on_delete=django.db.models.deletion.PROTECT, related_name='parameter_set', to='user.Application', verbose_name='antares.apps.user.models.application_parameter.action_definition')),
            ],
            options={
                'verbose_name': 'Application Parameter',
                'verbose_name_plural': 'Application Parameters',
                'db_table': 'user_application_parameter',
            },
        ),
        migrations.CreateModel(
            name='OrgUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='org_unit_author_set', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.OrgUnit')),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.org_unit.table_name',
                'verbose_name_plural': 'antares.apps.user.models.org_unit.table_name_plural',
                'db_table': 'user_org_unit',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='role_author_set', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.Role')),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.role.table_name',
                'verbose_name_plural': 'antares.apps.user.models.role.table_name_plural',
                'db_table': 'user_role',
            },
        ),
        migrations.CreateModel(
            name='RoleApplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('update_date', models.DateTimeField(editable=False)),
                ('application', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='role_set', to='user.Application')),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='role_application_author_set', to=settings.AUTH_USER_MODEL)),
                ('role', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='application_set', to='user.Role')),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.role_application.table_name',
                'verbose_name_plural': 'antares.apps.user.models.role_application.table_name_plural',
                'db_table': 'user_role_application',
            },
        ),
        migrations.CreateModel(
            name='UserOrgUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('update_date', models.DateTimeField(editable=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='user_org_unit_author_set', to=settings.AUTH_USER_MODEL)),
                ('org_unit', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_set', to='user.OrgUnit')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='org_unit_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.user_org_unit.table_name',
                'verbose_name_plural': 'antares.apps.user.models.user_org_unit.table_name_plural',
                'db_table': 'user_user_org_unit',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('update_date', models.DateTimeField(editable=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='user_role_author_set', to=settings.AUTH_USER_MODEL)),
                ('role', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_set', to='user.Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='role_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'antares.apps.user.models.user_role.table_name',
                'verbose_name_plural': 'antares.apps.user.models.user_role.table_name_plural',
                'db_table': 'user_user_role',
            },
        ),
    ]

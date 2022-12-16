# Generated by Django 4.1.4 on 2022-12-16 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangelogInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GenreEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GroupEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NamedRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_lead', models.BooleanField(null=True)),
                ('is_otoko', models.BooleanField(null=True)),
                ('is_in_Japanese', models.BooleanField()),
                ('character_name', models.CharField(max_length=255, null=True)),
                ('character_name_reading', models.CharField(max_length=255, null=True)),
                ('character_subtitle', models.TextField(null=True)),
                ('parent_character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='theater_info.namedrole')),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('production_blurb', models.TextField()),
                ('associated_groups', models.ManyToManyField(to='theater_info.groupenum')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileTextEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RoleEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
                ('is_onstage_role', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(null=True)),
                ('birth_country', models.CharField(blank=True, default='日本国', max_length=255)),
                ('birth_prefecture', models.CharField(blank=True, max_length=255)),
                ('birth_city', models.CharField(blank=True, max_length=255)),
                ('given_name', models.CharField(blank=True, max_length=255)),
                ('given_name_reading', models.CharField(blank=True, max_length=255)),
                ('given_name_romaji', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TriggerEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='VenueEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reading', models.CharField(max_length=255)),
                ('romaji', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WorkCategoryEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTextEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_in_Japanese', models.BooleanField()),
                ('text', models.TextField()),
                ('text_enum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.worktextenum')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.work')),
            ],
        ),
        migrations.CreateModel(
            name='WorkScene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('is_in_Japanese', models.BooleanField()),
                ('associated_roles', models.ManyToManyField(to='theater_info.namedrole')),
                ('associated_work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.work')),
                ('parent_scene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='theater_info.workscene')),
            ],
        ),
        migrations.AddField(
            model_name='work',
            name='enum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.workcategoryenum'),
        ),
        migrations.AddField(
            model_name='work',
            name='genre',
            field=models.ManyToManyField(to='theater_info.genreenum'),
        ),
        migrations.AddField(
            model_name='work',
            name='parent_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='theater_info.work'),
        ),
        migrations.AddField(
            model_name='work',
            name='trigger_warnings',
            field=models.ManyToManyField(to='theater_info.triggerenum'),
        ),
        migrations.CreateModel(
            name='StageName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reading', models.CharField(max_length=255)),
                ('romaji', models.CharField(max_length=255)),
                ('suffix', models.CharField(blank=True, max_length=10)),
                ('associated_staff_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='theater_info.staffmember')),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfileTextFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_text', models.CharField(max_length=255)),
                ('is_official_Hankyu_source', models.BooleanField()),
                ('associated_staff_member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.staffmember')),
                ('profile_text_enum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.profiletextenum')),
            ],
        ),
        migrations.AddField(
            model_name='staffmember',
            name='canonical_stage_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='theater_info.stagename'),
        ),
        migrations.CreateModel(
            name='ProductionRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('production', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.production')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.venueenum')),
            ],
        ),
        migrations.AddField(
            model_name='production',
            name='works',
            field=models.ManyToManyField(to='theater_info.work'),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(null=True)),
                ('date_end', models.DateField(null=True)),
                ('tour_venue', models.CharField(blank=True, max_length=255, null=True)),
                ('associated_production_run', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.productionrun')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.work')),
            ],
        ),
        migrations.AddField(
            model_name='namedrole',
            name='role_enum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.roleenum'),
        ),
        migrations.AddField(
            model_name='namedrole',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.work'),
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(null=True)),
                ('gender_role', models.CharField(choices=[('OY', 'otokoyaku'), ('MY', 'musumeyaku'), ('BT', 'both'), ('NA', 'not applicable')], default='NA', max_length=2)),
                ('associated_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.groupenum')),
                ('date_end_performance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group_depart', to='theater_info.performance')),
                ('date_start_performance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='group_join', to='theater_info.performance')),
                ('stage_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.stagename')),
            ],
        ),
        migrations.CreateModel(
            name='CastMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.performance')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.namedrole')),
                ('stage_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theater_info.stagename')),
            ],
        ),
        migrations.AddConstraint(
            model_name='stagename',
            constraint=models.UniqueConstraint(fields=('romaji', 'suffix'), name='Combination of romaji reading and suffix should be unique as it will be used as a URL slug.'),
        ),
    ]

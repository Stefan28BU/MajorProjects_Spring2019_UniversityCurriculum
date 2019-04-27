# Generated by Django 2.2 on 2019-04-27 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Curriculum', '0002_auto_20190427_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Description', models.CharField(max_length=255)),
                ('Cur_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Curriculum')),
                ('Grade_Dist_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Grade')),
            ],
            options={
                'db_table': 'Goal',
            },
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('Section_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Year', models.PositiveIntegerField(default=0)),
                ('Semester', models.CharField(max_length=255)),
                ('Enrollment', models.CharField(max_length=255)),
                ('Comment1', models.CharField(max_length=255)),
                ('Comment2', models.CharField(max_length=255)),
                ('Course_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Course')),
                ('Grade_Distribution_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Grade')),
            ],
            options={
                'db_table': 'CourseSection',
            },
        ),
        migrations.CreateModel(
            name='CourseGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Course')),
                ('Goal_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Goal')),
            ],
            options={
                'db_table': 'CourseGoal',
            },
        ),
        migrations.AddConstraint(
            model_name='coursesection',
            constraint=models.UniqueConstraint(fields=('Section_ID', 'Course_Name', 'Year', 'Semester'), name='courseSection_unique'),
        ),
        migrations.AddConstraint(
            model_name='coursegoal',
            constraint=models.UniqueConstraint(fields=('Goal_ID', 'Course_Name'), name='courseGoal_unique'),
        ),
    ]

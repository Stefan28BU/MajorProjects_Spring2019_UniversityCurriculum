# Generated by Django 2.2 on 2019-05-06 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Curriculum', '0004_grade_dist_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursetopics',
            name='Units',
        ),
        migrations.CreateModel(
            name='CurriculumCT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Units', models.PositiveIntegerField(default=0)),
                ('Associated_CT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.CourseTopics')),
                ('Associated_Curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curriculum.Curriculum')),
            ],
            options={
                'db_table': 'CurriculumCT',
            },
        ),
        migrations.AddConstraint(
            model_name='curriculumct',
            constraint=models.UniqueConstraint(fields=('Associated_Curriculum', 'Associated_CT'), name='CCT_Unique'),
        ),
    ]

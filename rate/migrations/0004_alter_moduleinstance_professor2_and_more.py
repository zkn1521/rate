# Generated by Django 4.0.3 on 2022-03-28 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0003_alter_moduleinstance_professor2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleinstance',
            name='Professor2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PROFESSOR_2', to='rate.professor', unique=True),
        ),
        migrations.AlterField(
            model_name='moduleinstance',
            name='Professor3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PROFESSOR_3', to='rate.professor', unique=True),
        ),
        migrations.AlterField(
            model_name='moduleinstance',
            name='Professor4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PROFESSOR_4', to='rate.professor', unique=True),
        ),
        migrations.AlterField(
            model_name='moduleinstance',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rate.professor', unique=True),
        ),
    ]

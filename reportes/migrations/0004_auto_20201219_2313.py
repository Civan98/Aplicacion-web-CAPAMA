# Generated by Django 3.0.2 on 2020-12-20 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0003_auto_20201210_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportesempleado',
            name='fecha_fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reportesempleado',
            name='fecha_inicio',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reportesusuario',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]

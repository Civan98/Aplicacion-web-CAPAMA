# Generated by Django 3.0.2 on 2021-01-02 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0004_auto_20201219_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportesempleado',
            old_name='id_repoteUsuario',
            new_name='id_repoteusuario',
        ),
    ]
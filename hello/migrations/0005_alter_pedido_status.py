# Generated by Django 4.2.11 on 2024-05-16 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_alter_itemnf_data_importacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('SOLICITADO', 'SOLICITADO'), ('RECEBIDO', 'RECEBIDO'), ('CANCELADO', 'CANCELADO')], max_length=20),
        ),
    ]

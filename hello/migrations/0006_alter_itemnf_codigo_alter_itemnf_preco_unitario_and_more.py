# Generated by Django 4.2.11 on 2024-05-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_alter_pedido_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemnf',
            name='codigo',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='itemnf',
            name='preco_unitario',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='itemnf',
            name='quantidade',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='itemnf',
            name='valor_total',
            field=models.CharField(max_length=32),
        ),
    ]

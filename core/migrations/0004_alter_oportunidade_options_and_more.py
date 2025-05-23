# Generated by Django 5.2 on 2025-05-06 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_oportunidade_foto_certificado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oportunidade',
            options={'ordering': ['-data'], 'verbose_name': 'Oportunidade', 'verbose_name_plural': 'Oportunidades'},
        ),
        migrations.RenameField(
            model_name='oportunidade',
            old_name='data_cadastro',
            new_name='criado_em',
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='oportunidades/'),
        ),
        migrations.AlterField(
            model_name='oportunidade',
            name='data',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='oportunidade',
            name='local',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='oportunidade',
            name='quantidade_vagas',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='oportunidade',
            name='titulo',
            field=models.CharField(max_length=200),
        ),
    ]

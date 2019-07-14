# Generated by Django 2.2.3 on 2019-07-11 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comission_plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_percentage', models.DecimalField(decimal_places=2, max_digits=3)),
                ('upper_percentage', models.DecimalField(decimal_places=2, max_digits=3)),
                ('min_value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Sellers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.IntegerField(max_length=11)),
                ('age', models.IntegerField()),
                ('email', models.CharField(max_length=100)),
                ('cpf', models.IntegerField(max_length=11)),
                ('comission_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Comission_plan')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('paid_comission', models.DecimalField(decimal_places=2, max_digits=20)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Sellers')),
            ],
        ),
        migrations.CreateModel(
            name='Check_comission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Sales')),
            ],
        ),
    ]
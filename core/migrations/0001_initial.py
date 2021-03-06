# Generated by Django 3.1 on 2020-09-30 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('home', models.CharField(max_length=50)),
                ('flat', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BaseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('base_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.basestatus')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('base_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.baseproduct')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.address')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.paymentmethod')),
                ('products', models.ManyToManyField(to='core.OrderedProduct')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rate', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('images', models.ManyToManyField(to='core.Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.category'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='images',
            field=models.ManyToManyField(to='core.Image'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.manufacturer'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.material'),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.address')),
                ('description', models.TextField()),
                ('images', models.ManyToManyField(to='core.Image')),
            ],
            bases=('core.address',),
        ),
    ]

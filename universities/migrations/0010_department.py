# Generated manually for Department model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0009_university_course_type_university_institution_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='universities.university')),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(fields=('university', 'name'), name='unique_department_name_per_university'),
        ),
    ]

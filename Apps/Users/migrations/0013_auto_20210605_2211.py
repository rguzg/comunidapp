import Apps.Users.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_auto_20201207_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='alumno',
            field=models.BooleanField(default=False, verbose_name='Es alumno'),
        ),
        migrations.AddField(
            model_name='user',
            name='alumno',
            field=models.BooleanField(default=False, verbose_name='Es alumno'),
        ),
    ]
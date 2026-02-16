from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("abi", "0003_alter_project_creator"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

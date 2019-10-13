
from django.db import migrations

def create_person_deleted_update_face_model_queue(apps, schema_editor):
    Queue = apps.get_model("message_queue", "Queue")
    queue = Queue(name = "person_deleted_update_face_model",
                    description = """
                    Queue for person ids that have been deleted
                    These need to be removed from Facial Recognition models
                    """)
    queue.save()

class Migration(migrations.Migration):

    dependencies = [
        ('message_queue', '0002_auto_20191012_1035'),
    ]

    operations = [
        migrations.RunPython(create_person_deleted_update_face_model_queue),
    ]

# Generated by Django 4.0.5 on 2022-06-15 07:22

from django.db import migrations

taggableFields = [
    "microchipped",
    "off_lead_consent",
    "vaccinated",
    "flead_wormed",
    "insured",
    "leucillin",
    "noise_sensitive",
]


def convert_to_tags(apps, schema_editor):
    Tag = apps.get_model("taggit", "Tag")
    TaggedItem = apps.get_model("taggit", "TaggedItem")
    ContentType = apps.get_model("contenttypes", "ContentType")

    try:
        ct = ContentType.objects.get(app_label="cerberus", model="pet")
    except ContentType.DoesNotExist:
        return

    Pet = apps.get_model("cerberus", "Pet")
    for pet in Pet.objects.all():
        for field in taggableFields:
            if getattr(pet, field, False):
                t, _ = Tag.objects.get_or_create(name=field.replace("_", " "), defaults={"slug": field})
                TaggedItem.objects.get_or_create(content_type_id=ct.id, object_id=pet.id, tag=t)


class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0008_customer_tags_pet_tags"),
    ]

    operations = [
        migrations.RunPython(convert_to_tags),
    ]

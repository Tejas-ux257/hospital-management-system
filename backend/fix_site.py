from django.contrib.sites.models import Site

Site.objects.update_or_create(
    id=1,
    defaults={
        "domain": "127.0.0.1:8000",
        "name": "localhost"
    }
)

print(" Django Site configured correctly")


Site.objects.all()



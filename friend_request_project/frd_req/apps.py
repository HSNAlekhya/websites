from django.apps import AppConfig


class FrdReqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frd_req'

def ready(self):
    import frd_req.signals
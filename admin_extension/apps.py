from django.apps import AppConfig


class AdminExtensionConfig(AppConfig):
    default_site = "spoj_tutor.admin.AdminExtension"
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_extension"

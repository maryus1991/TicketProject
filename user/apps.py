from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    verbose_name = 'کاربران'
    
    def ready(self):
        import user.signals
        return super().ready()
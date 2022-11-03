from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals

#  Since this signal is sent during the app registry population process,
#  and AppConfig.ready() runs after the app registry is fully populated,
# receivers cannot be connected in that method,
# One possibility is to connect them AppConfig.__init__() instead,
# taking care not to import models or trigger calls to the app registry.

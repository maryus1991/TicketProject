from django.apps import AppConfig


class TicketConfig(AppConfig):
    name = 'ticket'

    verbose_name = 'نوبت ها'

    # def ready(self):
    #     import ticket.signals
    #     return super().ready
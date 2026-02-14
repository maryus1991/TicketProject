from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, PassengerPlacement


@receiver(post_save, sender=Ticket)
def create_passenger_placement(sender, instance, created, **kwargs):
    if created :
        for _ in instance.count_ofـpassengers:
            PassengerPlacement.objects.create(
                ticket=instance,
                is_free=True,
            )
        print(f"{instance.count_ofـpassengers} placement create")  


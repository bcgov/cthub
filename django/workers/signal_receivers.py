from django.dispatch import receiver
from django_q.signals import pre_execute
from django_q.brokers import get_broker


@receiver(pre_execute)
def ack(sender, task, **kwargs):
    if task.get("ack_failure", False):
        ack_id = task.pop("ack_id", None)
        if ack_id:
            broker = get_broker()
            broker.acknowledge(ack_id)

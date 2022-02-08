from swa import crud
from swa.core.managers import QueueManager


def purchases_handler(manager: QueueManager):
    for item in manager.queue:
        crud.add_user_purchase(
            db=item.db,
            purchase=item.data.get('purchase')
        )

        manager.del_item(item.id)
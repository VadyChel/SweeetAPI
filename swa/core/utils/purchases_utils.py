from swa import crud
from swa.core.managers import QueueManager


def purchases_handler(manager: QueueManager):
    for item in manager.queue:
        if item.data["type"] == "user":
            crud.add_user_purchase(
                db=item.db,
                purchase=item.data.get('purchase')
            )
        else:
            crud.add_block_purchase(
                db=item.db,
                purchase=item.data.get('purchase')
            )

        manager.del_item(item.id)
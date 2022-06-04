from swa import crud
from swa.core.managers import QueueManager


async def purchases_handler(manager: QueueManager):
    for item in manager.queue:
        crud.purchases.create(
            db=item.db,
            purchase=item.data.get('purchase')
        )

        manager.del_item(item.id)
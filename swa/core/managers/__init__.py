from .queue_manager import QueueManager, QueueItemSchema
from swa.core.utils.purchases_utils import purchases_handler


purchases_manager = QueueManager(name="PurchasesManager", handler=purchases_handler)

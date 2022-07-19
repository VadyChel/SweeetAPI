from sqlalchemy.orm import Session
from swa import crud
from swa.schemas import UserPurchaseInRequest, CoinsLogsInRequest


def shop_logging(db: Session, purchase: UserPurchaseInRequest, coins_log: CoinsLogsInRequest):
    crud.purchases.create(db=db, purchase=purchase)
    crud.coins_logs.create(db=db, to_create=coins_log)

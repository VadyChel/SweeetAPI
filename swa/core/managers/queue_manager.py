import typing
import asyncio
from pydantic import BaseModel, Field


class QueueItemSchema(BaseModel):
    id: int = Field(0, const=True)
    db: typing.Any
    data: dict

    def __getitem__(self, item):
        return self.__getattribute__(item)


class QueueManager:
    def __init__(self, name: str, handler: typing.Callable):
        self.queue: typing.List[QueueItemSchema] = []
        self.name: str = name
        self.last_id: int = 0
        self.handler: typing.Callable = handler
        asyncio.create_task(self.handler_task())

    async def handler_task(self):
        while True:
            await self.handler(self)
            await asyncio.sleep(5)

    def get_queue(self):
        return self.queue

    def find(self, **kwargs):
        for item in self.queue:
            if all([item[key] == value for key, value in kwargs.items()]):
                return item

        return None

    def find_all(self, **kwargs):
        return [
            item
            for item in self.queue
            if all([item[key] == value for key, value in kwargs.items()])
        ]

    def add_item(self, item: QueueItemSchema):
        item.id = self._generate_id()
        self.queue.append(item)

    def del_item(self, item_id: int):
        for item in self.queue:
            if item.id == item_id:
                self.queue.remove(item)
                return item
        return None

    def _generate_id(self):
        new_id = self.last_id + 1
        self.last_id = new_id
        return new_id

    def __str__(self):
        return "Manager(name={0.name}, handler={0.handler}, queue={{".format(self)+("\n".join([
            "Item(id={0.id}, data={0.data})".format(item)
            for item in self.queue
        ]))+"})"
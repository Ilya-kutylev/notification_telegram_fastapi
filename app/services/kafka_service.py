from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json


class KafkaService:
    def __init__(self, broker_url: str, topic: str):
        self.broker_url = broker_url
        self.topic = topic
        self.producer = AIOKafkaProducer(bootstrap_servers=self.broker_url)
        self.consumer = AIOKafkaConsumer(self.topic,
                                         bootstrap_servers=self.broker_url,
                                         group_id='notification-group')

    async def start_producer(self):
        await self.producer.start()

    async def stop_producer(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, message: dict):
        await self.producer.send_and_wait(self.topic, json.dumps(message).encode("utf-8"))

    async def start_consumer(self, process_message):
        if not self.consumer:
            raise RuntimeError("Kafka consumer is not initialized.")
        await self.consumer.start()

        try:
            async for msg in self.consumer:
                message = json.loads(msg.value.decode("utf-8"))
                await process_message(message)
        finally:
            await self.consumer.stop()


async def get_kafka_service():
    return KafkaService(broker_url="localhost:9092", topic="notifications")

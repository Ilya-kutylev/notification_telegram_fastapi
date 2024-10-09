import uvicorn
from fastapi import FastAPI, BackgroundTasks

from app.function.notifications import router_notification
from app.services.kafka_service import get_kafka_service
from app.services.telegram_bot_service import kafka_consumer

app = FastAPI()

app.include_router(router_notification)

@app.on_event("startup")
async def startup_event():
    kafka_service = await get_kafka_service()
    await kafka_service.start_producer()

    background_tasks = BackgroundTasks()
    background_tasks.add_task(kafka_consumer, kafka_service)

@app.on_event("shutdown")
async def shutdown_event():
    kafka_service = await get_kafka_service()
    await kafka_service.stop_producer()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=2000)

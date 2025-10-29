from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.sensor_service import SensorService
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()
sensor_service = SensorService()

async def cleanup_old_data():
    """Limpa dados antigos (> 30 dias)"""
    logger.info("🧹 Running cleanup job...")
    # Implementar lógica de limpeza se necessário

def start_scheduler():
    scheduler.add_job(
        cleanup_old_data,
        'interval',
        hours=24,
        id='cleanup',
        coalesce=True,
        misfire_grace_time=60
    )
    scheduler.start()
    logger.info("⏰ Scheduler started")
from src.cfg import log
import uasyncio as asyncio
from . import hardware
import utime as time
from .web import app


async def every_second():
    """
    func that run every 3 seconds
    useful for have a finer controll on pump
    """
    while True:
        hardware.ledActuactor.update()
        hardware.pumpActuator.update()
        await asyncio.sleep(1)


def start():

    asyncio.create_task(every_second())

    app.run(host="0.0.0.0", port=80, debug=True)

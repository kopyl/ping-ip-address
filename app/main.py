import os
from datetime import datetime, timezone
import asyncio
from . import db
from . import telegram
from .ping import ping
from .messages import make_status_message


IP_ADDRESS = os.getenv("PING_IP_ADDRESS")
PORT = int(os.getenv("PING_PORT"))


async def main():
    last_status = db.get_last_status(IP_ADDRESS, PORT)
    is_reachable = ping(IP_ADDRESS, PORT)
    status_change_counter = 0

    while True:
        if is_reachable != last_status["status"]:
            status_change_counter += 1
            timestamp = datetime.now(timezone.utc)

            message = make_status_message(is_reachable, last_status, timestamp, status_change_counter)

            await telegram.send_telegram_message(message)
            db.write_status(is_reachable, IP_ADDRESS, PORT, timestamp)

            last_status = {
                "status": is_reachable,
                "timestamp": timestamp
            }
        await asyncio.sleep(1)

        is_reachable = ping(IP_ADDRESS, PORT)


if __name__ == "__main__":
    asyncio.run(main())
    
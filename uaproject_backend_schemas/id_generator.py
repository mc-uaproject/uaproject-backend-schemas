import logging
import re
import threading
import time
from datetime import datetime, timezone
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


def get_container_name_sync():
    try:
        container_id = open("/etc/hostname").read().strip()
        with httpx.Client(transport=httpx.HTTPTransport(uds="/var/run/docker.sock")) as client:
            r = client.get(f"http://localhost/containers/{container_id}/json")
            r.raise_for_status()
            return r.json()["Name"].lstrip("/")
    except Exception as e:
        logger.debug(f"Skipping container name resolution (not in Docker?): {e}")
        return None


def get_replica_index_sync():
    name = get_container_name_sync()
    logger.debug(f"Container name: {name}")

    if not name:
        return

    match = re.search(r"-(\d+)$", name)
    return int(match[1]) if match else None


class UAIdGenerator:
    def __init__(self, epoch: Optional[datetime] = None, replica_id: Optional[int] = None):
        default_epoch = datetime.fromtimestamp(1744463384, tz=timezone.utc)
        self.epoch = epoch.astimezone(timezone.utc) if epoch else default_epoch
        self.replica_id = replica_id or get_replica_index_sync() or 0
        self.lock = threading.Lock()
        self.last_timestamp = 0
        self.sequence = 0

    def generate(self, custom_date: Optional[datetime] = None) -> int:
        with self.lock:
            now = int(
                (custom_date.astimezone(timezone.utc) - self.epoch).total_seconds() * 1000
            ) if custom_date else int(
                (datetime.now(timezone.utc) - self.epoch).total_seconds() * 1000
            )
            if now == self.last_timestamp:
                self.sequence += 1
                if self.sequence >= 10:
                    time.sleep(0.001)
                    return self.generate(custom_date)
            else:
                self.sequence = 0
                self.last_timestamp = now

            return now * 1000 + (self.replica_id * 10) + self.sequence

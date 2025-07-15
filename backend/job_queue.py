import asyncio
from collections import defaultdict

queues = defaultdict(asyncio.Queue)

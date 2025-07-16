from collections import defaultdict
import asyncio

queues = defaultdict(asyncio.Queue)
jobs = {}
video_results = {}

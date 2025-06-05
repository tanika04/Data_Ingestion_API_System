from collections import deque
from typing import Dict
from models import Ingestion

# Global storage
ingestions: Dict[str, Ingestion] = {}
processing_queue = []  
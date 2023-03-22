#!/usr/bin/env python3

import logging
from server import svserver

logging.basicConfig(filename="slangserver.log", filemode="w", level=logging.INFO)
logger = logging.getLogger("slangserver logger")


svserver.start_io()


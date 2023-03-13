#!/usr/bin/env python3

import logging
from server import svserver


logging.basicConfig(filename="pygls.log", filemode="w", level=logging.INFO)
logger = logging.getLogger("svlangserver logger")


svserver.start_io()

import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("thegrid")

# Importing causes patterns to be registered, so do it after logging
from thegrid.control import Control

# Enqueue the main task
logger.info("Main loop starting")
loop = asyncio.get_event_loop()
ctrl = Control()
loop.create_task(ctrl.setup())

# Run the main loop
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    ctrl.shutdown()
    loop.close()

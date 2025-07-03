import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logging():
    # Para desenvolvimento, usar apenas console logging
    if os.getenv("DEBUG") == "True" or os.getenv("TESTING") == "True":
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    else:
        # Em produção, usar arquivo + console
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout),
            ],
        )

    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete.")

    return logger

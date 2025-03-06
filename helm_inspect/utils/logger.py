"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import logging
import sys


def setup_logger(verbose: bool = False) -> logging.Logger:
    """
    Setup logger for the application.

    Args:
        verbose (bool): Enable verbose logging (debug mode).

    Returns:
        logging.Logger: Logger object.
    """

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("helm-inspect")

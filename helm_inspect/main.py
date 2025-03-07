"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from art import text2art
import sys

from helm_inspect.utils.cli import (
    detect_drift,
    parse_args,
    validate_args,
    check_prerequisites,
)
from helm_inspect.utils.cluster import get_cluster_name
from helm_inspect.utils.calibration import calibrate_system
from helm_inspect.utils.logger import setup_logger


def main():
    print(text2art("\n\nHelm\nInspect\n\n", font="speed"))

    check_prerequisites()

    args = parse_args()
    logger = setup_logger(args.verbose)
    validate_args(args)

    cluster_name = get_cluster_name()

    if args.calibrate:
        try:
            calibrate_system(args.release, args.namespace, cluster_name)
            return
        except Exception as e:
            logger.error(f"❌ Error calibrating system: {str(e)}")
            sys.exit(1)
        return

    try:
        detect_drift(
            args.release,
            args.namespace,
            cluster_name,
            args.no_ignore,
            args.slack_channel,
            args.slack_token,
        )
    except Exception as e:
        logger.error(f"❌ Error detecting drift: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
from datetime import datetime

from helm_inspect.utils.logger import setup_logger
from helm_inspect.utils.drift_check import get_ignorable_keys
from helm_inspect.utils.constant import TMP_DIR, DRIFT_DIR

logger = setup_logger()


def get_calibration_file(release: str, namespace: str, cluster: str) -> dict:
    """
    Retrieve existing calibration data if available.

    Args:
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.

    Returns:
        dict or None: The calibration data if available, otherwise None.
    """

    calibration_file = TMP_DIR / f"calibration_{release}_{namespace}_{cluster}.json"
    if calibration_file.exists():
        try:
            with open(calibration_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to read calibration file: {e}")
    return None


def save_calibration_data(
    ignorable_keys: list, release: str, namespace: str, cluster: str
) -> None:
    """
    Save calibration data to file.

    Args:
        ignorable_keys (list): List of keys to ignore.
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.
    """

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    calibration_file = TMP_DIR / f"calibration_{release}_{namespace}_{cluster}.json"

    calibration_data = {
        "date": datetime.utcnow().isoformat(),
        "release": release,
        "namespace": namespace,
        "cluster": cluster,
        "ignorable_keys": ignorable_keys,
    }

    try:
        with open(calibration_file, "w") as f:
            json.dump(calibration_data, f, indent=2)
        logger.info("✅ Calibration data saved successfully.")
    except OSError as e:
        logger.error(f"Failed to save calibration file: {e}")


def delete_calibration_file(release: str, namespace: str, cluster: str) -> None:
    """
    Delete calibration file for a given release.

    Args:
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.
    """

    calibration_file = TMP_DIR / f"calibration_{release}_{namespace}_{cluster}.json"

    if calibration_file.exists():
        try:
            calibration_file.unlink()
            logger.info("✅ Calibration data deleted successfully.")
        except OSError as e:
            logger.error(f"Failed to delete calibration file: {e}")


def calibrate_system(release: str, namespace: str, cluster_name: str):
    """
    Calibrate the system by deleting existing calibration data and saving new data.

    Args:
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster_name (str): The cluster name.
    """

    delete_calibration_file(release, namespace, cluster_name)
    ignorable_keys = get_ignorable_keys(release, namespace)
    save_calibration_data(ignorable_keys, release, namespace, cluster_name)


def save_drift_data(drift_data: dict, release: str, namespace: str, cluster: str):
    """
    Save drift data to file.

    Args:
        drift_data (dict): The drift data to save.
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.
    """

    DRIFT_DIR.mkdir(parents=True, exist_ok=True)
    drift_file = DRIFT_DIR / f"drift_{release}_{namespace}_{cluster}.json"

    try:
        with open(drift_file, "w") as f:
            json.dump(drift_data, f, indent=2)
        logger.info("✅ Drift data saved successfully.")
    except OSError as e:
        logger.error(f"Failed to save drift file: {e}")

"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import argparse
import shutil
import sys

from datetime import datetime
from pathlib import Path

from helm_inspect.utils.calibration import get_calibration_file, save_drift_data
from helm_inspect.utils.drift_check import check_drift, IGNORABLE_KEYS
from helm_inspect.utils.logger import setup_logger
from typing import Optional

logger = setup_logger()


def check_prerequisites():
    """
    Ensure required tools are installed.

    Checks if 'helm' and 'kubectl' are installed and available in the system PATH.
    If any of the tools are missing, logs an error message and exits the program.
    """

    missing_tools = [tool for tool in ["helm", "kubectl"] if not shutil.which(tool)]

    if missing_tools:
        logger.error("❌ Missing prerequisites:")
        for tool in missing_tools:
            logger.error(f"   - {tool} is not installed or not in PATH.")
        logger.info("Please install the missing tools and try again.")
        sys.exit(1)


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="HelmInspect - Detect drift between Helm and Kubernetes"
    )

    parser.add_argument("-r", "--release", required=True, help="Helm release name")
    parser.add_argument("-n", "--namespace", required=True, help="Kubernetes namespace")

    parser.add_argument(
        "-c",
        "--calibrate",
        action="store_true",
        help="Calibrate HelmInspect to capture system-generated keys after a fresh Helm installation",
    )

    parser.add_argument(
        "-I",
        "--no-ignore",
        action="store_true",
        help="Disable key ignoring for strict drift detection (shows all differences including system-generated keys)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (debug mode).",
    )

    return parser.parse_args()


def detect_drift(
    release: str, namespace: str, cluster_name: str, no_ignore: bool
) -> None:
    """
    Detect drift between Helm and Kubernetes.

    Args:
        release (str): Helm release name.
        namespace (str): Kubernetes namespace.
        cluster_name (str): Kubernetes cluster name.
        no_ignore (bool): Flag to disable key ignoring for strict drift detection.
    """

    calibration_data = get_calibration_file(release, namespace, cluster_name)

    if calibration_data:
        try:
            calibration_date = datetime.fromisoformat(calibration_data["date"])
            days_old = (datetime.utcnow() - calibration_date).days
            if days_old > 30:
                logger.warning(
                    f"⚠️ Calibration data is {days_old} days old. Consider recalibrating.\n"
                )
        except (KeyError, ValueError):
            logger.error("❌ Invalid calibration data format. Consider recalibrating.")

    no_cal_file = False

    if no_ignore:
        logger.info("✨ Proceeding without ignoring any keys.\n\n")
        ignorable_keys: Optional[list] = None
    elif calibration_data:
        logger.info("✨ Using existing calibration data.\n\n")
        ignorable_keys = calibration_data["ignorable_keys"]
    else:
        logger.warning(
            "⚠️ No calibration data found!\n"
            "  • Using default ignorable keys which may not be accurate.\n"
            f"  • Run 'helm-inspect --calibrate --release {release} --namespace {namespace}'\n"
            "    immediately after a fresh Helm installation for accurate drift detection.\n\n"
        )
        no_cal_file = True
        ignorable_keys = IGNORABLE_KEYS.copy()

    drift_meta = check_drift(release, namespace, ignorable_keys, no_cal_file)
    drift_file = (
        Path.home()
        / ".helminspect"
        / "drift"
        / f"drift_{release}_{namespace}_{cluster_name}.json"
    )

    save_drift_data(drift_meta, release, namespace, cluster_name)

    logger.info("✨ Drift detection completed.")
    logger.info(
        "-----\n\n✨Drift Summary✨\n\n"
        f" • Release: {release}\n"
        f" • Namespace: {namespace}\n\n"
        f" • Drifts: {drift_meta['drift_summary']['total_drifts']}\n"
        f"   +---------------------+-----------------------+\n"
        f"   | Type                | Count                 |\n"
        f"   +---------------------+-----------------------+\n"
        f"   | New Keys            | {drift_meta['drift_summary']['new_keys']: <22}|\n"
        f"   | Missing Keys        | {drift_meta['drift_summary']['removed_keys']: <22}|\n"
        f"   | Changed Keys        | {drift_meta['drift_summary']['modified_keys']: <22}|\n"
        f"   +---------------------+-----------------------+\n\n"
        f"  • Drift Report File: {drift_file}\n"
    )

"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import argparse
import shutil
import sys
import os
import subprocess
import json
from datetime import datetime
from art import text2art

from helm_inspect.core import check_drift, get_ignorable_keys
from helm_inspect.utils import IGNORABLE_KEYS


def check_prerequisites():
    missing_tools = []
    for tool in ["helm", "kubectl"]:
        if not shutil.which(tool):
            missing_tools.append(tool)

    if missing_tools:
        print("❌ Missing prerequisites:")
        for tool in missing_tools:
            print(f"   - {tool} is not installed or not in PATH.")
        print("\nPlease install the missing tools and try again.")
        sys.exit(1)


def get_cluster_name():
    try:
        result = subprocess.run(
            [
                "kubectl",
                "config",
                "view",
                "--minify",
                "-o",
                "jsonpath={.clusters[0].name}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown_cluster"


def get_calibration_file(release, namespace, cluster):
    tmp_dir = os.path.join(os.path.expanduser("~"), ".helminspect", "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    calibration_file = os.path.join(
        tmp_dir, f"calibration_{release}_{namespace}_{cluster}.json"
    )

    if os.path.exists(calibration_file):
        with open(calibration_file, "r") as f:
            return json.load(f)

    return None


def save_calibration_data(ignorable_keys, release, namespace, cluster):
    tmp_dir = os.path.join(os.path.expanduser("~"), ".helminspect", "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    calibration_file = os.path.join(
        tmp_dir, f"calibration_{release}_{namespace}_{cluster}.json"
    )

    calibration_data = {
        "date": datetime.utcnow().isoformat(),
        "release": release,
        "namespace": namespace,
        "cluster": cluster,
        "ignorable_keys": ignorable_keys,
    }

    with open(calibration_file, "w") as f:
        json.dump(calibration_data, f, indent=2)


def delete_calibration_file(release, namespace, cluster):
    tmp_dir = os.path.join(os.path.expanduser("~"), ".helminspect", "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    calibration_file = os.path.join(
        tmp_dir, f"calibration_{release}_{namespace}_{cluster}.json"
    )

    if os.path.exists(calibration_file):
        os.remove(calibration_file)


def main():
    print(text2art("Helm\nInspect", font="speed"))

    check_prerequisites()

    parser = argparse.ArgumentParser(
        description="HelmInspect - Detect drift between Helm and Kubernetes"
    )
    parser.add_argument("--release", required=True, help="Helm release name")
    parser.add_argument("--namespace", required=True, help="Kubernetes namespace")
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="Calibrate HelmInspect to capture system-generated keys after a fresh Helm installation",
    )
    parser.add_argument(
        "--no-ignore",
        action="store_true",
        help="Disable key ignoring for strict drift detection (shows all differences including system-generated keys)",
    )

    args = parser.parse_args()

    cluster_name = get_cluster_name()

    if args.no_ignore and args.calibrate:
        print(
            "❌ Cannot use --no-ignore with --calibrate. The --calibrate flag is used to identify keys to ignore, "
            "while --no-ignore explicitly disables this feature. Please use only one of these flags."
        )
        return

    if args.calibrate:
        delete_calibration_file(args.release, args.namespace, cluster_name)
        print("✅ Calibration data deleted.")

        ignorable_keys = get_ignorable_keys(args.release, args.namespace)
        save_calibration_data(
            ignorable_keys, args.release, args.namespace, cluster_name
        )
        print("✅ New calibration data saved with ignorable keys.")

        return

    calibration_data = get_calibration_file(args.release, args.namespace, cluster_name)

    if calibration_data:
        try:
            calibration_date = datetime.fromisoformat(calibration_data["date"])
            days_old = (datetime.utcnow() - calibration_date).days
            if days_old > 30:
                print(
                    f"WARNING: Calibration data is {days_old} days old. Consider recalibrating for accurate drift detection. \n"
                )
        except (KeyError, ValueError):
            print("ERROR: Calibration data format is invalid. Consider recalibrating.")

    if args.no_ignore:
        print("✅ Proceeding without ignoring any keys.")
        ignorable_keys = None
    elif calibration_data:
        print("✅ Using existing calibration data.")
        ignorable_keys = calibration_data["ignorable_keys"]
    else:
        print(
            "CAUTION: No calibration data found for this release/namespace/cluster combination!\n\n"
            "  • Using default ignorable keys which may not be accurate for your environment\n"
            f"  • For best results, run 'helm-inspect --calibrate --release {args.release} --namespace {args.namespace}'\n"
            "    immediately after a fresh Helm installation when you know there is no drift\n"
            "  • This creates a profile of system-generated keys specific to your cluster"
        )
        ignorable_keys = IGNORABLE_KEYS.copy()
    check_drift(args.release, args.namespace, ignorable_keys)


if __name__ == "__main__":
    main()

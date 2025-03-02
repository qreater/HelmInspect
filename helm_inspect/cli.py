"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import argparse
import shutil
import sys
from helm_inspect.core import check_drift
from art import text2art


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


def main():
    print(text2art("Helm\nInspect", font="speed"))

    check_prerequisites()

    parser = argparse.ArgumentParser(
        description="HelmInspect - Detect drift between Helm and Kubernetes"
    )
    parser.add_argument("--release", required=True, help="Helm release name")
    parser.add_argument("--namespace", required=True, help="Kubernetes namespace")
    args = parser.parse_args()

    check_drift(args.release, args.namespace)


if __name__ == "__main__":
    main()

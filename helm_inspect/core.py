"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import difflib
from helm_inspect.utils import (
    get_helm_manifest,
    get_k8s_resource,
    extract_relevant_data,
)


def compare_values(helm_manifest, namespace):
    for resource in helm_manifest:
        kind = resource.get("kind", "Unknown")
        name = resource.get("metadata", {}).get("name", "Unknown")

        if kind not in ["Deployment", "Service", "Ingress", "ConfigMap", "Secret"]:
            continue

        print(f"\n🔍 Checking drift for {kind} `{name}`...")

        live_resource = get_k8s_resource(kind, name, namespace)
        if not live_resource:
            print(f"❌ Drift detected: {kind} `{name}` is missing in Kubernetes.")
            continue

        helm_data = extract_relevant_data(resource)
        live_data = extract_relevant_data(live_resource)

        helm_json = json.dumps(helm_data, indent=2, sort_keys=True)
        live_json = json.dumps(live_data, indent=2, sort_keys=True)

        diff = list(
            difflib.unified_diff(
                helm_json.splitlines(),
                live_json.splitlines(),
                fromfile="Helm Manifest",
                tofile="Live Kubernetes",
            )
        )

        if diff:
            print(f"❌ Drift detected in {kind} `{name}`:")
            print("\n".join(diff))
        else:
            print(f"✅ No drift detected in {kind} `{name}`.")


def check_drift(release, namespace):
    helm_manifest = get_helm_manifest(release, namespace)

    if not helm_manifest:
        print("⚠️ No Helm manifest found. Ensure the release exists and try again.")
        return

    compare_values(helm_manifest, namespace)

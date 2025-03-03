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


def extract_keys_recursive(data, parent_key=""):
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys.add(full_key)
            keys.update(extract_keys_recursive(value, full_key))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            keys.update(
                extract_keys_recursive(item, f"{parent_key}[{index}]")
                if parent_key
                else extract_keys_recursive(item)
            )
    return keys


def get_ignorable_keys(release, namespace):
    helm_manifest = get_helm_manifest(release, namespace)
    ignorable_keys = set()
    resource_count = 0

    print(f"🔍 Analyzing {len(helm_manifest)} resources for calibration...")

    for resource in helm_manifest:
        if not resource:
            continue

        kind = resource.get("kind", "Unknown")
        name = resource.get("metadata", {}).get("name", "Unknown")

        print(f"  📊 Processing {kind}/{name}...", end="\r")

        live_resource = get_k8s_resource(kind, name, namespace)
        if not live_resource:
            continue

        helm_keys = extract_keys_recursive(extract_relevant_data(resource, None))
        live_keys = extract_keys_recursive(extract_relevant_data(live_resource, None))

        ignorable_keys.update(live_keys - helm_keys)
        resource_count += 1

    print(
        f"✅ Analyzed {resource_count} resources and found {len(ignorable_keys)} drift-prone keys."
    )

    return list(ignorable_keys)


def compare_values(helm_manifest, namespace, ignorable_keys):
    for resource in helm_manifest:
        if not resource:
            continue

        kind = resource.get("kind", "Unknown")
        name = resource.get("metadata", {}).get("name", "Unknown")

        if kind not in ["Deployment", "Service", "Ingress", "ConfigMap", "Secret"]:
            continue

        print(f"\n🔍 Checking drift for {kind} `{name}`...")

        live_resource = get_k8s_resource(kind, name, namespace)
        if not live_resource:
            print(f"❌ Drift detected: {kind} `{name}` is missing in Kubernetes.")
            continue

        helm_data = extract_relevant_data(resource, ignorable_keys)
        live_data = extract_relevant_data(live_resource, ignorable_keys)

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


def check_drift(release, namespace, ignorable_keys):
    helm_manifest = get_helm_manifest(release, namespace)

    if not helm_manifest:
        print("⚠️ No Helm manifest found. Ensure the release exists and try again.")
        return

    compare_values(helm_manifest, namespace, ignorable_keys)

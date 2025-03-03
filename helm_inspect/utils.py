"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import subprocess
import json
import yaml
from typing import Any, Dict, List, Set, Union

IGNORABLE_KEYS = [
    "clusterIP",
    "clusterIPs",
    "internalTrafficPolicy",
    "ipFamilies",
    "ipFamilyPolicy",
    "sessionAffinity",
    "progressDeadlineSeconds",
    "revisionHistoryLimit",
    "template.metadata.annotations",
    "strategy",
    "template.metadata.creationTimestamp",
    "template.spec.dnsPolicy",
    "template.spec.restartPolicy",
    "template.spec.schedulerName",
    "template.spec.securityContext",
    "template.spec.terminationGracePeriodSeconds",
    "template.spec.containers.resources",
    "template.spec.containers.terminationMessagePath",
    "template.spec.containers.terminationMessagePolicy",
    "template.spec.containers.ports.protocol",
    "volumes.[0].configMap.defaultMode",
    "ingressClassName",
]


def run_command(command: List[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(command)}")
        print(f"🔍 Output: {e.stderr.strip()}")
        return ""


def get_helm_manifest(release: str, namespace: str) -> List[Dict[str, Any]]:
    output = run_command(["helm", "get", "manifest", release, "-n", namespace])
    try:
        return list(yaml.safe_load_all(output)) if output else []
    except yaml.YAMLError:
        print("❌ Failed to parse Helm manifest YAML.")
        return []


def get_k8s_resource(kind: str, name: str, namespace: str) -> Dict[str, Any]:
    output = run_command(
        ["kubectl", "get", kind.lower(), name, "-n", namespace, "-o", "json"]
    )
    try:
        return json.loads(output) if output else {}
    except json.JSONDecodeError:
        print(f"❌ Failed to parse {kind} `{name}` JSON.")
        return {}


def remove_nested_keys(data: Any, keys_to_ignore: Set[str]) -> Any:
    """Recursively removes ignored keys from a nested dictionary or list."""

    def pop_nested_keys(d: Union[Dict[str, Any], List[Any]], key_path: str):
        """Recursively traverses the dictionary/list and removes keys using a key path."""
        keys = key_path.split(".")
        current = d

        for i, key in enumerate(keys):
            if "[" in key and "]" in key:
                key_name, index_part = key.split("[", 1)
                index = int(index_part.rstrip("]"))

                if isinstance(current, dict) and key_name in current:
                    current = current[key_name]

                if isinstance(current, list) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return

            elif isinstance(current, dict):
                if key in current:
                    if i == len(keys) - 1:
                        current.pop(key, None)
                    else:
                        current = current[key]

            elif isinstance(current, list):
                for item in current:
                    if isinstance(item, dict):
                        pop_nested_keys(item, ".".join(keys[i:]))
                break

    if isinstance(data, dict):
        cleaned_data = {
            k: remove_nested_keys(v, keys_to_ignore) for k, v in data.items()
        }
        for key_path in keys_to_ignore:
            pop_nested_keys(cleaned_data, key_path)
        return cleaned_data

    elif isinstance(data, list):
        return [remove_nested_keys(item, keys_to_ignore) for item in data]

    return data


def extract_relevant_data(
    resource: Dict[str, Any], ignorable_keys: list
) -> Dict[str, Any]:
    """Extracts relevant data from a Kubernetes resource."""
    kind = resource.get("kind", "Unknown")
    if kind in ["ConfigMap", "Secret"]:
        return resource.get("data", {})

    elif kind in ["Deployment", "Service", "Ingress"]:
        spec = resource.get("spec", {})

        if not ignorable_keys:
            return spec
        spec = remove_nested_keys(spec, ignorable_keys)
        return spec

    return resource

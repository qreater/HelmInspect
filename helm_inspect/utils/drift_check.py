"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import difflib
from typing import Any, Dict, List, Set

from helm_inspect.utils.cluster import get_helm_manifest, get_k8s_resource
from helm_inspect.utils.logger import setup_logger

logger = setup_logger()

SUPPORTED_KINDS = ["Deployment", "Service", "Ingress", "ConfigMap", "Secret"]

IGNORABLE_KEYS = [
    "Ingress;ingressClassName",
    "Deployment;template.metadata.creationTimestamp",
    "Deployment;template.spec.containers[0].terminationMessagePath",
    "Deployment;progressDeadlineSeconds",
    "Deployment;template.spec.schedulerName",
    "Deployment;revisionHistoryLimit",
    "Deployment;template.spec.securityContext",
    "Service;ipFamilyPolicy",
    "Service;clusterIPs[0]",
    "Deployment;template.spec.dnsPolicy",
    "Deployment;template.spec.terminationGracePeriodSeconds",
    "Deployment;template.spec.volumes[0].configMap.defaultMode",
    "Deployment;strategy.rollingUpdate.maxUnavailable",
    "Service;ipFamilies[0]",
    "Service;sessionAffinity",
    "Deployment;template.spec.restartPolicy",
    "Deployment;strategy.type",
    "Service;clusterIP",
    "Service;internalTrafficPolicy",
    "Deployment;template.spec.containers[0].terminationMessagePolicy",
    "Deployment;strategy.rollingUpdate.maxSurge",
    "Deployment;template.spec.containers[0].resources",
    "Deployment;template.spec.containers[0].ports[0].protocol",
]


def compare_values(
    helm_manifest: List[Dict[str, Any]],
    namespace: str,
    ignorable_keys: List[str],
    no_cal_file: bool = False,
) -> dict:
    """
    Compares values between Helm manifest and live Kubernetes resources.

    Args:
        helm_manifest (List[Dict[str, Any]]): The Helm manifest.
        namespace (str): The Kubernetes namespace.
        ignorable_keys (List[str]): The keys to ignore during comparison.
        no_cal_file (bool): Flag to disable calibration file.

    Returns:
        dict: The drift logs and reports.
    """

    drift_logs = []
    drift_reports = []

    total_drifts, total_new_keys, total_removed_keys, total_modified_keys = 0, 0, 0, 0

    for resource in helm_manifest:
        if not resource:
            continue

        kind, name = get_resource_info(resource)

        if not is_supported_resource(kind):
            continue

        logger.info(f"Checking drift for {kind} `{name}`...")

        live_resource = get_k8s_resource(kind, name, namespace)
        if not live_resource:
            message = handle_missing_resource(kind, name)
            drift_logs.append(message)
            continue

        helm_data = extract_relevant_data(resource, ignorable_keys, no_cal_file)
        live_data = extract_relevant_data(live_resource, ignorable_keys, no_cal_file)

        diff = detect_drift(helm_data, live_data)
        drift_logs.append(handle_drift_diff(diff, kind, name))

        helm_key_values = extract_deepest_keys_values(helm_data)
        live_key_values = extract_deepest_keys_values(live_data)

        new_keys, removed_keys, modified_keys = extract_drift_keys(
            helm_key_values, live_key_values
        )

        total_new_keys += len(new_keys)
        total_removed_keys += len(removed_keys)
        total_modified_keys += len(modified_keys)
        total_drifts += len(new_keys) + len(removed_keys) + len(modified_keys)

        drift_reports.extend(
            generate_drift_report(
                kind,
                name,
                new_keys,
                removed_keys,
                modified_keys,
                helm_key_values,
                live_key_values,
            )
        )

    return {
        "drift_logs": drift_logs,
        "drift_reports": drift_reports,
        "drift_summary": {
            "total_drifts": total_drifts,
            "new_keys": total_new_keys,
            "removed_keys": total_removed_keys,
            "modified_keys": total_modified_keys,
        },
    }


def get_resource_info(resource: Dict[str, Any]) -> tuple:
    """
    Extracts the kind and name from the Helm resource.

    Args:
        resource (Dict[str, Any]): The Helm resource.

    Returns:
        tuple: A tuple containing the kind and name of the resource.
    """

    kind = resource.get("kind", "Unknown")
    name = resource.get("metadata", {}).get("name", "Unknown")
    return kind, name


def is_supported_resource(kind: str) -> bool:
    """
    Checks if the resource kind is supported.

    Args:
        kind (str): The Kubernetes resource kind.
    """

    return kind in SUPPORTED_KINDS


def handle_missing_resource(kind: str, name: str) -> str:
    """
    Handles the case where the resource is missing in Kubernetes.

    Args:
        kind (str): The Kubernetes resource kind.
        name (str): The Kubernetes resource name.

    Returns:
        str: The drift message.
    """

    message = f"Drift detected: {kind} `{name}` is missing in Kubernetes.\n"
    logger.error(message)
    return message


def handle_drift_diff(diff: list, kind: str, name: str) -> str:
    """
    Handles and logs the drift diff results.

    Args:
        diff (list): The drift diff.
        kind (str): The Kubernetes resource kind.
        name (str): The Kubernetes resource name.

    Returns:
        str: The drift message.
    """

    if diff:
        message = f"❌ Drift detected in {kind} `{name}`:\n" + "\n".join(diff)
        logger.error(f"{message}\n")
        return message
    else:
        message = f"✅ No drift detected in {kind} `{name}`.\n"
        logger.info(message)
        return message


def detect_drift(helm_data: Dict[str, Any], live_data: Dict[str, Any]) -> List[str]:
    """
    Compares Helm data and live data to find drift.

    Args:
        helm_data (Dict[str, Any]): The Helm data.
        live_data (Dict[str, Any]): The live data.

    Returns:
        List[str]: A list of drift messages.
    """

    helm_json = json.dumps(helm_data, indent=2, sort_keys=True)
    live_json = json.dumps(live_data, indent=2, sort_keys=True)

    return list(
        difflib.unified_diff(
            helm_json.splitlines(),
            live_json.splitlines(),
            fromfile="Helm Manifest",
            tofile="Live Kubernetes",
        )
    )


def extract_drift_keys(
    helm_key_values: Dict[str, Any], live_key_values: Dict[str, Any]
) -> tuple:
    """
    Extracts new, removed, and modified keys between Helm and live data.

    Args:
        helm_key_values (Dict[str, Any]): The Helm key values.
        live_key_values (Dict[str, Any]): The live key values.

    Returns:
        tuple: A tuple containing new, removed, and modified keys.
    """

    new_keys = set(live_key_values.keys()) - set(helm_key_values.keys())
    removed_keys = set(helm_key_values.keys()) - set(live_key_values.keys())
    modified_keys = {
        key
        for key in helm_key_values.keys() & live_key_values.keys()
        if helm_key_values[key] != live_key_values[key]
    }

    return new_keys, removed_keys, modified_keys


def generate_drift_report(
    kind: str,
    name: str,
    new_keys: set,
    removed_keys: set,
    modified_keys: set,
    helm_key_values: dict,
    live_key_values: dict,
) -> list:
    """
    Generates drift reports for new, removed, and modified keys.

    Args:
        kind (str): The Kubernetes resource kind.
        name (str): The Kubernetes resource name.
        new_keys (set): The new keys.
        removed_keys (set): The removed keys.
        modified_keys (set): The modified keys.
        helm_key_values (dict): The Helm key values.
        live_key_values (dict): The live key values.

    Returns:
        list: A list of drift reports.
    """

    drift_reports = []

    for key in new_keys:
        drift_reports.append(
            {"kind": kind, "name": name, "drift_type": "new_key", "change": key}
        )

    for key in removed_keys:
        drift_reports.append(
            {"kind": kind, "name": name, "drift_type": "key_removed", "change": key}
        )

    for key in modified_keys:
        drift_reports.append(
            {
                "kind": kind,
                "name": name,
                "drift_type": "value_modified",
                "change": {
                    "key": key,
                    "old_value": helm_key_values[key],
                    "new_value": live_key_values[key],
                },
            }
        )

    return drift_reports


def check_drift(
    release: str, namespace: str, ignorable_keys: List[str], no_cal_file: bool = False
) -> dict:
    """
    Checks for drift between Helm manifest and live Kubernetes resources.

    Args:
        release (str): The Helm release name.
        namespace (str): The Kubernetes namespace.
        ignorable_keys (List[str]): The keys to ignore during comparison.
        no_cal_file (bool): Flag to disable calibration file.

    Returns:
        dict: A dictionary containing drift logs, reports, and summary.
    """

    helm_manifest = get_helm_manifest(release, namespace)

    if not helm_manifest:
        message = (
            "\n\n❌ No Helm manifest found. Ensure the release exists and try again.\n\n"
        )
        logger.error(message)
        return {
            "drift_logs": [message],
            "drift_reports": [],
            "drift_summary": {
                "total_drifts": 0,
                "new_keys": 0,
                "removed_keys": 0,
                "modified_keys": 0,
            },
        }

    return compare_values(helm_manifest, namespace, ignorable_keys, no_cal_file)


def extract_deepest_keys_values(data: Any, parent_key: str = "") -> Dict[str, Any]:
    """
    Recursively extracts only the deepest keys and their corresponding values
    from a nested dictionary or list.

    Args:
        data (Any): The data to extract keys and values from.
        parent_key (str): The parent key to prepend to the extracted keys.

    Returns:
        Dict[str, Any]: A dictionary mapping the deepest keys to their values.
    """
    result = {}

    if isinstance(data, dict):
        is_deepest = True
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            sub_result = extract_deepest_keys_values(value, full_key)
            if sub_result:
                result.update(sub_result)
                is_deepest = False
        if is_deepest:
            result[parent_key] = data

    elif isinstance(data, list):
        is_deepest = True
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]" if parent_key else f"[{index}]"
            sub_result = extract_deepest_keys_values(item, full_key)
            if sub_result:
                result.update(sub_result)
                is_deepest = False
        if is_deepest:
            result[parent_key] = data

    else:
        result[parent_key] = data

    return result


def get_ignorable_keys(release: str, namespace: str) -> List[str]:
    """
    Gets the keys that can be ignored during drift comparison.

    Args:
        release (str): The Helm release name.
        namespace (str): The Kubernetes namespace.

    Returns:
        List[str]: A list of ignorable keys.
    """
    helm_manifest = get_helm_manifest(release, namespace)
    ignorable_keys = set()
    resource_count = 0

    logger.info("🔍 Starting Analysis for calibration... \n\n")

    for resource in helm_manifest:
        if not resource:
            continue

        kind = resource.get("kind", "Unknown")
        name = resource.get("metadata", {}).get("name", "Unknown")

        logger.info(f"Checking drift for {kind} `{name}`...")

        live_resource = get_k8s_resource(kind, name, namespace)
        if not live_resource:
            logger.warning(f"Resource {kind} `{name}` not found during calibration")
            continue

        helm_key_values = extract_deepest_keys_values(
            extract_relevant_data(resource, None)
        )
        live_key_values = extract_deepest_keys_values(
            extract_relevant_data(live_resource, None)
        )

        helm_key_values = {
            f"{kind};{name};{key}": value for key, value in helm_key_values.items()
        }
        live_key_values = {
            f"{kind};{name};{key}": value for key, value in live_key_values.items()
        }

        ignorable_keys.update(
            set(helm_key_values.keys()).symmetric_difference(
                set(live_key_values.keys())
            )
        )
        resource_count += 1

    logger.info(
        f"\n\nAnalyzed {resource_count} resources and found {len(ignorable_keys)} drift-prone keys.\n"
    )

    return list(ignorable_keys)


def remove_nested_keys(data: Any, keys_to_ignore: Set[str]) -> Any:
    """
    Recursively removes ignored keys from a nested dictionary or list.
    If removing a key results in an empty dict or list, remove the parent key too.

    Args:
        data (Any): The data to clean.
        keys_to_ignore (Set[str]): The keys to ignore.

    Returns:
        Any: Cleaned data with ignored keys removed.
    """

    def pop_nested_keys(d: Any, key_path: str):
        if "metadata.annotations" in key_path:
            keys = key_path.split(".annotations.", 1)
            if len(keys) == 2:
                annotations_path, annotation_key = keys
                keys = annotations_path.split(".") + ["annotations", annotation_key]
        else:
            keys = key_path.split(".")

        current = d
        parents = []

        for i, key in enumerate(keys):
            if "[" in key and "]" in key:
                key_name, index_part = key.split("[", 1)
                index = int(index_part.rstrip("]"))

                if isinstance(current, dict) and key_name in current:
                    parents.append((current, key_name))
                    current = current[key_name]

                if isinstance(current, list) and 0 <= index < len(current):
                    parents.append((current, index))
                    if i == len(keys) - 1:
                        current.pop(index)
                    else:
                        current = current[index]
                else:
                    return
            elif isinstance(current, dict):
                parents.append((current, key))
                if key in current:
                    if i == len(keys) - 1:
                        del current[key]
                    else:
                        current = current[key]

        for parent, key in reversed(parents):
            if isinstance(parent, dict) and key in parent and parent[key] in ({}, []):
                del parent[key]
            elif (
                isinstance(parent, list)
                and isinstance(key, int)
                and 0 <= key < len(parent)
            ):
                if isinstance(parent[key], (dict, list)) and not parent[key]:
                    parent.pop(key)

    for key in keys_to_ignore:
        pop_nested_keys(data, key)

    return data


def extract_relevant_data(
    resource: Dict[str, Any], ignorable_keys: List[str], no_cal_file: bool = False
) -> Dict[str, Any]:
    """
    Extracts relevant data from a Kubernetes resource.

    Args:
        resource (Dict[str, Any]): The Kubernetes resource.
        ignorable_keys (List[str]): The keys to ignore.
        no_cal_file (bool): Flag to disable calibration file.

    Returns:
        Dict[str, Any]: The extracted data.
    """
    kind = resource.get("kind", "Unknown")
    data = resource.get("data", {})
    spec = resource.get("spec", {})

    if not ignorable_keys:
        return data if kind in ["ConfigMap", "Secret"] else spec

    kind_ignorable_keys = {}
    split_num = 1 if no_cal_file else 2

    for resource_kind in SUPPORTED_KINDS:
        kind_ignorable_keys[resource_kind] = [
            key.split(";", split_num)[split_num]
            for key in ignorable_keys
            if key.startswith(f"{resource_kind};")
        ]

    if kind in kind_ignorable_keys:
        keys_to_ignore = set(kind_ignorable_keys[kind])
        if kind in ["ConfigMap", "Secret"]:
            return remove_nested_keys(data, keys_to_ignore)
        return remove_nested_keys(spec, keys_to_ignore)

    return resource

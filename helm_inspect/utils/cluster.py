"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import subprocess
import yaml
from typing import Any, Dict, List

from helm_inspect.utils.logger import setup_logger

logger = setup_logger()


def run_command(command: List[str]) -> str:
    """
    Run a shell command and return its output.

    Args:
        command (List[str]): The command to run as a list of strings.

    Returns:
        str: The standard output from the command.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """

    try:
        valid_commands = ["kubectl", "helm"]

        if not any(cmd in command[0] for cmd in valid_commands):
            raise ValueError(f"Invalid command: {command[0]}")

        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running command: {' '.join(command)}")
        logger.error(f"Output: {e.stderr.strip()}")
        return ""


def get_cluster_name() -> str:
    """
    Retrieve the current Kubernetes cluster name.

    Returns:
        str: The name of the current Kubernetes cluster or "unknown_cluster" if an error occurs.
    """

    output = run_command(
        ["kubectl", "config", "view", "--minify", "-o", "jsonpath={.clusters[0].name}"]
    )
    return output.strip() or "unknown_cluster"


def get_helm_manifest(release: str, namespace: str) -> List[Dict[str, Any]]:
    """
    Get the manifest of a Helm release.

    Args:
        release (str): The name of the Helm release.
        namespace (str): The namespace of the Helm release.

    Returns:
        List[Dict[str, Any]]: The manifest of the Helm release as a list of dictionaries.
    """

    output = run_command(["helm", "get", "manifest", release, "-n", namespace])
    try:
        return list(yaml.safe_load_all(output)) if output else []
    except yaml.YAMLError:
        logger.error("Failed to parse Helm manifest YAML.")
        return []


def get_k8s_resource(kind: str, name: str, namespace: str) -> Dict[str, Any]:
    """
    Get a Kubernetes resource in JSON format.

    Args:
        kind (str): The kind of the Kubernetes resource (e.g., pod, service).
        name (str): The name of the Kubernetes resource.
        namespace (str): The namespace of the Kubernetes resource.

    Returns:
        Dict[str, Any]: The Kubernetes resource as a dictionary.
    """

    output = run_command(
        ["kubectl", "get", kind.lower(), name, "-n", namespace, "-o", "json"]
    )
    try:
        return json.loads(output) if output else {}
    except json.JSONDecodeError:
        logger.error(f"Failed to parse {kind} `{name}` JSON.")
        return {}

![Logo](docs/assets/logo.webp)

Helm Inspect helps you track and detect drift between your Helm manifests and the actual deployed resources—without any complicated setup. It provides a drift check for Helm charts, uses a calibration model for precise drift detection, and sends Slack notifications on detected drifts.

## Table of Contents

- [Options](#options)
- [Installation](#installation)
- [Calibration - Ignoring System-Generated Keys](#calibration---ignoring-system-generated-keys)
- [Detecting Helm Drifts](#detecting-helm-drifts)
- [Strict Mode (Detect All Changes)](#strict-mode-detect-all-changes)
- [Slack Integration](#slack-integration)
- [Command Summary](#command-summary)
- [Features](#features)
- [License](#license)

---

## Options

| **Option**        | **Short** | **Description**                                                           |
| ----------------- | --------- | ------------------------------------------------------------------------- |
| `--release`       | `-r`      | Helm release name (Required).                                             |
| `--namespace`     | `-n`      | Kubernetes namespace (Required).                                          |
| `--calibrate`     | `-c`      | Captures system-generated keys after a fresh Helm install.                |
| `--no-ignore`     | `-I`      | Disables ignoring system-generated keys for strict drift detection.       |
| `--verbose`       | `-v`      | Enables verbose logging (debug mode).                                     |
| `--slack-channel` |           | Slack channel to post drift results (can use `HI_SLACK_CHANNEL` env var). |
| `--slack-token`   |           | Slack bot token (can use `HI_SLACK_BOT_TOKEN` env var).                   |

---

## Installation

> [!NOTE]
> Ensure you have **Python 3.8+**, [Kubectl](https://kubernetes.io/docs/tasks/tools/) and [Helm](https://helm.sh/docs/intro/install/) installed.

HelmInspect is a lightweight CLI tool to detect Helm drifts instantly. Install it via pip:

```sh
pip install helm-inspect
```

---

## Calibration - Ignoring System-Generated Keys

After every **Helm install**, Kubernetes automatically adds some system-generated keys that **should not** be considered as drifts. To account for these, run:

```sh
helm-inspect -r <release-name> -n <namespace> -c
```

<details>
<summary> Example </summary>

**Command**

```sh
helm-inspect -r my-release -n production -c
```

This assumes the current state is a **fresh installation**, identifies system-added keys, and stores them in a temporary ignore list.

**Output**

```sh
[INFO] ✅ Calibration data deleted successfully.
[INFO] 🔍 Starting Analysis for calibration...

[INFO] Checking drift for Secret `myrelease-secret`...
[INFO] Checking drift for ConfigMap `myrelease-configmap`...
[INFO] Checking drift for Service `myrelease-service`...
[INFO] Checking drift for Deployment `myrelease-deployment`...
[INFO] Checking drift for Ingress `myrelease-ingress`...

[INFO] Analyzed 5 resources and found 22 drift-prone keys.
[INFO] ✅ Calibration data saved successfully.
```

</details>

---

## Detecting Helm Drifts

To check for configuration drifts, simply run:

```sh
helm-inspect -r <release-name> -n <namespace>
```

<details>
<summary> Example </summary>

**Command**

```sh
helm-inspect -r my-release -n production
```

**Output**

```sh
[INFO] ✨ Using existing calibration data.

[INFO] Checking drift for Secret `myrelease-secret`...
[INFO] ✅ No drift detected in Secret `myrelease-secret`.

[INFO] Checking drift for ConfigMap `myrelease-configmap`...
[ERROR] ❌ Drift detected in ConfigMap `myrelease-configmap`:
--- Helm Manifest
+++ Live Kubernetes
@@ -1,3 +1,3 @@
 {
-  "custom.conf": "\nserver {\n    listen 80;\n    server_name localhost;\n}\n"
+  "custom.conf": "\nserver {\n    listen 8000;\n    server_name localhost;\n}\n"
}

[INFO] Checking drift for Service `myrelease-service`...
[INFO] ✅ No drift detected in Service `myrelease-service`.
[INFO] ✅ Drift data saved successfully.
```

</details>

This will:

- Compare the deployed Helm manifest with the actual Kubernetes resources.
- Show differences in **CLI output** (like a `diff`).
- Store a **JSON report** in a temp directory.

---

## Strict Mode (Detect All Changes)

By default, HelmInspect ignores system-generated keys. To **disable** this behavior and see _every_ difference:

```sh
helm-inspect -r <release-name> -n <namespace> -I
```

<details>
<summary> Example </summary>

**Command**

```sh
helm-inspect -r my-release -n production -I
```

**Output**

```sh
[INFO] Checking drift for ConfigMap `myrelease-configmap`...
[ERROR] ❌ Drift detected in ConfigMap `myrelease-configmap`:
--- Helm Manifest
+++ Live Kubernetes
@@ -1,3 +1,3 @@
 {
-  "custom.conf": "\nserver {\n    listen 80;\n    server_name localhost;\n}\n"
+  "custom.conf": "\nserver {\n    listen 8000;\n    server_name localhost;\n}\n"
}

[INFO] Checking drift for Secret `myrelease-secret`...
[ERROR] ❌ Drift detected in Secret `myrelease-secret`:
--- Helm Manifest
+++ Live Kubernetes
@@ -1,3 +1,3 @@
 {
-  "authToken": "abcd1234"
+  "authToken": "efgh5678"
}
```

</details>

This mode is useful if you suspect hidden or untracked changes.

---

## Slack Integration

Automate drift notifications to Slack:

```sh
helm-inspect -r <release-name> -n <namespace> --slack-token <token> --slack-channel <channel>
```

<details>
<summary> Example </summary>

**Command**

```sh
helm-inspect -r my-release -n production --slack-token xoxb-123456 --slack-channel SLACKCHANNELID
```

**Output**

```sh
[INFO] ✅ Drift data saved successfully.
✨ Slack Notification Sent!
```

</details>

This sends drift reports **directly to your team’s Slack channel**, keeping everyone updated.

---

## Command Summary

| **Command**                                                                                | **Description**                            |
| ------------------------------------------------------------------------------------------ | ------------------------------------------ |
| `helm-inspect -r <release> -n <namespace> -c`                                              | Calibrate to ignore system-generated keys. |
| `helm-inspect -r <release> -n <namespace>`                                                 | Detect drifts and show differences.        |
| `helm-inspect -r <release> -n <namespace> -I`                                              | Strict mode (show all changes).            |
| `helm-inspect -r <release> -n <namespace> --slack-token <token> --slack-channel <channel>` | Send drift reports to Slack.               |

---

## Features

- **Drift Detection**: Compare Helm manifests with actual Kubernetes resources.
- **Calibration**: Ignore system-generated keys for precise drift detection.
- **Strict Mode**: Detect all changes, including hidden or untracked ones.
- **Slack Integration**: Send drift reports directly to your team’s Slack channel.
- **Lightweight**: No complicated setup or dependencies—just install and run.
- **Open Source**: Available under the Apache Version 2.0 License.

---

## License

HelmInspect is released under the Apache Version 2.0 License.

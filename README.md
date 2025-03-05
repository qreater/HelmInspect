```
______  __      ______                     ________                                      _____
___  / / /_____ ___  /_______ ___          ____  _/_______ ________________ _____ _________  /_  
__  /_/ / _  _ \__  / __  __ `__ \          __  /  __  __ \__  ___/___  __ \_  _ \_  ___/_  __/
_  __  /  /  __/_  /  _  / / / / /         __/ /   _  / / /_(__  ) __  /_/ //  __// /__  / /_
/_/ /_/   \___/ /_/   /_/ /_/ /_/          /___/   /_/ /_/ /____/  _  .___/ \___/ \___/  \__/ 
                                                                   /_/                         

```

HelmInspect is a tool designed to monitor and detect manual changes in Helm manifests, ensuring consistency and integrity in Helm deployments. It does not apply fixes but provides visibility into drift.

## Features
- Monitors and detects manual changes in Helm manifests.
- Provides a **drift check** for Helm charts.
- Uses a **calibration model** for precise drift detection.
- Tracks **historical data** of changes for better insights.
- Sends **Slack notifications** on detected drifts.
- Offers a **readability-focused report** for better understanding.


## Installation

### Prerequisites
Ensure you have **Python 3.8+**, [Kubernetes](https://kubernetes.io/releases/download/), [Helm](https://helm.sh/docs/intro/quickstart/) and [Poetry](https://python-poetry.org/docs/#installation) installed.

### Setup

1. Install dependencies using Poetry:
   ```sh
   poetry install
   ```
2. Activate the virtual environment:
   ```sh
   poetry shell
   ```

## Usage
You can run the tool using:
```sh
poetry run Helm-Inspect <release-name>
```

### Arguments
- `release-name`: The name of the Helm release to inspect.

### Options
| Option            | Description |
|-------------------|-------------|
| `--release`      | The name of the Helm release. |
| `--namespace` | Kubernetes namespace of the release. |
| `--calibrate`     | Calibrate HelmInspect to capture system-generated keys after a fresh Helm installation |
| `--no-ignore`     |Disable key ignoring for strict drift detection (shows all differences including system-generated keys)|

### Example Commands

Inspect a drift in a Helm release named `my-release`:
```sh
poetry run helm-inspect my-release
```

Inspect a drift in a Helm release named `my-release` in the `my-namespace` namespace:
```sh
poetry run helm-inspect my-release --namespace my-namespace
```

Calibrate HelmInspect to capture system-generated keys after a fresh Helm installation:
```sh
poetry run helm-inspect my-release --calibrate
```

Disable key ignoring for strict drift detection:
```sh
poetry run helm-inspect my-release --no-ignore
```



## License

HelmInspect is released under the MIT License.


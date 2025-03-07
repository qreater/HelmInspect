"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import os
from pathlib import Path


HI_SLACK_CHANNEL = os.getenv("HI_SLACK_CHANNEL")
"""
Slack channel to post drift detection results.

This can be set using the `--slack-channel` flag or the `HI_SLACK_CHANNEL` environment variable.
"""

HI_SLACK_BOT_TOKEN = os.getenv("HI_SLACK_BOT_TOKEN")
"""
Slack Bot Token.

This can be set using the `--slack-token` flag or the `HI_SLACK_BOT_TOKEN` environment variable.
"""

SLACK_FILE_UPLOAD_GET_URL = "https://slack.com/api/files.getUploadURLExternal"
"""
Slack API URL for getting the file upload URL.
"""

SLACK_FILE_UPLOAD_COMPLETE_URL = "https://slack.com/api/files.completeUploadExternal"
"""
Slack API URL for completing the file upload.
"""

SLACK_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
"""
Slack API URL for posting messages.
"""

BASE_DIR: Path = (
    Path.home() / ".helminspect"
    if "HI_BASE_DIR" not in os.environ
    else Path(os.environ["HI_BASE_DIR"])
)
"""
Base directory for Helm Inspect.

This can be set using the `HI_BASE_DIR` environment variable.
"""

TMP_DIR = BASE_DIR / "tmp"
"""
Temporary directory for Helm Inspect.
"""

DRIFT_DIR = BASE_DIR / "drift"
"""
Directory to store drift data.
"""

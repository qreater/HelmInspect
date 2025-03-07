"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import requests
import json

from helm_inspect.utils.constant import (
    SLACK_FILE_UPLOAD_GET_URL,
    SLACK_FILE_UPLOAD_COMPLETE_URL,
    SLACK_MESSAGE_URL,
)
from helm_inspect.utils.logger import setup_logger

logger = setup_logger()


def send_slack_notification_with_attachment(
    slack_token: str, slack_channel: str, message: str, file_data: dict
) -> None:
    """
    Send a notification to a Slack channel with a file attachment.

    Args:
        slack_token (str): Slack API token.
        slack_channel (str): Slack channel to send the message to.
        message (str): Message to send.
        file_data (dict): The drift report (JSON) to send as an attachment.
    """
    file_content = json.dumps(file_data, indent=2)
    file_length = len(file_content.encode("utf-8"))

    file_upload_url, file_id = get_file_upload_url(slack_token, file_length)
    if not file_upload_url or not file_id:
        return

    if not upload_file_to_slack(file_upload_url, slack_token, file_content):
        return

    ts_id = post_message_to_slack(slack_token, slack_channel, message)
    if not ts_id:
        return

    complete_file_upload(slack_token, slack_channel, file_id, ts_id)


def get_file_upload_url(slack_token: str, file_length: int) -> tuple[str, str]:
    """
    Get the file upload URL from Slack.

    Args:
        slack_token (str): Slack API token.
        file_length (int): Length of the file content.

    Returns:
        tuple: File upload URL and file ID.
    """
    headers = {"Authorization": f"Bearer {slack_token}"}
    file_meta = {"filename": "drift_report.json", "length": file_length}

    response = requests.post(SLACK_FILE_UPLOAD_GET_URL, headers=headers, data=file_meta)
    if response.status_code != 200 or not response.json().get("ok"):
        logger.error(
            f"❌ Failed to get file upload URL: {response.json().get('error', 'Unknown error')}"
        )
        return None, None

    return response.json().get("upload_url"), response.json().get("file_id")


def upload_file_to_slack(
    file_upload_url: str, slack_token: str, file_content: str
) -> bool:
    """
    Upload the file to Slack.

    Args:
        file_upload_url (str): URL to upload the file.
        slack_token (str): Slack API token.
        file_content (str): Content of the file.

    Returns:
        bool: True if the file was uploaded successfully, False otherwise.
    """
    headers = {"Authorization": f"Bearer {slack_token}"}
    file_upload_params = {"filename": "drift_report.json"}

    response = requests.post(
        file_upload_url, headers=headers, params=file_upload_params, data=file_content
    )
    if response.status_code != 200:
        logger.error(
            f"❌ Failed to upload file: {response.json().get('error', 'Unknown error')}"
        )
        return False

    return True


def post_message_to_slack(slack_token: str, slack_channel: str, message: str) -> str:
    """
    Post a message to a Slack channel.

    Args:
        slack_token (str): Slack API token.
        slack_channel (str): Slack channel to send the message to.
        message (str): Message to send.

    Returns:
        str: Timestamp ID of the posted message.
    """
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }
    message_meta = {"channel": slack_channel, "blocks": message}

    response = requests.post(SLACK_MESSAGE_URL, headers=headers, json=message_meta)
    if response.status_code != 200 or not response.json().get("ok"):
        logger.error(
            f"❌ Failed to send Slack notification: {response.json().get('error', 'Unknown error')}"
        )
        return None

    return response.json().get("ts")


def complete_file_upload(
    slack_token: str, slack_channel: str, file_id: str, ts_id: str
) -> None:
    """
    Complete the file upload process by attaching the file to the message thread.

    Args:
        slack_token (str): Slack API token.
        slack_channel (str): Slack channel to send the message to.
        file_id (str): ID of the uploaded file.
        ts_id (str): Timestamp ID of the posted message.
    """
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    file_complete_meta = {
        "files": json.dumps([{"id": file_id, "title": "Drift Report"}]),
        "channel_id": slack_channel,
        "thread_ts": ts_id,
    }

    response = requests.post(
        SLACK_FILE_UPLOAD_COMPLETE_URL, headers=headers, json=file_complete_meta
    )
    if response.status_code != 200 or not response.json().get("ok"):
        logger.error(
            f"❌ Failed to complete file upload: {response.json().get('error', 'Unknown error')}"
        )
    else:
        logger.info("✨ Slack notification sent successfully.")


def build_slack_message(
    drift_meta: dict, release: str, namespace: str, cluster: str
) -> str:
    """
    Build the Slack message payload.

    Args:
        drift_meta (dict): Drift detection metadata.
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.

    Returns:
        str: JSON string of the Slack message payload.
    """
    drift_detected = drift_meta["drift_summary"]["total_drifts"] > 0

    message = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 Helm Drift Anomaly Report",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Release:* `{release}`"},
                {"type": "mrkdwn", "text": f"*Namespace:* `{namespace}`"},
                {"type": "mrkdwn", "text": f"*Cluster:* `{cluster}`"},
                {
                    "type": "mrkdwn",
                    "text": "*Drift Status:* Detected!"
                    if drift_detected
                    else "*Drift Status:* Clean",
                },
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Total Drifts Detected:* {drift_meta['drift_summary']['total_drifts']}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*New Keys Detected:* {drift_meta['drift_summary']['new_keys']}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Missing Keys Detected:* {drift_meta['drift_summary']['removed_keys']}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Changed Keys Detected:* {drift_meta['drift_summary']['modified_keys']}",
                },
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Drift Report Attached Below!"},
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "© 2025 @Qreater | <https://github.com/qreater|GitHub>",
                }
            ],
        },
    ]

    return json.dumps(message)


def post_slack_message(
    drift_meta: dict,
    release: str,
    namespace: str,
    cluster: str,
    slack_channel: str,
    slack_token: str,
) -> None:
    """
    Post a drift detection summary to a Slack channel with an attachment.

    Args:
        drift_meta (dict): Drift detection metadata.
        release (str): The release name.
        namespace (str): The namespace of the release.
        cluster (str): The cluster name.
        slack_channel (str): Slack channel to post the message to.
        slack_token (str): Slack API token.
    """
    drift_report = drift_meta.get("drift_reports", {})
    message = build_slack_message(drift_meta, release, namespace, cluster)
    send_slack_notification_with_attachment(
        slack_token, slack_channel, message, drift_report
    )

import json
import random
from datetime import datetime
from os import getenv
from typing import List, Tuple

import urllib3


def generate_roster(members: List[str]) -> Tuple[str, List[str]]:
    """
    Generate a roster of members in random order, selecting one as the chosen
    """
    random.seed(datetime.now().microsecond)
    random_roster = members.copy()
    random.shuffle(random_roster)
    chosen = random.choice(members)

    return chosen, random_roster


def render_roster(chosen: str, roster: List[str], render_chosen: bool) -> str:
    """
    Render the roster as a markdown string
    """
    roster = [f"\t{name}\n" for name in roster]

    output = (
        "Roster:\n"
        f"{''.join(roster)}"
    )
    if render_chosen:
        output = f"Chosen: {chosen}\n\n{output}"
    return output


def get_slack_body(body_text):
    return {"text": body_text}


def get_rocket_body(body_text):
    return {
        "username": "slack-random-roster",
        "icon_emoji": ":robot:",
        "text": body_text,
    }


def get_ms_teams_body(body_text):
    return {"text": body_text}


def post(webhook, body):
    http = urllib3.PoolManager()
    exit_code = {
        "statusCode": 200,
        "body": "Success",
    }

    try:
        response = http.request(
            "POST",
            webhook,
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        if response.status != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status, response.data)
            )

    except Exception as e:
        exit_code["statusCode"] = 500
        exit_code["body"] = (
            f"Other Exception: {str(e)}"
            f" (input argument of --url_hook : {webhook})"
        )

    return exit_code


def lambda_handler(event, context):
    exit_code = {
        "statusCode": 200,
        "body": "Success",
    }

    members = getenv("TEAM_ROSTER", default=None)
    render_chosen = getenv("RENDER_CHOSEN", default=False)
    renders = [
        {"url": getenv("SLACK_WEBHOOK_URL", default=None), "render": get_slack_body},
        {"url": getenv("ROCKET_WEBHOOK_URL", default=None), "render": get_rocket_body},
        {"url": getenv("MS_TEAMS_WEBHOOK_URL", default=None), "render": get_ms_teams_body},
    ]

    if members:
        members = members.split(",")
    else:
        return exit_code

    chosen, roster = generate_roster(members)
    roster_output = render_roster(chosen, roster, render_chosen)

    for render in renders:
        if render["url"]:
            body = render["render"](roster_output)
            exit_code = post(render["url"], body)

    return exit_code


if __name__ == "__main__":
    lambda_handler("a", "b")

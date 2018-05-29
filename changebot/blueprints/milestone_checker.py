from flask import current_app

from .pull_request_checker import pull_request_check


MISSING_MESSAGE = 'This pull request has no milestone set.'
PRESENT_MESSAGE = 'This pull request has a milestone set.'


@pull_request_check
def process_milestone(pr_handler, repo_handler):
    """
    A very simple set a failing status if the milestone is not set.
    """
    if not repo_handler.get_config_value("check_milestone", False):
        return [], None

    fail_message = repo_handler.get_config_value("milestone_checker", {}).get("missing_message", MISSING_MESSAGE)
    pass_message = repo_handler.get_config_value("milestone_checker", {}).get("present_message", PRESENT_MESSAGE)

    if not repo_handler.get_config_value('post_pr_comment', False):
        if not pr_handler.milestone:
            pr_handler.set_status('failure', fail_message, current_app.bot_username + ": milestone")
        else:
            pr_handler.set_status('success', pass_message, current_app.bot_username + ": milestone")

        return [], None

    else:
        if not pr_handler.milestone:
            return [fail_message], False
        else:
            return [], True

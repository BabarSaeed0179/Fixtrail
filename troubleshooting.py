
"""
FixTrail troubleshooting decision engine.

This module contains the built-in troubleshooting questions and weighted rules.
It is designed to work with gui.py, which calls:

    analyze_answers(category, answers, custom_rules)

The function returns:
    (diagnosis, decision_score, recommended_solution)

The Decision Score is a rule-based comparison, not a probability or a
guarantee that the selected diagnosis is correct.
"""

from collections.abc import Mapping, Sequence
from typing import Any


# Each question is displayed by the GUI in this exact order.
# Each rule refers to its question text and the answer that activates it.
CATEGORIES = {
    "Wi-Fi": {
        "questions": [
            "Is Airplane Mode enabled on your device?",
            "Is Wi-Fi switched off on your device?",
            "Can other devices connect to the same Wi-Fi network?",
            "Are you connected to Wi-Fi but unable to open websites?",
        ],
        "rules": [
            {
                "question": "Is Airplane Mode enabled on your device?",
                "expected_answer": "Yes",
                "diagnosis": "Airplane Mode is preventing a Wi-Fi connection",
                "weight": 50,
                "solution": (
                    "Turn off Airplane Mode, make sure Wi-Fi is enabled, "
                    "and try connecting to the network again."
                ),
            },
            {
                "question": "Is Wi-Fi switched off on your device?",
                "expected_answer": "Yes",
                "diagnosis": "Wi-Fi is disabled on the device",
                "weight": 55,
                "solution": (
                    "Enable Wi-Fi in your device's network settings, select "
                    "the correct network, and reconnect."
                ),
            },
            {
                "question": "Can other devices connect to the same Wi-Fi network?",
                "expected_answer": "No",
                "diagnosis": "The router or internet connection may be unavailable",
                "weight": 65,
                "solution": (
                    "Check the router's power and status lights. If permitted, "
                    "restart the router by following the provider's instructions. "
                    "If other devices still cannot connect, contact the network "
                    "administrator or internet provider."
                ),
            },
            {
                "question": "Are you connected to Wi-Fi but unable to open websites?",
                "expected_answer": "Yes",
                "diagnosis": "The connection may have a DNS or internet access issue",
                "weight": 60,
                "solution": (
                    "Try opening another website and reconnecting to the network. "
                    "If the issue continues, restart the device and contact the "
                    "network administrator to check internet and DNS settings."
                ),
            },
        ],
        "fallback": (
            "No specific Wi-Fi fault was identified. Check that Wi-Fi is enabled, "
            "confirm that you selected the correct network, move closer to the "
            "router, and restart your device. Contact IT support if the issue remains."
        ),
    },

    "Printer": {
        "questions": [
            "Is the printer displaying an offline status?",
            "Is there a paper jam or paper-out warning?",
            "Is the printer's USB or network connection disconnected?",
            "Are print jobs stuck in the print queue?",
        ],
        "rules": [
            {
                "question": "Is the printer displaying an offline status?",
                "expected_answer": "Yes",
                "diagnosis": "The printer is offline or unavailable",
                "weight": 60,
                "solution": (
                    "Make sure the printer is powered on and connected to the "
                    "same network or computer. Check its display for warnings, "
                    "then try printing a test page."
                ),
            },
            {
                "question": "Is there a paper jam or paper-out warning?",
                "expected_answer": "Yes",
                "diagnosis": "The printer has a paper feed problem",
                "weight": 70,
                "solution": (
                    "Follow the printer manufacturer's instructions to remove "
                    "jammed paper safely or refill the paper tray. Close all "
                    "covers securely before printing again."
                ),
            },
            {
                "question": "Is the printer's USB or network connection disconnected?",
                "expected_answer": "Yes",
                "diagnosis": "The printer connection is disconnected",
                "weight": 65,
                "solution": (
                    "Reconnect the USB cable or check that the printer is joined "
                    "to the correct Wi-Fi or network. Avoid forcing connectors."
                ),
            },
            {
                "question": "Are print jobs stuck in the print queue?",
                "expected_answer": "Yes",
                "diagnosis": "A stuck print queue may be blocking new jobs",
                "weight": 55,
                "solution": (
                    "Open the printer queue, review pending jobs, and cancel "
                    "the stuck job if appropriate. Restart the printer and "
                    "send a small test document."
                ),
            },
        ],
        "fallback": (
            "No specific printer fault was identified. Check power, paper, ink or "
            "toner warnings, and the cable or network connection. Restart the "
            "printer and try a test page. Contact IT support if it remains unavailable."
        ),
    },

    "Slow Computer": {
        "questions": [
            "Is the available storage space nearly full?",
            "Does the computer become faster after closing unused applications?",
            "Does the computer take unusually long to start?",
            "Is CPU or memory usage consistently high?",
        ],
        "rules": [
            {
                "question": "Is the available storage space nearly full?",
                "expected_answer": "Yes",
                "diagnosis": "Low available storage may be affecting performance",
                "weight": 60,
                "solution": (
                    "Review storage usage and remove only files or applications "
                    "you recognise and no longer need. Empty the recycle bin or "
                    "trash if appropriate. Do not delete system files."
                ),
            },
            {
                "question": "Does the computer become faster after closing unused applications?",
                "expected_answer": "Yes",
                "diagnosis": "Too many running applications may be using system resources",
                "weight": 55,
                "solution": (
                    "Close applications that are not needed and avoid opening "
                    "many resource-intensive programs at the same time."
                ),
            },
            {
                "question": "Does the computer take unusually long to start?",
                "expected_answer": "Yes",
                "diagnosis": "Startup applications or background processes may be slowing boot time",
                "weight": 50,
                "solution": (
                    "Review startup applications and disable only non-essential "
                    "items you recognise. Restart the computer and check whether "
                    "startup time improves."
                ),
            },
            {
                "question": "Is CPU or memory usage consistently high?",
                "expected_answer": "Yes",
                "diagnosis": "A process may be using excessive CPU or memory",
                "weight": 65,
                "solution": (
                    "Use Task Manager or Activity Monitor to identify applications "
                    "using unusually high resources. Save your work before closing "
                    "an application, and ask IT support about unfamiliar processes."
                ),
            },
        ],
        "fallback": (
            "No specific performance issue was identified. Restart the computer, "
            "close applications you are not using, and check available storage. "
            "If the computer remains slow, record when the slowdown occurs and "
            "contact IT support."
        ),
    },

    "Login": {
        "questions": [
            "Does the account display a locked-account message?",
            "Does the system reject the password as incorrect?",
            "Could Caps Lock or the keyboard layout be incorrect?",
            "Are you unable to receive the password-reset email?",
        ],
        "rules": [
            {
                "question": "Does the account display a locked-account message?",
                "expected_answer": "Yes",
                "diagnosis": "The account may be locked",
                "weight": 70,
                "solution": (
                    "Wait for the organisation's lockout period or contact the "
                    "IT administrator to request an account unlock. Do not keep "
                    "repeating login attempts."
                ),
            },
            {
                "question": "Does the system reject the password as incorrect?",
                "expected_answer": "Yes",
                "diagnosis": "The supplied login credentials may be incorrect",
                "weight": 55,
                "solution": (
                    "Check the username and enter the password carefully. If it "
                    "still fails, use the organisation's official password-reset "
                    "process. Never share your password with anyone."
                ),
            },
            {
                "question": "Could Caps Lock or the keyboard layout be incorrect?",
                "expected_answer": "Yes",
                "diagnosis": "Keyboard settings may be changing the entered password",
                "weight": 60,
                "solution": (
                    "Check Caps Lock, Num Lock where relevant, and the selected "
                    "keyboard language. Re-enter the password carefully."
                ),
            },
            {
                "question": "Are you unable to receive the password-reset email?",
                "expected_answer": "Yes",
                "diagnosis": "The password-reset email may be delayed or misdirected",
                "weight": 50,
                "solution": (
                    "Check the junk or spam folder and confirm that you are using "
                    "the correct registered email address. If the email does not "
                    "arrive, contact the organisation's IT support team."
                ),
            },
        ],
        "fallback": (
            "No specific login issue was identified. Check the username, keyboard "
            "settings, and internet connection. Use only the official password-reset "
            "process or contact IT support. Never share your password."
        ),
    },
}


def _validate_rule(rule: Mapping[str, Any], rule_number: int) -> None:
    """Check that a built-in or administrator-created rule is usable."""
    required_fields = (
        "question",
        "expected_answer",
        "diagnosis",
        "weight",
        "solution",
    )

    missing_fields = [
        field for field in required_fields
        if field not in rule or rule[field] is None
    ]
    if missing_fields:
        raise ValueError(
            f"Troubleshooting rule {rule_number} is missing: "
            + ", ".join(missing_fields)
        )

    for field in ("question", "diagnosis", "solution"):
        if not isinstance(rule[field], str) or not rule[field].strip():
            raise ValueError(
                f"Troubleshooting rule {rule_number} has an invalid {field}."
            )

    if rule["expected_answer"] not in ("Yes", "No"):
        raise ValueError(
            f"Troubleshooting rule {rule_number} must expect 'Yes' or 'No'."
        )

    # bool is a subclass of int in Python, so reject it explicitly.
    weight = rule["weight"]
    if isinstance(weight, bool) or not isinstance(weight, int) or weight < 1:
        raise ValueError(
            f"Troubleshooting rule {rule_number} must have a positive whole-number weight."
        )


def analyze_answers(
    category: str,
    answers: Sequence[str],
    custom_rules: Sequence[Mapping[str, Any]] | None = None,
) -> tuple[str, float, str]:
    """
    Match answers against built-in and administrator-added rules.

    The answers must follow the same order as the built-in questions,
    followed by the custom questions supplied in custom_rules.

    The rule with the highest weight is selected. If multiple rules match,
    the Decision Score is:

        selected rule weight / total weight of matching rules * 100

    If weights are equal, the first matching rule is selected.
    """
    if category not in CATEGORIES:
        raise ValueError(f"Unknown troubleshooting category: {category!r}.")

    if isinstance(answers, (str, bytes)) or not isinstance(answers, Sequence):
        raise ValueError("Answers must be a list or tuple of Yes/No values.")

    if custom_rules is None:
        custom_rules = []

    if isinstance(custom_rules, (str, bytes)) or not isinstance(custom_rules, Sequence):
        raise ValueError("Custom rules must be provided as a list or tuple.")

    built_in_questions = CATEGORIES[category]["questions"]
    expected_answer_count = len(built_in_questions) + len(custom_rules)

    if len(answers) != expected_answer_count:
        raise ValueError(
            f"{category} requires {expected_answer_count} answers, "
            f"but {len(answers)} were provided."
        )

    for answer_number, answer in enumerate(answers, start=1):
        if answer not in ("Yes", "No"):
            raise ValueError(
                f"Answer {answer_number} must be 'Yes' or 'No'."
            )

    # Pair every rule with its question position. This avoids ambiguity if an
    # administrator creates a question whose wording duplicates a built-in one.
    indexed_rules = []

    for rule in CATEGORIES[category]["rules"]:
        _validate_rule(rule, len(indexed_rules) + 1)
        try:
            question_index = built_in_questions.index(rule["question"])
        except ValueError as error:
            raise ValueError(
                f"A built-in rule refers to an unknown question: {rule['question']!r}."
            ) from error
        indexed_rules.append((question_index, rule))

    for custom_number, custom_rule in enumerate(custom_rules, start=1):
        if not isinstance(custom_rule, Mapping):
            raise ValueError(
                f"Custom rule {custom_number} must be a dictionary-like object."
            )
        _validate_rule(custom_rule, len(indexed_rules) + 1)
        # The GUI appends custom questions after all built-in questions.
        question_index = len(built_in_questions) + custom_number - 1
        indexed_rules.append((question_index, custom_rule))

    matching_rules = []

    for rule_number, (question_index, rule) in enumerate(indexed_rules, start=1):
        _validate_rule(rule, rule_number)
        if answers[question_index] == rule["expected_answer"]:
            matching_rules.append(rule)

    if not matching_rules:
        return (
            "No specific problem identified",
            0.0,
            CATEGORIES[category]["fallback"],
        )

    # max() keeps the first rule when two matching rules have equal weights.
    selected_rule = max(matching_rules, key=lambda item: item["weight"])
    total_matching_weight = sum(rule["weight"] for rule in matching_rules)

    decision_score = (
        selected_rule["weight"] / total_matching_weight
    ) * 100

    return (
        selected_rule["diagnosis"],
        decision_score,
        selected_rule["solution"],
    )

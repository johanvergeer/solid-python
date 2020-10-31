import logging
from smtplib import SMTP_SSL
from ssl import create_default_context
from pathlib import Path
from typing import List, Set

from attr import dataclass

from python_solid_principles.ordinal import ordinal

logger = logging.getLogger(__name__)


def get_input(text: str) -> str:
    return input(text)


@dataclass
class User:
    email: str
    password: str


def send_email(
    formatted_content: str, sender: User, receiver_email_addresses: Set[str]
) -> None:
    context = create_default_context()
    port = 465

    with SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender.email, sender.password)
        server.sendmail(sender.email, receiver_email_addresses, formatted_content)


def format_to_plain_text(lines: List[str]) -> str:
    return "\n".join(lines)


def read_lines_from_file(file_path: Path) -> List[str]:
    logger.info(f"Trying to read file: '{file_path}'")

    with file_path.open() as f:
        return f.read().splitlines()


def get_sender_data() -> User:
    sender_email = get_input("Type your email: ")
    sender_password = get_input("Type your password: ")

    return User(sender_email, sender_password)


def _get_receiver_email_address_message(current_email_addresses_count: int) -> str:
    message = f"{ordinal(current_email_addresses_count + 1)} receiver email address"

    if current_email_addresses_count > 0:
        message += " (or press enter to continue)"

    message += ": "

    return message


def get_receiver_email_addresses() -> Set[str]:
    receiver_mail_addresses = set()
    while (
        len(
            username := get_input(
                _get_receiver_email_address_message(len(receiver_mail_addresses))
            ).strip()
        )
        > 0
    ):
        receiver_mail_addresses.add(username)

    return receiver_mail_addresses


def get_input_file_path() -> Path:
    return Path(get_input("Enter file name: "))


def send_file_to_email():
    lines = read_lines_from_file(get_input_file_path())
    send_email(
        formatted_content=format_to_plain_text(lines),
        sender=get_sender_data(),
        receiver_email_addresses=get_receiver_email_addresses(),
    )


if __name__ == "__main__":
    send_file_to_email()

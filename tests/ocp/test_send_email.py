from pathlib import Path
from unittest.mock import patch

import pytest

from python_solid_principles.ocp.send_email import (
    format_to_plain_text,
    read_lines_from_file,
    User,
    get_sender_data,
    get_receiver_email_addresses,
    send_email,
    SMTP_SSL,
)


def test_get_file_path():
    pass


@pytest.mark.parametrize(
    "lines,expected_text",
    [
        ([], ""),
        (["first line"], "first line"),
        (["first line", "second line"], "first line\nsecond line"),
    ],
)
def test_format_to_plain_text(lines, expected_text):
    assert format_to_plain_text(lines) == expected_text


class TestReadLinesFromFile:
    def test_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            read_lines_from_file(Path() / "non_existing_file.txt")

    @pytest.mark.parametrize(
        "file_content,expected_lines",
        [
            ("", []),
            ("some text", ["some text"]),
            ("some text\nsecond line", ["some text", "second line"]),
        ],
    )
    def test_read_lines_from_file(self, file_content, expected_lines, tmp_path):
        file_path = tmp_path / "testfile.txt"
        with file_path.open("w+") as test_file:
            test_file.writelines(file_content)

        assert read_lines_from_file(file_path) == expected_lines


@patch("python_solid_principles.ocp.send_email.get_input")
def test_get_sender_data(get_input_mock):
    # GIVEN the user should enter the email address first
    # AND the password should be entered second
    get_input_mock.side_effect = ["johan@test.com", "1234"]

    # WHEN the sender data is requested
    sender_data = get_sender_data()

    # THEN the email and password were requested from the user
    get_input_mock.assert_any_call("Type your email: ")
    get_input_mock.assert_any_call("Type your password: ")

    # AND a User with the correct info is returned
    assert sender_data == User("johan@test.com", "1234")


@pytest.mark.parametrize(
    "expected_email_addresses",
    [
        pytest.param(["receiver@test.com"], id="Single receiver address"),
        pytest.param([], id="No receiver addresses"),
        pytest.param(
            ["receiver_1@example.com", "receiver_2@example.com"],
            id="Multiple receiver addresses",
        ),
    ],
)
def test_get_receiver_email_addresses(expected_email_addresses):
    with patch("python_solid_principles.ocp.send_email.get_input") as get_input_mock:
        # GIVEN the user will enter the sender email addresses
        # AND presses enter once the last email address was entered
        entered_values = expected_email_addresses + ["\n"]
        get_input_mock.side_effect = entered_values

        # WHEN getting the receiver email addresses
        email_addresses = get_receiver_email_addresses()

        # THEN the user was asked to enter the first receiver email address
        get_input_mock.assert_any_call("1st receiver email address: ")
        # AND when the user entered the first value he is asked for a second value
        if len(expected_email_addresses) > 1:
            get_input_mock.assert_any_call(
                "2nd receiver email address (or press enter to continue): "
            )

        # AND the entered receiver email addresses should be returned
        assert email_addresses == set(expected_email_addresses)


@pytest.fixture
def ssl_context_mock(mocker):
    context_mock = mocker.Mock(name="context_mock")
    mocker.patch(
        "python_solid_principles.ocp.send_email.create_default_context",
        return_value=context_mock,
    )
    return context_mock


@pytest.fixture
def smtp_ssl_mock(mocker, ssl_context_mock):
    smtp_ssl_mock = mocker.MagicMock(name="smtp_ssl_mock", spec=SMTP_SSL)
    mocker.patch("python_solid_principles.ocp.send_email.SMTP_SSL", new=smtp_ssl_mock)
    return smtp_ssl_mock


def test_send_email(ssl_context_mock, smtp_ssl_mock):
    # GIVEN a context mock
    # AND an SMTP_SSL mock
    # AND some content to send, a sender and a set of receivers
    formatted_content = "Some content"
    sender = User("johan@example.com", "1234")
    receiver_email_addresses = {"receiver_1@example.com"}

    # WHEN sending the email
    send_email(formatted_content, sender, receiver_email_addresses)

    # THEN the gmail smtp server is used on port 465 with the ssl context
    smtp_ssl_mock.assert_called_with("smtp.gmail.com", 465, context=ssl_context_mock)
    # AND the user is logged in, in order to send the email
    context_manager_mock = smtp_ssl_mock.return_value.__enter__
    context_manager_mock.return_value.login.assert_called_with(
        sender.email, sender.password
    )
    context_manager_mock.return_value.sendmail.assert_called_with(
        sender.email, receiver_email_addresses, formatted_content
    )

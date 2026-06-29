from app.ui.validation import RequiredArgumentsValidator


def test_required_arguments_validator_fails_when_missing_arguments():
    validator = RequiredArgumentsValidator(1)

    result = validator.validate(())

    assert result.valid is False
    assert result.message == "Expected at least 1 argument(s)."


def test_required_arguments_validator_passes_when_argument_present():
    validator = RequiredArgumentsValidator(1)

    result = validator.validate(("file.txt",))

    assert result.valid is True
    assert result.message == ""


def test_required_arguments_validator_accepts_more_than_minimum():
    validator = RequiredArgumentsValidator(2)

    result = validator.validate(("a", "b", "c"))

    assert result.valid is True
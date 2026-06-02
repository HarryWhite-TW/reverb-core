from elysia_core.input.preprocess import preprocess_input


def as_escape(text):
    return text.encode("unicode_escape").decode()


def summarize_case(label, value):
    result = preprocess_input(value)
    error_codes = [error.code for error in result.errors]
    event_names = [event.name for event in result.events]

    print(f"Case: {label}")
    print(f"  input: {value!r}")
    print(f"  processed_text_escape: {as_escape(result.processed_text)}")
    print(f"  is_valid: {result.is_valid}")
    print(f"  errors: {error_codes}")
    print(f"  events: {event_names}")
    print(f"  correlation_id_present: {bool(result.correlation_id)}")
    print(f"  correlation_id_length: {len(result.correlation_id)}")
    print()


def main():
    cases = [
        ("valid symbol normalization", "What!!??"),
        ("empty / whitespace fallback", "   "),
        ("unexpected type guard", None),
    ]

    for label, value in cases:
        summarize_case(label, value)


if __name__ == "__main__":
    main()

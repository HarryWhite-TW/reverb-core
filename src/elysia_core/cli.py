import sys
import json
from elysia_core.input.preprocess import preprocess_input

def main():

    args = sys.argv[1:]

    if not args:
        args = [""]

    use_json = False

    if args[0] == "--json":
        use_json = True
        args = args[1:]

    text = " ".join(args)

    result = preprocess_input(text)

    if use_json:
        output = {
            "processed_text": result.processed_text,
            "is_valid": result.is_valid,
            "errors": [e.code for e in result.errors],
            "events": [
                {
                    "name": ev.name,
                    "changed": ev.changed,
                    "severity": ev.severity
                }
                for ev in result.events
            ],
            "correlation_id": result.correlation_id,
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print("Processed:", result.processed_text)
        print("Valid:", result.is_valid)
        print("Errors:", [e.code for e in result.errors])
        print("Correlation ID:", result.correlation_id)
        print("Events:")
        for ev in result.events:
            print(f"- {ev.name} (changed={ev.changed}, severity={ev.severity})")
            ##實際演示:- strip_spaces (changed=False, severity=info)

if __name__ == "__main__":#只有當這個檔案被直接執行時，才呼叫 main()
    main()                #如果它被 import，main() 不會自動跑。
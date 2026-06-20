def main():
    try:
        with open("HelloWorld-test1.in", "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        import sys
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)

    print("Hello World!")

    # Print file content without extra newline
    # (end="" prevents print from adding another newline)
    print(content, end="")

if __name__ == "__main__":
    main()
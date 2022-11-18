def panic(error_msg):
    print(error_msg, file=sys.stderr)
    exit(1)

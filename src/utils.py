def color_text(color: str, text: str) -> str:
    colors = {
        "red": "\033[1;31m",
        "green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "blue": "\033[1;34m",
        "cyan": "\033[1;36m",
        "white": "\033[0m",
    }

    color_code = colors.get(color.lower(), colors["white"])
    print(f"{color_code}{text}{colors['white']}")


def resume(args):
    if args.http_method:
        http_method = ' http method: ' + args.http_method + ','
    color_text(
        'cyan', f'target: {args.target}, port: {args.port}, attack: {args.attack},{http_method} packet number: {args.count if args.count else "Infinite"}\n')

import logging

from .main import QemyCLI

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(name)s] [%(levelname)s] %(message)s"
    )
    # Start CLI with logging off
    logging.disable(logging.CRITICAL + 1)

    QemyCLI().run()

if __name__ == '__main__':
    main()

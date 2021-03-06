import logging
import sys

from project.handlers.backup import backup_postgres_handler

# * Setting up logger *#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main(arg):
    # * If the provided argument is backup then we will make a logical backup of the database. *#
    if arg == "backup":
        backup_postgres_handler(logger)
    else:
        logger.error("Invalid argument provided. Please provide a valid one.")
        sys.exit(1)


if __name__ == "__main__":
    # * Error if no arguments are provided. *#
    if len(sys.argv) != 2:
        logger.error("Please provide a valid argument.")
        sys.exit(1)

    # * Run the main function with user provided arguments *#
    main(sys.argv[1].lower())

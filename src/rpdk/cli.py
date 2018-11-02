"""This tool provides support for creating CloudFormation resource providers.
"""
import argparse
import logging
from logging.config import dictConfig

from .data_loaders import resource_yaml
from .generate import setup_subparser as generate_setup_subparser
from .init import setup_subparser as init_setup_subparser
from .project_settings import setup_subparser as project_settings_setup_subparser
from .test import setup_subparser as test_setup_subparser
from .validate import setup_subparser as validate_setup_subparser


def setup_logging(verbosity=0):
    """Configure logging with a variable verbosity level (0, 1, 2)."""
    if verbosity > 1:
        level = logging.DEBUG
    elif verbosity > 0:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging_config = resource_yaml(__name__, "data/logging/logging.yaml")
    logging_config["handlers"]["console"]["level"] = level
    dictConfig(logging_config)


def main(args_in=None):
    """The entry point for the CLI."""
    # see docstring of this file
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase the output verbosity. Can be specified multiple times.",
    )

    # the default command just prints the help message
    # subparsers should set their own default commands
    parser.set_defaults(command=lambda args: parser.print_help())

    subparsers = parser.add_subparsers(dest="subparser_name")
    init_setup_subparser(subparsers)
    validate_setup_subparser(subparsers)
    generate_setup_subparser(subparsers)
    project_settings_setup_subparser(subparsers)
    test_setup_subparser(subparsers)
    args = parser.parse_args(args=args_in)

    setup_logging(args.verbose)
    args.command(args)


if __name__ == "__main__":
    main()
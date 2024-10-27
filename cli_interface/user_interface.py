# cli_interface/user_interface.py

import argparse
import sys
import os
from .message_maker import MessageMaker

class UserInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="CLI tool to generate and manage commit messages."
        )
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument(
            '--message-template',
            choices=['complex', 'simple'],
            default='simple',
            help='Select the commit message template complexity.'
        )

        subparsers = self.parser.add_subparsers(dest='command', help='Commands')

        # Commit command
        commit_parser = subparsers.add_parser('commit', help='Generate and commit a message.')
        
        # Filter command
        filter_parser = subparsers.add_parser('filter', help='Filter commit history.')
        filter_parser.add_argument('--impact-type', type=str, help='Filter by impact type.')
        filter_parser.add_argument('--change-type', type=str, help='Filter by change type.')

        # Help flag is automatically handled by argparse

    def parse_args(self):
        return self.parser.parse_args()

    def display_commit_message(self, commit_message):
        print(f"\nGenerated commit message:\n{commit_message}")

    def prompt_user_action(self):
        return input("\nDo you want to (a)ccept this message, (r)egenerate, or (q)uit? ").lower()

    def prompt_feedback(self):
        return input("Please provide feedback for regeneration (or press Enter to skip): ")

    def show_error(self, message):
        print(f"Error: {message}", file=sys.stderr)
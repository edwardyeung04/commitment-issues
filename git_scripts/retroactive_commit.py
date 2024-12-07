import os
import subprocess
import sys
import logging
from cli_interface.message_maker import MessageMaker

class RetroactiveCommit:
    def __init__(self):
        self.message_maker = MessageMaker()

    def generate_commit_message(self):
        # Get a list of commit hashes
        commit_hashes = subprocess.check_output(
            ['git', 'rev-list', '--reverse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().split()

        # Set GIT_SEQUENCE_EDITOR to automatically pick all commits
        env = os.environ.copy()
        env['GIT_SEQUENCE_EDITOR'] = 'sed -i -e "s/^pick /edit /"'

        # Start an interactive rebase silently
        subprocess.run(
            ['git', 'rebase', '-i', '--root'],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        for commit_hash in commit_hashes:
            # Extract the diff for the commit
            diff = subprocess.check_output(['git', 'show', commit_hash], stderr=subprocess.DEVNULL).decode()

            # Extract old commit message for reference
            old_message = subprocess.check_output(
                ['git', 'log', '-1', '--pretty=%s', commit_hash],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Generate a new commit message
            new_message = self.message_maker.generate_message(diff)

            # Set commit author/committer dates (not strictly necessary, but preserving from original code)
            try:
                env['GIT_COMMITTER_DATE'] = subprocess.check_output(
                    ['git', 'log', '-1', '--format=%cD', commit_hash],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                env['GIT_AUTHOR_DATE'] = subprocess.check_output(
                    ['git', 'log', '-1', '--format=%aD', commit_hash],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
            except subprocess.CalledProcessError:
                logging.warning(f"Could not retrieve dates for commit {commit_hash}. Using current date/time.")

            if new_message:
                # Print the summary of what we're doing for this commit
                print(f"Amending commit {commit_hash}")
                print(f"Old message: {old_message}")
                print(f"New message: {new_message}\n")

                # Amend the commit silently
                subprocess.run(
                    ['git', 'commit', '--amend', '-m', new_message],
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            else:
                print(f"No new message generated for {commit_hash}, skipping amendment.\n")

            # Continue the rebase silently
            subprocess.run(
                ['git', 'rebase', '--continue'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

        print("All commits have been updated with new messages.")
        print("To apply these changes to your remote repository, use:\n")
        print("    git push --force\n")
        print("Note: Force pushing rewrites history on the remote repository, so ensure this is safe to do.")

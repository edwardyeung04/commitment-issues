import subprocess
from cli_interface.message_maker import MessageMaker

class RetroactiveCommit:
    def __init__(self):
        self.message_maker = MessageMaker()

    def generate_commit_message(self):
        # Get a list of commit hashes
        commit_hashes = subprocess.check_output(['git', 'rev-list', 'HEAD']).decode().split()

        for commit_hash in commit_hashes:
            # Extract the diff for the commit if not provided
            diff = subprocess.check_output(['git', 'show', commit_hash]).decode()
            
            # Generate a commit message using the MessageMaker
            new_message = self.message_maker.generate_message(diff)
            
            # Amend the commit with the new message
            subprocess.run(['git', 'commit', '--amend', '-m', new_message], env={
                'GIT_COMMITTER_DATE': subprocess.check_output(['git', 'log', '-1', '--format=%cD', commit_hash]).decode().strip(),
                'GIT_AUTHOR_DATE': subprocess.check_output(['git', 'log', '-1', '--format=%aD', commit_hash]).decode().strip(),
            })
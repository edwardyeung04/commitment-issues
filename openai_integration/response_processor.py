# openai_integration/response_processor.py

import re

class ResponseProcessor:
    def __init__(self):
        pass

    def process_response(self, raw_response):
        if not raw_response:
            return None

        # Remove any leading/trailing whitespace
        response_text = raw_response.strip()

        # Define a regex pattern to match the commit message format
        pattern = r"^\s*(?P<ChangeType>feat|feature|bugfix|fix|refactor|docs|doc|test|tests|chore)\s*\|\s*(?P<ImpactArea>[\w\s]+):\s*(?P<TLDR>.+?)(?:\n|$)"

        match = re.match(pattern, response_text, re.IGNORECASE)

        if not match:
            print("Generated commit message does not match the required format.")
            print("Response from GPT:\n", response_text)
            return None

        # Extract the summary components
        change_type = match.group('ChangeType').strip().lower()
        impact_area = match.group('ImpactArea').strip().lower()
        tldr = match.group('TLDR').strip()

        # Normalize ChangeType
        change_type_mapping = {
            'feat': 'feature',
            'fix': 'bugfix',
            'doc': 'docs',
            'tests': 'test',
        }
        change_type = change_type_mapping.get(change_type, change_type)

        # Build the commit message
        lines = response_text.split('\n', 1)
        if len(lines) > 1:
            # There is a detailed description
            detailed_description = lines[1].strip()
            commit_message = f"{change_type} | {impact_area}: {tldr}\n\n{detailed_description}"
        else:
            # No detailed description
            commit_message = f"{change_type} | {impact_area}: {tldr}"

        return commit_message

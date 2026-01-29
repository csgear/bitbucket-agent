import os
import sys
from atlassian import Bitbucket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BitbucketPRAgent:
    def __init__(self):
        self.url = os.getenv('BITBUCKET_URL')
        self.username = os.getenv('BITBUCKET_USERNAME')
        self.password = os.getenv('BITBUCKET_PASSWORD')
        self.project_key = os.getenv('BITBUCKET_PROJECT_KEY')
        self.verify_ssl = os.getenv('BITBUCKET_VERIFY_SSL', 'True').lower() == 'true'

        if not all([self.url, self.username, self.password, self.project_key]):
            print("Error: Missing environment variables. Please check your .env file.")
            sys.exit(1)

        if not self.verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.bitbucket = Bitbucket(
            url=self.url,
            username=self.username,
            password=self.password,
            verify_ssl=self.verify_ssl
        )

    def create_pull_request(self, repo_slug, title, source_branch, destination_branch='master', description='', reviewers=None):
        """
        Creates a Pull Request in Bitbucket Server.
        """
        try:
            print(f"Attempting to create PR in {repo_slug}: '{title}' from {source_branch} to {destination_branch}...")

            pr_response = self.bitbucket.open_pull_request(
                source_project=self.project_key,
                source_repo=repo_slug,
                dest_project=self.project_key,
                dest_repo=repo_slug,
                source_branch=source_branch,
                destination_branch=destination_branch,
                title=title,
                description=description,
                reviewers=reviewers if reviewers else []
            )

            # The structure of the response depends on the library and API version,
            # but usually it returns a dict representing the PR.
            if 'links' in pr_response and 'self' in pr_response['links']:
                pr_url = pr_response['links']['self'][0]['href']
                print(f"Successfully created PR: {pr_url}")
            else:
                # Fallback if URL extraction fails but no exception was raised
                print("PR created successfully.")
                print(pr_response)

            return pr_response

        except Exception as e:
            print(f"Failed to create PR: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    agent = BitbucketPRAgent()

    # You would typically gather these from args or another source
    # For demonstration, we'll hardcode or look for args
    if len(sys.argv) < 4:
        print("Usage: python create_pr.py <repo_slug> <title> <source_branch> [destination_branch]")
        sys.exit(1)

    repo_slug = sys.argv[1]
    title = sys.argv[2]
    source_branch = sys.argv[3]
    destination_branch = sys.argv[4] if len(sys.argv) > 4 else 'master'

    agent.create_pull_request(repo_slug, title, source_branch, destination_branch)

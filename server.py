from mcp.server.fastmcp import FastMCP
from create_pr import BitbucketPRAgent
import os

# Initialize FastMCP server
mcp = FastMCP("bitbucket-pr-agent")

# Initialize the Bitbucket agent
# Ensure environment variables are loaded (BitbucketPRAgent does this via dotenv)
try:
    bb_agent = BitbucketPRAgent()
except SystemExit:
    # If env vars are missing, BitbucketPRAgent exits.
    # In an MCP context, we might want to fail gracefully or log an error,
    # but for now, we'll let it be potentially noisy or handle it inside the tool.
    bb_agent = None


@mcp.tool()
def create_bitbucket_pr(repo_slug: str, title: str, source_branch: str, destination_branch: str = "master", description: str = "") -> str:
    """
    Create a Pull Request in the configured Bitbucket Server repository.

    Args:
        repo_slug: The slug of the repository where the PR will be created.
        title: The title of the pull request.
        source_branch: The name of the branch to merge from.
        destination_branch: The name of the branch to merge into (default: master).
        description: The description of the pull request.
    """
    if not bb_agent:
        return "Error: Bitbucket agent not initialized. Check server logs and environment variables."

    result = bb_agent.create_pull_request(
        repo_slug=repo_slug,
        title=title,
        source_branch=source_branch,
        destination_branch=destination_branch,
        description=description
    )

    if result:
        # Try to extract the link again for the return message
        if isinstance(result, dict) and 'links' in result and 'self' in result['links']:
            return f"PR Created Successfully: {result['links']['self'][0]['href']}"
        if isinstance(result, dict):
            return f"PR Created Successfully. ID: {result.get('id', 'Unknown')}"
        return "PR Created Successfully."
    else:
        return "Failed to create PR. Check server logs for details."


if __name__ == "__main__":
    mcp.run()

mcp-name: io.github.csgear/bitbucket-agent


# Bitbucket PR Agent (MCP Server)


This is an MCP (Model Context Protocol) server that allows AI agents to create Pull Requests in a self-hosted Bitbucket Server instance.

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration:**
    Copy `.env.example` to `.env` and fill in your details:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` with your Bitbucket URL, credentials, project key, and repository slug.

## running the Server

You can test the server locally by running:

```bash
python server.py
```

(Note: Standard MCP servers communicate over stdio, so running this directly in a terminal will just wait for input).

## Integration with MCP Clients (e.g., Claude Desktop, VS Code with MCP)

To use this with an MCP-compliant client, you need to configure it to run this python script.

**Example `claude_desktop_config.json`:**

```json
{
  "mcpServers": {
    "bitbucket-agent": {
      "command": "python",
      "args": ["/absolute/path/to/bitbucket/server.py"],
      "env": {
        "BITBUCKET_URL": "https://bitbucket.yourcompany.com",
        "BITBUCKET_USERNAME": "your_username",
        "BITBUCKET_PASSWORD": "your_password",
        "BITBUCKET_PROJECT_KEY": "PROJ",
        "BITBUCKET_REPO_SLUG": "repo"
      }
    }
  }
}
```

_Note: You can either rely on the `.env` file loading (if the working directory is correct) or pass the environment variables directly in the config as shown above._

## VS Code Configuration

To use this agent with GitHub Copilot (or other MCP-enabled VS Code extensions), you typically need to add the server configuration to your VS Code settings.

1.  Open your **Workspace Settings** (`.vscode/settings.json`) or **User Settings**.
2.  Add the definition for this MCP server. For example:

```json
"github.copilot.mcpServers": {
    "bitbucket-agent": {
        "command": "python",
        "args": [
            "${workspaceFolder}/server.py"
        ],
        "env": {
             "BITBUCKET_URL": "https://bitbucket.yourcompany.com",
             "BITBUCKET_USERNAME": "your_username",
             "BITBUCKET_PASSWORD": "your_password",
             "BITBUCKET_PROJECT_KEY": "PROJ",
             "BITBUCKET_REPO_SLUG": "repo"
        }
    }
}
```

> **Note:** Adjust the `${workspaceFolder}/server.py` path if your script is located elsewhere. You may need to use an absolute path if `${workspaceFolder}` is not resolved correctly by your specific extension version.


import subprocess


def get_git_branch():
    try:
        # Run the git command to get the current branch
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()  # Return the branch name
        else:
            return None
    except FileNotFoundError:
        # Git command not found, handle the error
        return None


def get_database_index():
    branch = get_git_branch()
    if branch:
        print("Current branch:", branch)
        if branch == "main":
            return 0
        elif branch == "development":
            return 1
        else:
            raise Exception("invalid git branch. valid branches: 'main' or 'development'.")
    else:
        raise Exception("Unable to determine the current git branch.")


DATABASE_HOST = "localhost"
DATABASE_PORT = 6379
DATABASE_INDEX = get_database_index()

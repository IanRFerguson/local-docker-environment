from pygit2 import Repository


def check_parsons_branch(
    path_to_parsons: str = "/src/parsons",
    dev_branch_name: str = "ianferguson-docker-dev",
):
    live_branch_name = Repository(path=path_to_parsons).head.shorthand

    if not live_branch_name == dev_branch_name:
        raise OSError(
            f"Parsons branch is not set to {dev_branch_name} [currently {live_branch_name}]"
        )

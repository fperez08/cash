import sys

import anyio

import dagger


async def test():
    async with dagger.Connection(
        dagger.Config(log_output=sys.stderr)
    ) as client:
        # get reference to the local project
        src = client.host().directory(".")

        python = (
            client.container()
            .from_("python:3.10-slim-buster")
            # mount cloned repository into image
            .with_mounted_directory("/src", src)
            # set current working directory for next commands
            .with_workdir("/src")
            .with_exec(["python3", "main.py"])
        )

        # execute
        await python.exit_code()

    print("Tests succeeded!")


if __name__ == "__main__":
    anyio.run(test)

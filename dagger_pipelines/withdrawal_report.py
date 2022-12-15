import sys
import anyio
import dagger

from utils import env


async def test():
    async with dagger.Connection(
        dagger.Config(log_output=sys.stderr)
    ) as client:
        src_path = "/src"
        config_files_path = env("CONFIG_FILES_PATH")
        src = client.host().directory(".")
        token = client.host().directory(config_files_path).file("token.json")
        config_file = (
            client.host().directory(config_files_path).file("cash_config.json")
        )
        credentials = (
            client.host().directory(config_files_path).file("credentials.json")
        )
        python = (
            client.container()
            .from_("python:3.10")
            .with_mounted_directory(src_path, src)
            .with_file(src_path, token)
            .with_file(src_path, config_file)
            .with_file(src_path, credentials)
            .with_workdir(src_path)
            .with_env_variable("PYTHONPATH", "${PYTHONPATH}:${PWD}")
            .with_env_variable("CONFIG_PATH", src_path)
            .with_env_variable("CREDENTIALS_PATH", src_path)
            .with_env_variable("TOKEN_PATH", src_path)
            .with_exec(["pip3", "install", "poetry"])
            .with_exec(["poetry", "config", "virtualenvs.create", "false"])
            .with_exec(["poetry", "install", "--without", "test,pipeline,dev"])
            .with_exec(
                [
                    "python3",
                    "main.py",
                    "--label",
                    "withdrawal",
                    "--days",
                    "30",
                ]
            )
        )

        # execute
        await python.exit_code()

    print("Cash run succeeded!")


if __name__ == "__main__":
    anyio.run(test)

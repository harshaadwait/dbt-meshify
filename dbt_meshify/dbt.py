# third party
import os
from typing import Optional, List

try:
    from dbt.cli.main import dbtRunner, dbtRunnerResult
    from dbt.contracts.graph.manifest import Manifest
except ImportError:
    dbtRunner = None

if dbtRunner is not None:
    dbt_runner = dbtRunner()
else:
    dbt_runner = None


class Dbt:
    def __init__(self):
        self.dbt_runner = dbtRunner()

    def invoke(
        self, directory: Optional[os.PathLike] = None, runner_args: Optional[List[str]] = None
    ):
        starting_directory = os.getcwd()
        if directory:
            os.chdir(directory)
        result = self.dbt_runner.invoke(runner_args if runner_args else [])
        os.chdir(starting_directory)

        if not result.success:
            raise result.exception
        return result.result

    def parse(self, directory: os.PathLike):
        return self.invoke(directory, ["--quiet", "parse"])

    def ls(self, directory: os.PathLike, arguments: Optional[List[str]] = None) -> List[str]:
        """
        Execute dbt ls with the given arguments and return the result as a list of strings.
        Log level is set to none to prevent dbt from printing to stdout.
        """
        args = ["--log-format", "json", "--log-level", "none", "ls"]
        if arguments:
            args.extend(arguments)
        return self.invoke(directory, args)

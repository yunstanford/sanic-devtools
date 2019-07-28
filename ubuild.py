import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("coverage")
    build.packages.install("asynctest")
    build.packages.install("pytest-mock")
    build.packages.install("pytest-sanic", version="==1.0.0")
    build.packages.install("pytest-toolbox", version="==0.4")
    build.executables.run([
        "coverage", "run", "--append",
        "--source=sanic_devtools",
        "./bin/pytest", "./tests",
    ] + build.options.args)
    build.executables.run([
        "coverage", "report", "-m"
    ])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload",
    ])
    build.executables.run([
        "twine", "upload", "dist/*"
    ])

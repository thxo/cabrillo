from nox_poetry import session

SRC = "cabrillo"


@session(python=["3.10"])
def test(session):
    session.run(
        "pytest",
        "-vvv",
        # "--cov-report=xml",
        # f"--cov={SRC}",
        external=True,
    )


@session(python=["3.10"])
def lint(session):
    session.run("black", ".", external=True)
    session.run("flake8", SRC, "./tests", external=True)
    session.run("bandit", "-r", SRC, external=True)
    session.run("pylint", SRC, external=True)
    session.run("isort", ".", external=True)

"""Nox configuration file"""

import nox
import os

running_on_ci = os.getenv("CI")

@nox.session
def requirements(session: nox.Session) -> None:
    """
    Regenerate the pinned requirements for running tests and building
    documentation.

    This workflow updates :file:`uv.lock` to contain pinned requirements
    for different versions of Python, different operating systems, and
    different dependency sets (i.e., `docs` or `tests`).

    When run in CI, this session will create a file that contains the
    pull request message for the GitHub workflow that updates the pinned
    requirements (:file:`.github/workflows/update-pinned-reqs.yml`).
    """
    uv_lock_upgrade = ["uv", "lock", "--upgrade", "--no-progress"]

    # When silent is `True`, `session.run()` returns a multi-line string
    # with the standard output and standard error.

    uv_output: str | bool = session.run(
        *uv_lock_upgrade,
        *session.posargs,
        silent=running_on_ci,
    )

    if running_on_ci:
        session.log(uv_output)
        _create_requirements_pr_message(uv_output=uv_output, session=session)


@nox.session
def validate_requirements(session: nox.Session) -> None:
    """
    Verify that the requirements in :file:`uv.lock` are compatible
    with the requirements in `pyproject.toml`.
    """
    session.log(
        "🛡 If this check fails, regenerate the pinned requirements in "
        "`uv.lock` with `nox -s requirements`."
    )

    # Generate the cache without updating uv.lock by syncing the
    # current environment. If there ends up being a `--dry-run` option
    # for `uv sync`, we could probably use it here.

    session.run("uv", "sync", "--frozen", "--all-extras", "--no-progress")

    # Verify that uv.lock will be unchanged. Using --offline makes it
    # so that only the information from the cache is used.

    session.run("uv", "lock", "--check", "--offline", "--no-progress")

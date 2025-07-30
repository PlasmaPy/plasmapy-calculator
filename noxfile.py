"""Nox configuration file"""

import nox
import os
import shutil
import pathlib

running_on_ci = os.getenv("CI")


def _create_requirements_pr_message(uv_output: str, session: nox.Session) -> None:
    """
    Create the pull request message during requirements updates.

    This function copies a GitHub flavored Markdown template to a new
    file and appends a table containing the updated requirements, with
    links to the corresponding PyPI pages. This file is then used as the
    body of the pull request message used in the workflow for updating
    requirements.

    Parameters
    ----------
    uv_output : str
        The multi-line output of ``session.run(..., silent=True)``.
    """

    pr_template = pathlib.Path("./.github/content/update-requirements-pr-template.md")
    pr_message = pathlib.Path("./.github/content/update-requirements-pr-body.md")

    shutil.copy(pr_template, pr_message)

    lines = [
        "",
        "| package | old version | new version |",
        "| :-----: | :---------: | :---------: |",
    ]

    for package_update in uv_output.splitlines():
        if not package_update.startswith("Updated"):
            session.debug(f"Line not added to table: {package_update}")
            continue

        try:
            # An example line is "Updated nbsphinx v0.9.6 -> v0.9.7"
            _, package_, old_version_, _, new_version_ = package_update.split()
        except ValueError:
            session.debug(f"Line not added to table: {package_update}:")
            continue

        old_version = f"{old_version_.removeprefix('v')}"
        new_version = f"{new_version_.removeprefix('v')}"

        pypi_link = f"https://pypi.org/project/{package_}/{new_version}"
        package = f"[`{package_}`]({pypi_link})"

        lines.append(f"| {package} | `{old_version}` | `{new_version}` |")

    with pr_message.open(mode="a") as file:
        file.write("\n".join(lines))


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


@nox.session
def smoke_test(session: nox.Session) -> None:
    session.install(".")
    session.run("plasmapy-calculator")

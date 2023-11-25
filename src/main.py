import sys

from pyflow import Workflow

import utils

ALL = "all"


def main(workflow: Workflow):
    ide = workflow.args[0]
    search = ""

    if len(workflow.args) > 1:
        search = " ".join(workflow.args[1:])

    projects = sorted(
        filter(
            lambda p: search.lower() in p.fullname.lower(),
            filter(
                lambda p: p.ide.name == ide or ide == ALL,
                utils.find_recent_projects(),
            ),
        ),
        key=lambda p: p.updated_at,
        reverse=True,
    )

    for project in projects:
        if not project.ide.installed:
            continue

        title = project.fullname

        if ide == ALL:
            title = f"{project.ide.name} > {title}"

        workflow.new_item(
            title=title,
            subtitle=str(project.path),
            arg=f"open -n {project.ide.app} --args {project.path}",
            valid=True,
        ).set_icon_file(
            path=str(project.icon),
        ).set_alt_mod(
            subtitle="Reveal in Finder...",
            arg=f"open {project.path}",
        ).set_cmd_mod(
            subtitle="Reveal in Finder...",
            arg=f"open {project.path}",
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()

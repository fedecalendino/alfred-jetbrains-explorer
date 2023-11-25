import re
from datetime import datetime
from os.path import expanduser
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from classes import Project

HOME = Path(expanduser("~"))
PATH = HOME / Path("Library/Application Support/JetBrains/")


def check_options_file(ide_name: str, path: Path) -> Iterable[Project]:
    root = ElementTree.parse(path)

    groups = {}

    for group in root.findall(".//ProjectGroup"):
        name = group.find(".//option[@name='name']").attrib["value"]

        for project in group.findall(".//option[@name='projects']/list/option"):
            project_path = project.attrib["value"]
            groups[project_path] = name

    for entry in root.findall(".//entry"):
        project_path = entry.attrib["key"]

        if "$USER_HOME$" not in project_path:
            continue

        project_name = project_path.split("/")[-1]

        ide_code = entry.find(".//option[@name='productionCode']").attrib["value"].lower()
        timestamp = entry.find(".//option[@name='projectOpenTimestamp']")

        if timestamp is None:
            continue

        epoch = timestamp.attrib["value"]
        updated_at = datetime.utcfromtimestamp(int(epoch) // 1000)

        yield Project(
            name=project_name,
            path=project_path,
            ide_name=ide_name,
            ide_code=ide_code,
            updated_at=updated_at,
            group=groups.get(project_path),
        )


def find_recent_projects() -> Iterable[Project]:
    projects = {}

    for item in PATH.iterdir():
        if not item.is_dir():
            continue

        ide_name = re.sub("[^a-zA-Z]", "", item.name)
        xml = item / "options/recentProjects.xml"

        if not xml.exists():
            continue

        for project in check_options_file(ide_name, xml):
            if project.path not in projects:
                projects[project.path] = project
            else:
                if project.updated_at > projects[project.path].updated_at:
                    projects[project.path] = project

    yield from projects.values()

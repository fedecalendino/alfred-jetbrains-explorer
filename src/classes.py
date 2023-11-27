from datetime import datetime
from os.path import expanduser
from pathlib import Path

HOME = Path(expanduser("~"))


class IDE:
    def __init__(self, name: str, code: str):
        self.name: str = name
        self.code: str = code

    @property
    def app(self) -> Path:
        return Path(f"/Applications/{self.name}.app")

    @property
    def icon(self):
        return self.app / Path(f"Contents/Resources/{self.name.lower()}.icns")

    @property
    def installed(self) -> bool:
        return self.app.exists()

    def __repr__(self):
        return self.name


class Project:
    def __init__(
        self,
        name: str,
        path: str,
        ide_name: str,
        ide_code: str,
        updated_at: datetime,
        group: str = None,
    ):
        self.name: str = name
        self.path: str = Path(path.replace("$USER_HOME$", str(HOME)))
        self.ide: IDE = IDE(ide_name, ide_code)
        self.updated_at: datetime = updated_at
        self.group: str = group

    @property
    def fullname(self) -> str:
        if self.group:
            return f"{self.name} ({self.group})"

        return f"{self.name}"

    @property
    def exists(self) -> bool:
        return (self.path / Path(".idea/workspace.xml")).exists()

    @property
    def icon(self) -> Path:
        icon = self.path / Path(".idea/icon.png")

        if not icon.exists():
            icon = self.ide.icon

        return icon

    def __repr__(self):
        return f"{self.name} ({self.ide}) [{self.updated_at}]"

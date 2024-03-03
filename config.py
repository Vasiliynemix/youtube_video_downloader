import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class GoogleConfig:
    auth_file_name: str = os.getenv("GOOGLE_AUTH_FILE_NAME")
    spreadsheet_id: str = os.getenv("SPREADSHEET_ID")
    scopes: list[str] = field(default_factory=lambda: ["https://www.googleapis.com/auth/spreadsheets",
                                                       "https://www.googleapis.com/auth/drive"])


@dataclass
class VideoConfig:
    video_dir_name: str = os.getenv("VIDEO_DIR_NAME")
    video_root_dir: str = os.getenv("VIDEO_ROOT_DIR")


@dataclass
class PathsConfig:
    root_path: str = str(Path(__file__).parent)
    google: GoogleConfig = field(default_factory=GoogleConfig)
    video: VideoConfig = field(default_factory=VideoConfig)

    @property
    def path_to_google_auth_file(self) -> str:
        return os.path.join(self.root_path, self.google.auth_file_name)

    @property
    def path_to_video_dir(self) -> str:
        return os.path.join(self.video.video_root_dir, self.video.video_dir_name)


@dataclass
class Config:
    google: GoogleConfig = field(default_factory=GoogleConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)


cfg = Config()

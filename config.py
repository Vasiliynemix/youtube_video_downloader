import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class GoogleConfig:
    auth_file_name: str = os.getenv("GOOGLE_AUTH_FILE_NAME")
    spreadsheet_id: str = os.getenv("SPREADSHEET_ID")
    scopes: list[str] = ["https://www.googleapis.com/auth/spreadsheets",
                         "https://www.googleapis.com/auth/drive"]


class VideoConfig:
    video_dir_name: str = os.getenv("VIDEO_DIR_NAME")
    video_root_dir: str = os.getenv("VIDEO_ROOT_DIR")


class PathsConfig:
    root_path: str = str(Path(__file__).parent)
    google: GoogleConfig = GoogleConfig
    video: VideoConfig = VideoConfig

    path_to_google_auth_file = os.path.join(root_path, google.auth_file_name)

    path_to_video_dir = os.path.join(video.video_root_dir, video.video_dir_name)


class Config:
    google: GoogleConfig = GoogleConfig
    paths: PathsConfig = PathsConfig


cfg = Config()

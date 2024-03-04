import asyncio

from pytube import YouTube
from config import cfg
from db.db import update_product, db_start, get_product, set_product
from services.sheets import GoogleSheet
from utils import is_valid_url


def download_video(db_conn, article_id, video_url, i):
    print(f"Скачивание {i} видео...")
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').last()
        filename = f"{article_id}.mp4"
        stream.download(output_path=cfg.paths.path_to_video_dir, filename=filename)
        print("Видео успешно скачано!")
        update_product(None, article_id, video_url)
    except Exception as e:
        print(f"Произошла ошибка при скачивании видео: {e}")


async def download_video_async(db_conn, article_id, video_url, i):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, download_video, db_conn, article_id, video_url, i)


async def main():
    db_conn = None
    db_start(db_conn)

    google_sheets = GoogleSheet()

    while True:
        result_info = google_sheets.get_articles_and_youtube_urls(
            cfg.google.spreadsheet_id,
            ['🗄️ Каталог!A:A', '🗄️ Каталог!AO:AO'],
        )

        tasks = []
        for i, (article_id, video_url) in enumerate(result_info, start=1):
            if article_id and video_url:
                if is_valid_url(video_url[0]):
                    product = get_product(db_conn, int(article_id[0]))
                    if product is None:
                        set_product(db_conn, int(article_id[0]), None)
                    else:
                        if product[1] == video_url[0]:
                            continue
                    tasks.append(download_video_async(db_conn, article_id[0], video_url[0], i))

        for task in tasks:
            await task

        print("Sleeping...")
        await asyncio.sleep(20)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
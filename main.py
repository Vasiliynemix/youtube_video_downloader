import asyncio

from asyncpg import Pool
from pytube import YouTube
from config import cfg
from db.db import db_start, set_product, get_product, update_product
from services.sheets import GoogleSheet
from utils import is_valid_url


async def download_video(db_conn: Pool, article_id: str, video_url: str, i: int):
    print(f"Downloading video {i} ({article_id})...")
    try:
        yt = YouTube(video_url)

        stream = yt.streams.filter(progressive=True, file_extension="mp4").last()
        if stream:
            await asyncio.to_thread(stream.download, output_path=cfg.paths.path_to_video_dir, filename=f"{article_id}.mp4")
            print(f"Video {i} ({article_id}) downloaded in {stream.resolution} successfully.")
            await update_product(db_conn, int(article_id), video_url)
            return

    except Exception as e:
        print(f"Error downloading video {i} ({article_id}): {e}")


async def main():
    db_conn = None
    await db_start(db_conn)

    google_sheets = GoogleSheet()

    while True:
        result_info = await google_sheets.get_articles_and_youtube_urls(
            cfg.google.spreadsheet_id,
            ['🗄️ Каталог!A:A', '🗄️ Каталог!AO:AO'],
        )

        tasks = []
        for i, (article_id, video_url) in enumerate(result_info, start=1):
            if article_id and video_url:
                if is_valid_url(video_url[0]):
                    product = await get_product(db_conn, int(article_id[0]))
                    if product is None:
                        await set_product(db_conn, int(article_id[0]), None)
                    else:
                        if product[1] == video_url[0]:
                            continue
                    tasks.append(download_video(db_conn, article_id[0], video_url[0], i))

        await asyncio.gather(*tasks)

        print("Sleeping...")
        await asyncio.sleep(20)

if __name__ == '__main__':
    asyncio.run(main())

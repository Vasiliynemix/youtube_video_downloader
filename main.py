import asyncio
from youtube_dl import YoutubeDL
from config import cfg  # Replace with your config
from db.db import update_product, db_start, get_product, set_product
from services.sheets import GoogleSheet
from utils import is_valid_url


def download_video(db_conn, article_id, video_url, i):
    print(f"Downloading video {i} ({article_id})...")
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f"{cfg.paths.path_to_video_dir}/{article_id}.mp4"
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if info:
                ydl.download([video_url])
                print(f"Video {i} ({article_id}) downloaded successfully.")
                update_product(db_conn, int(article_id), video_url)
                return

    except Exception as e:
        print(f"Error downloading video {i} ({article_id}): {e}")


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
    asyncio.run(main())
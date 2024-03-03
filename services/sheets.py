import httplib2
from asyncpg import Pool
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from config import cfg


class GoogleSheet:
    _credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cfg.paths.path_to_google_auth_file,
        cfg.google.scopes,
    )
    _http_auth = _credentials.authorize(httplib2.Http())
    _service = discovery.build('sheets', 'v4', http=_http_auth)

    def __init__(self):
        pass

    async def get_articles_and_youtube_urls(self, spreadsheet_id: str, ranges):
        response = await self.__fetch_batches(spreadsheet_id, ranges)

        values = response.get('valueRanges', [])

        if len(values) < len(ranges):
            print("Не удалось получить данные из одного из диапазонов.")
            return

        articles = values[0]['values']
        youtube_urls = values[1]['values']

        if not articles or not youtube_urls:
            print("Один из диапазонов ячеек пуст.")
            return

        return zip(articles[1:], youtube_urls[1:])

    async def __fetch_batches(self, spreadsheet_id: str, ranges):
        return self._service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=ranges,
        ).execute()

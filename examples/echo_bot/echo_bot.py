import aiomatrix
import config


async def echo_handler(
        event: aiomatrix.types.events.RoomMessageEvent,
        content: aiomatrix.types.modules.instant_messaging.TextContent,
        client: aiomatrix.AiomatrixClient
):
    await client.instant_messaging_api.send_notice(room_id=event.room_id, text=content.body, reply_to=event.event_id)


async def main():
    storage = aiomatrix.storage.StorageRepo(
        internal_storage=aiomatrix.storage.SqliteInternalDataStorage(db_path=config.db_path),
        events_storage=aiomatrix.storage.SqliteEventStorage(db_path=config.db_path),
        presence_storage=aiomatrix.storage.SqlitePresenceStorage(db_path=config.db_path)
    )
    bot = aiomatrix.AiomatrixClient(
        server_url='https://example.com',
        auth_details=('password', {'login': '@login:example.com', 'password': 'password'}),
    )
    dp = aiomatrix.AiomatrixDispatcher(clients=[bot], data_storage=storage)
    executor = aiomatrix.Executor(dp)
    executor.start_polling(timeout=10, track_presence=False)

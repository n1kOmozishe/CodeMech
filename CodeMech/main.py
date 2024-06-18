import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Bot token'ları ve özel durumlar
bot_configs = [
    {
        'token_key': 'TOKEN1',
        'status': discord.Status.online,
        'activity_type': discord.ActivityType.streaming,
        'activity_name': 'Live on Twitch',
        'activity_url': 'https://www.twitch.tv/your_channel'
    },
    {
        'token_key': 'TOKEN2',
        'status': discord.Status.dnd,  # Do Not Disturb
        'activity_type': discord.ActivityType.listening,
        'activity_name': 'CodeMech'
    },
    {
        'token_key': 'TOKEN3',
        'status': discord.Status.idle,
        'activity_type': discord.ActivityType.watching,
        'activity_name': 'CodeMech'
    },
    {
        'token_key': 'TOKEN4',
        'status': discord.Status.online,
        'activity_type': discord.ActivityType.watching,
        'activity_name': 'Twitch streams'
    },
    {
        'token_key': 'TOKEN5',
        'status': discord.Status.online,
        'activity_type': discord.ActivityType.watching,
        'activity_name': 'Custom Activity'  # Örnek olarak 'Custom Activity' olarak değiştirdim
    },
    {
        'token_key': 'TOKEN6',
        'status': discord.Status.online,
        'activity_type': discord.ActivityType.streaming,
        'activity_name': 'Live on Twitch',
        'activity_url': 'https://www.twitch.tv/your_channel'
    }
]

# Belirli ses kanalının ID'si
VOICE_CHANNEL_ID = os.getenv('VOICE_CHANNEL_ID')

if VOICE_CHANNEL_ID is None:
    raise ValueError("VOICE_CHANNEL_ID is not set in the .env file")

VOICE_CHANNEL_ID = int(VOICE_CHANNEL_ID)

class MyBot(commands.Bot):
    def __init__(self, token, command_prefix, intents, status, activity_type, activity_name, activity_url=None):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.token = token
        self.status = status
        self.activity_type = activity_type
        self.activity_name = activity_name
        self.activity_url = activity_url

    async def on_ready(self):
        print(f'{self.user.name} is online!')
        activity = discord.Activity(
            type=self.activity_type,
            name=self.activity_name,
            url=self.activity_url
        )
        await self.change_presence(status=self.status, activity=activity)

        channel = self.get_channel(VOICE_CHANNEL_ID)
        if channel is not None and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f'{self.user.name} connected to {channel.name}')
        else:
            print(f'{self.user.name} could not find the voice channel with ID {VOICE_CHANNEL_ID}.')

intents = discord.Intents.default()
intents.presences = True  # Presence güncellemelerini almak için
intents.voice_states = True  # Voice state güncellemelerini almak için

async def create_bot(config):
    token = os.getenv(config['token_key'])
    if token is None:
        print(f"Token '{config['token_key']}' is not set in the .env file. Skipping bot creation.")
        return

    bot = MyBot(
        token=token,
        command_prefix='!', 
        intents=intents,
        status=config['status'],
        activity_type=config['activity_type'],
        activity_name=config['activity_name'],
        activity_url=config.get('activity_url')
    )
    await bot.start(token)

async def main():
    while True:
        try:
            tasks = [create_bot(config) for config in bot_configs if os.getenv(config['token_key']) is not None]
            await asyncio.gather(*tasks)
        except discord.LoginFailure:
            print("Login failed. Check your bot token or Discord credentials.")
        except Exception as e:
            print(f"An error occurred: {type(e).__name__}: {e}")

        await asyncio.sleep(60)  # 60 saniye (1 dakika) bekleme süresi

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

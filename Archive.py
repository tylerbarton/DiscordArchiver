import discord
from tqdm import tqdm
import argparse

import Archive

client = discord.Client()
channel = None

# Parser
parser = argparse.ArgumentParser(description='Discord channel scraper')

requiredNamed = parser.add_argument_group('Required arguments:')
requiredNamed.add_argument('-u', '--user', type=str,
                           help='Discord user token.', required=True)
requiredNamed.add_argument('-c', '--channel', type=str,
                           help='ID of the channel to archive. Only the last id of the url is needed.', required=True)
requiredNamed.add_argument('-o', '--output', type=str,
                           help='Output file where the messages will be saved. In the form of *.txt', required=True)

optionalNamed = parser.add_argument_group('Optional arguments:')
optionalNamed.add_argument('-l', '--limit', type=int, default=1000000,
                           help='The limit of the amount of messages to scrape. Default is unlimited.', required=False)

args = parser.parse_args()


def test_connection():
    """
    Prints a success message if the client was successfully initiated.
    """
    if client:
        print('Connection successful.')
        print('Logged into ID: ', client.user.name)
        print('Channel ID: ', args.channel)


def load_channel(channel_id: int):
    """
    Loads and validates the channel
    @:param channel_id ID of the channel to load
    @:return True if channel was successfully loaded, else false.
    :rtype: bool
    """
    Archive.channel = client.get_channel(id=int(channel_id))
    if Archive.channel is None:
        print("Error: This channel does not exist.")
        return False
    print('Channel Name: ', Archive.channel)
    return True


async def scrape_channel(channel: discord.channel):
    """
    Scrapes a channel
    @:param channel The channel object to scrape
    """
    print("Scraping messages... Don't send any messages while scraping!")
    output_dir = open(args.output, 'w')
    with tqdm(leave=True, unit=' messages') as scraped:
        message_count = 0
        async for message in channel.history(limit=args.limit):
            # format the message
            line = "[{}] {}: {}".format(message.created_at, message.author.name, message.content)
            line = line.encode('utf-8', 'ignore')

            # write to output file
            output_dir.write(str(line))
            output_dir.write("\n")

            # update
            message_count += 1
            scraped.update(1)


@client.event
async def on_ready():
    """
    Called when the discord client is ready.
    Will immediately start archiving the targeted channel.
    """
    test_connection()
    if load_channel(channel_id=args.channel):
        await scrape_channel(channel=Archive.channel)
        print('-----')
        print('Archiving complete.')

# ----------------------------
userToken = args.user
client.run(userToken, bot=False)

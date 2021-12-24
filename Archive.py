import discord
from tqdm import tqdm
import argparse

import Archive

client = discord.Client()
channel = None

# Parser
parser = argparse.ArgumentParser(description='Discord channel scraper')

requiredNamed = parser.add_argument_group('Required arguments:')
requiredNamed.add_argument('-c', '--channel', type=str,
                           help='ID of the channel to archive. Only the last id of the url is needed.', required=True)
requiredNamed.add_argument('-o', '--output', type=str,
                           help='Output file where the messages will be saved. In the form of *.txt', required=True)

optionalNamed = parser.add_argument_group('Optional arguments:')
optionalNamed.add_argument('-l', '--limit', type=int,
                           help='The limit of the amount of messages to scrape. Default is unlimited.', required=False)

args = parser.parse_args()


def test_connection():
    """
    Prints a success message if the client was successfully initiated.
    """
    if client:
        print('Connection successful.')
        print('Logged into ID: ', client.user.id)
        print('Channel ID: ', args.channel)



def load_channel(id: int):
    """
    Loads and validates the channel
    @:param id ID of the channel to load
    @:return True if channel was successfully loaded, else false.
    :rtype: bool
    """
    Archive.channel = client.get_channel(id=836056676175446117)
    if Archive.channel is None:
        print("Error: This channel does not exist.")
        return False
    # if Archive.channel.read_message_history:
    #     print("Error: You do not have permission to read this channel's history")
    #     return False
    print('Channel Name: ', client.get_channel(id=836056676175446117))
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
        async for message in channel.history(limit=1000000000):
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
    if load_channel(args.channel):
        await scrape_channel(Archive.channel)
        print('-----')
        print('Archiving complete.')

# ----------------------------
userToken = "NTc4MjI4NzczMzkzMDA2NjA0.X0VP1A.tJ8x-wCYMOxI_GV203asxhVQUvc"
client.run(userToken, bot=False)

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError

# Replace these variables with your own values
api_id = '29597128'
api_hash = 'feea1340241265662aec5d75678e9573'
phone_number = '+917510038270'
group_username = '@speeedyyyyyyyyyy'

usernames = ['Krishbhi', 'Yash_747', 'Boss_swastik']  # List of usernames to add to the group

async def add_members_to_group():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.start(phone_number)
        
        # Get the group entity
        try:
            group_entity = await client.get_entity(group_username)
        except ValueError:
            print(f"Group '{group_username}' not found.")
            return

        # Add members to the group
        for username in usernames:
            try:
                await client(InviteToChannelRequest(group_entity, [username]))
                print(f"Added {username} to the group.")
            except FloodWaitError as e:
                print(f"Flood wait error: {e}")
                return
            except Exception as e:
                print(f"Error adding {username} to the group: {e}")

# Run the function to add members to the group
with client.loop.run_until_complete(add_members_to_group()):
    pass

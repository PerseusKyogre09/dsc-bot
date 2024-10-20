# Discord Bot

## Description
This Discord bot is designed to enhance your server experience with various fun and useful commands. Currently, it has a leveling up system.

## Current Features
- **User Leveling System**: Track user activity in the server and reward them with levels and XP for their engagement.

### Music Functionality (In Progress)
- The bot is currently being enhanced to include a music functionality that allows users to search for and play songs from SoundCloud in voice channels. This feature is under development and will be available soon.
- **Pokédex**: Use the `!pokedex <pokemon_name>` command to fetch and display detailed information about a specific Pokémon, including its height, weight, types, and sprite.

## Future Features
The following features are planned for future updates:

- **Enhanced Music Playback**: Integration with additional music sources and features such as playlists and queue management.
- **Fun Commands**: Add more interactive and fun commands, such as games or trivia.
- **Moderation Tools**: Implement tools for server moderation, including mute, kick, and ban commands.
- **Customizable Prefix**: Allow server admins to set a custom command prefix for the bot.

## Screenshots
![Image](https://imgur.com/J5QFqLX.png)

## Installation
To install and run this bot, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
```bash
cd <project_directory>
```
2. Install the required packages:
```bash
pip install discord.py requests
```
3. Create a .env file and add your Discord bot token:
```
DISCORD_TOKEN=your_token_here
SOUNDCLOUD_CLIENT_ID=your_client_id_here
```
4. Run the bot:
```bash
python bot.py
```

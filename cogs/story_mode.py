import asyncio
import os
import typing
import json

import discord
from discord.ext import commands, vbu

from . import utils


class StoryMode(vbu.Cog):
    def __init__(self, bot, logger_name="StoryMode"):
        super().__init__(bot, logger_name=logger_name)

        self.premade_stories: typing.List[utils.Story]

        # Empty premade stories
        try:
            self.premade_stories[:] = []
        except AttributeError:
            self.premade_stories = []

        # Load premade stories
        story_directory = r".\premade_stories"
        story_directory_list = os.listdir(story_directory)
        for filename in story_directory_list:
            json_data = json.load(filename)
            story = utils.Story.from_json(json_data)
            self.premade_stories.append(story)

    @commands.command(name="play")
    async def _play_command(self, ctx: vbu.Context):
        """
        Play a story mode game.
        """

        if not isinstance(ctx, vbu.SlashContext):
            return await ctx.send(
                f"This command can only be used as a slash command. Please run `/{ctx.command.name}`"
            )

        options = []
        for story in self.premade_stories:
            options.append(
                discord.ui.SelectOption(
                    label=story.start.title, value=story.start.title
                )
            )

        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.SelectMenu(
                    custom_id="STORY_PICKER",
                    options=[options],
                )
            )
        )

        interaction = await ctx.interaction
        interaction.response.send_message(
            "Pick a story", components=components, empheral=True
        )

        check = lambda m: m.author == ctx.author and m.channel == ctx.channel

        try:
            interaction: discord.ComponentInteraction = await self.bot.wait_for(
                "component_interaction", timeout=120.0, check=check
            )
        except asyncio.TimeoutError:
            return await interaction.follow_up.send(
                "You took to long to pick a story. Please try again.", empheral=True
            )
        
        story = next((s for s in self.premade_stories if s.start.title == interaction.component.custom_id), None)
        if story is None:
            return await interaction.follow_up.send(
                "Something wen't wrong, couldn't find that story. Please try again.", empheral=True
            )
        
        await interaction.follow_up.send(story)


def setup(bot: vbu.Bot):
    x = StoryMode(bot)
    bot.add_cog(x)

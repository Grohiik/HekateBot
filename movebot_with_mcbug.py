from Token import mojira_password, mojira_username, bot_token as TOKEN
import discord
import re
from jira import JIRA
from discord.utils import get


regex = re.compile(
    "((mc|mcapi|mcce|mcd|mcl|mcpe|mce|realms|web|bds)-[0-9]+)", re.IGNORECASE
)

client = discord.Client()

hekate_id = 563388386564505620
hekate_join_log_id = 720034217920036974

hekate_extra_id = 715660274937626635
hekate_extra_join_log_id = 715939568590782464

Voicechannel = {}


async def mc_bug(message, issues):
    jira = JIRA(
        server="https://bugs.mojang.com", basic_auth=(mojira_username, mojira_password),
    )

    for issueid in issues[:3]:
        try:
            issue = jira.issue(issueid[0])

            embed = discord.Embed(
                color=0xA7D9FC,
                title=str.upper(issueid[0]),
                description=f"**{issue.fields.summary}**",
                url=f"https://bugs.mojang.com/browse/{issueid[0]}",
            )
            embed.add_field(name="Status", value=issue.fields.status)

            embed.add_field(name="Resolution", value=issue.fields.resolution)

            embed.set_footer(text=f"created: {issue.fields.created[:10]}")

            await message.channel.send(embed=embed)
        except:
            try:
                await message.channel.send(f"{issueid[0]} does not exist")
            except:
                await message.channel.send(f"fuck off {message.author.mention}")


@client.event
async def on_member_join(member):
    if member.guild == client.get_guild(hekate_id):
        await client.get_channel(hekate_join_log_id).send(
            f"Member joined: {member.mention}"
        )

    elif member.guild == client.get_guild(hekate_extra_id):
        await client.get_channel(hekate_extra_join_log_id).send(
            f"Member joined: {member.mention}"
        )


@client.event
async def on_member_remove(member):
    if member.guild == client.get_guild(hekate_id):
        await client.get_channel(hekate_join_log_id).send(
            f"{member.mention} left us ;-;"
        )

    elif member.guild == client.get_guild(hekate_extra_id):
        await client.get_channel(hekate_extra_join_log_id).send(
            f"{member.mention} left us ;-;"
        )


@client.event
async def on_voice_state_update(member, before, after):
    global Voicechannel

    if after.channel and before.channel:
        if (
            after.self_deaf
            and not before.self_deaf
            and before.channel != member.guild.afk_channel
        ):
            await member.move_to(member.guild.afk_channel)
            Voicechannel[member] = before.channel
        elif not after.self_deaf and before.self_deaf and member in Voicechannel:
            await member.move_to(Voicechannel[member])
            Voicechannel.pop(member)
    elif member in Voicechannel:
        Voicechannel.pop(member)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    issues = re.findall(regex, message.content)
    if issues:
        await mc_bug(message, issues)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_resumed():
    print("Reconected as")
    print(client.user.name)
    print(client.user.id)
    print("------")


client.run(TOKEN)

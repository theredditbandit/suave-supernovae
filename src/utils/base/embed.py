import typing as t
from enum import Enum

import disnake


class Emojis(Enum):
    CHECK = ":white_check_mark:"
    CROSS = ":x:"
    WARNING = ":warning:"


class EmbedColors(Enum):
    SUCCESS = 0x22C55E
    ERROR = 0xF43F5E
    WARNING = 0xF59E0B
    PRIMARY = 0x6366f1


class BaseEmbed(disnake.Embed):
    def __init__(
        self,
        usr: disnake.Member | disnake.User,
        title: str | None = None,
        description: str | None = None,
        color: int = EmbedColors.PRIMARY.value,
    ) -> None:
        _color = disnake.colour.Color(color)
        super().__init__(
            title=title,
            description=description,
            color=_color,
            timestamp=disnake.utils.utcnow(),
        )
        self.set_footer(
            text=usr,
            icon_url=usr.avatar.url if usr.avatar else "",
        )


def createEmbed(
    usr: disnake.Member | disnake.User,
    title: str | None = None,
    description: str | None = None,
    type: t.Literal["primary", "success", "error", "warning"] = "primary",
):
    if type == "success":
        color = EmbedColors.SUCCESS.value
    elif type == "error":
        color = EmbedColors.ERROR.value
    elif type == "warning":
        color = EmbedColors.WARNING.value
    else:
        color = EmbedColors.PRIMARY.value
    return BaseEmbed(usr=usr, title=title, description=description, color=color)

async def sendEmbed(inter: disnake.Interaction ,embed: disnake.Embed, first: bool = False, **kwargs: t.Any) -> None:
    try:
        if first:
            await inter.response.send_message(embed=embed, **kwargs)
        else:
            await inter.channel.send(embed=embed, **kwargs)
    except disnake.Forbidden:
        try:
            if first:
                await inter.response.send_message(
                    "Hey, seems like I can't send embeds. Please check my permissions :)",
                    **kwargs
                )
            else:
                await inter.channel.send(
                    "Hey, seems like I can't send embeds. Please check my permissions :)",
                    **kwargs
                )

        except disnake.Forbidden:
            await inter.author.send(
                f"Hey, seems like I can't send any message in {inter.channel.name if inter.channel.name else "**|**"} on {inter.guild.name if inter.guild else ""}\n"  # type: ignore
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
                **kwargs
            )

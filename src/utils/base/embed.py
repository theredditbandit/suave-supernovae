import typing as t
from enum import Enum

import disnake


class Emojis(Enum):
    """
    A class to store emojis
    """

    CHECK = ":white_check_mark:"
    CROSS = ":x:"
    WARNING = ":warning:"


class EmbedColors(Enum):
    """
    A class to store embed colors
    """

    SUCCESS = 0x22C55E
    ERROR = 0xF43F5E
    WARNING = 0xF59E0B
    PRIMARY = 0x6366F1


class BaseEmbed(disnake.Embed):
    """
    A class to create a base embed

    Parameters
    ----------
    usr : disnake.Member | disnake.User
        The user to set the footer to
    title : str, optional
        The title of the embed, by default None
    description : str, optional
        The description of the embed, by default None
    color : int, optional
        The color of the embed, by default EmbedColors.PRIMARY.value
    """

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
    """
    Create an embed

    Parameters
    ----------
    usr : disnake.Member | disnake.User
        The user to set the footer to
    title : str, optional
        The title of the embed, by default None
    description : str, optional
        The description of the embed, by default None
    type : typing.Literal["primary", "success", "error", "warning"], optional
        The type of the embed, by default "primary"

    Returns
    -------
    BaseEmbed
        The created embed
    """
    if type == "success":
        color = EmbedColors.SUCCESS.value
    elif type == "error":
        color = EmbedColors.ERROR.value
    elif type == "warning":
        color = EmbedColors.WARNING.value
    else:
        color = EmbedColors.PRIMARY.value
    return BaseEmbed(usr=usr, title=title, description=description, color=color)


async def sendEmbed(
    inter: disnake.Interaction,
    embed: disnake.Embed,
    first: bool = False,
    **kwargs: t.Any,
) -> None:
    """
    Send an embed

    Parameters
    ----------
    inter : disnake.Interaction
        The interaction to send the embed in
    embed : disnake.Embed
        The embed to send
    first : bool, optional
        Whether to send the message as the first response, by default False

    Raises
    ------
    disnake.Forbidden
        If the bot does not have permissions to send the embed
    """
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
                    **kwargs,
                )
            else:
                await inter.channel.send(
                    "Hey, seems like I can't send embeds. Please check my permissions :)",
                    **kwargs,
                )

        except disnake.Forbidden:
            await inter.author.send(
                f"Hey, seems like I can't send any message in {inter.channel.name if inter.channel.name else "**|**"} on {inter.guild.name if inter.guild else ""}\n"  # type: ignore
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
                **kwargs,
            )

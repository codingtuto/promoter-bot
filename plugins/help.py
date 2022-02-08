import logging
import os
from Config import Messages as tr
from Config import Config as C
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
UPDATES_CHANNEL = C.UPDATES_CHANNEL
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.incoming & filters.command(['start', 'start@Forcesubtele_xobot']))
def _start(client, message):
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               client.send_message(
                   chat_id=message.chat.id,
                   text="Désolé monsieur, vous êtes interdit de m'utiliser. Contactez notre [groupe de support](https://t.me/codingtuto).",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            client.send_message(
                chat_id=message.chat.id,
                text="**Avant d'utiliser ce bot vous devez rejoindre notre canal, si vous quitter le canal vous serez banni par le bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Rejoindre", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            client.send_message(message.chat.id,
                text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
	        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                           InlineKeyboardButton("Notre canal", url="https://t.me/lesrobotsdecodingteam"),
                           InlineKeyboardButton("Groupe", url="https://t.me/codingtuto")
                      ],

                  ]
             ),
        parse_mode="markdown",
        reply_to_message_id=message.message_id
        )
            return
    client.send_message(message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
	reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Notre canal", url="https://t.me/lesrobotsdecodingteam"),
                    InlineKeyboardButton("Groupe", url="https://t.me/codingtuto")
                ],
            ]
        ),
        parse_mode="markdown",
        reply_to_message_id=message.message_id
        )


@Client.on_message(filters.incoming & filters.command(['source_code', 'source_code@promotercodebot']))
def _source_code(client, message):
    client.send_message(message.chat.id,
        text=tr.SC_MSG.format(message.from_user.first_name, message.from_user.id),
	reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Créateur", url="https://t.me/A_liou")
                ],
                [
                    InlineKeyboardButton("Notre canal", url="https://t.me/lesrobotsdecodingteam"),
                    InlineKeyboardButton("Groupe", url="https://t.me/codingtuto")
                ],
                [
                    InlineKeyboardButton("Créateur", url="https://t.me/A_liou")
                ]
            ]
        ),
        parse_mode="markdown",
        reply_to_message_id=message.message_id
        )

@Client.on_message(filters.incoming & filters.command(['help', 'help@promotercodebot']))
def _help(client, message):
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               client.send_message(
                   chat_id=message.chat.id,
                   text="Désolés monsieur vous n'êtes pas autorisé à me démarrer ceci est un ordre des administrateurs.",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            client.send_message(
                chat_id=message.chat.id,
                text="**Vous devez rejoindre notre canal, quitter le canal égale au bannissement du bot !**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Rejoindre", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            client.send_message(
                chat_id=message.chat.id,
                text="Hey ce commande est en privé. \nPour en savoir plus rejoins notre [Groupe](https://t.me/codingtuto).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        disable_notification = True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '-->', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        button = [
            [InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '-->', callback_data = f"help+{pos+1}")
            ],
        ]
    return button

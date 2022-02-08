import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ Rejoignez le canal mentionné et appuyez à nouveau sur le bouton Libérer moi.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Vous êtes reistreint par les administrateurs pour d'autres raisons.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} essaie de se désactiver moi-même mais je ne peux pas le désactiver car je ne suis pas un administrateur dans ce chat, ajoutez-moi à nouveau en tant qu'administrateur.**\n__#Je quitte le groupe...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Avertissement : Ne cliquez pas sur le bouton si vous pouvez parler librement.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              " {} , vous n'êtes pas encore abonné à ma chaîne. Veuillez vous joindre en utilisant le bouton ci-dessous et appuyez sur le bouton Libérez moi pour te libérer.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Abonner au canal", url=channel_url)
                ],
                [
                    InlineKeyboardButton("Libérez moi", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **Je ne suis pas admin dans ce groupe.**\n__faites-moi administrateur avec l'autorisation de bannir et de supprimer des messay et ajoutez-moi à nouveau.\n#Je quitte le groupe...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **Je ne suis pas admin dans ce [canal]({channel_url})**\n__Faîtes-moi admin dans ce canal.\n#Je quitte le groupe...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub", "fsub@promotercodebot", "forcesubscribe@promotercodebot"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe est désactivé avec succès.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Réactiver tous les membres dont le son est désactivé par moi...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Désactiver tous les membres qui sont désactivés par moi.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **Je ne suis pas admin dans ce groupe.**\n__Je ne peux pas réactiver le son des membres car je ne suis pas administrateur dans ce chat, faites-moi administrateur avec autorisation de bannir des membres.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              channel_url = client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          message.reply_text(f"✅ **Forcer l'abonnement est activé**\n__Forcer l'abonnement est activé, tous les membres du groupe doivent s'abonner au  [canal]({channel_url}) avant d'entamer une conversation dans ce groupe.**Devellopée par l'équipe** @codingtuto__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Pas administrateur dans le canal**\n__Je ne suis pas administrateur dans ce [canal]({channel_url}). Ajoutez-moi en tant qu'administrateur afin d'activer ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Nom d'utilisateur/ID de chaîne non valide.**")
        except Exception as err:
          message.reply_text(f"❗ **ERREUR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        message.reply_text(f"✅ **Forcer l'abonnement est activé dans ce chat.**\n__pour ce  [Canal]({channel_url})__/n **Dévellopée par l'équipe** @codingtuto ", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Forcer l'abonnement est désactivé dans ce groupe.**")
  else:
      message.reply_text("❗ **Créateur de groupe requis**\n__Vous devez être le créateur du groupe pour le faire .__")

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = "DXWPtDJnMaLmCr5whwiY9whd"
IMG_PATH = "./DOWNLOADS"

FayasNoushad = Client(
    "Remove Background Bot",
    bot_token = "5262921643:AAG4rteoha8hM1bK9nchzxnFhDigfMQTa5s",
    api_id = 7924471,
    api_hash = "1e706c26adb6600aac9d62688dc81605",
)

START_TEXT = """
Salam {}, Mən sənin atdığın şəkillərin arxa planını silmək üçün @DeMoN_DPB_TTX və @Cahildi tərəfindən kodlaşdırılmışam\nSualın olarsa və ya botda xəta əmələ gələrsə, Sahiblə əlaqə saxla :)

"""
HELP_TEXT = """
- Şəkili mənə at
- Mən şəkili yükləyəcəm
- Arxa planı silib yenidən sənə atacağam

Mən RemoveBG api*sindən istifadə olunaran kodlaşdırılmışam.
"""
ABOUT_TEXT = """
- **Bot :** `MWRemoveBgBot`
- **Sahib :** [n404](https://t.me/Cahilemdi)
- **Kanalımız :** [Maraqlı Web💻(Hacker)](https://t.me/maragliweb)
- **Kanalımız :** [Dark Web Azerbaijan](https://t.me/DarkWebAzerbaijan)
- **Qrupumuz :** [𝔸𝕫𝕖𝕣𝕓𝕒𝕚𝕛𝕒𝕟 𝕋𝕖𝕩𝕟𝕠𝕝𝕠𝕛𝕚 𝕊𝕦𝕡𝕡𝕠𝕣𝕥 💻](https://t.me/AzerbaijanSupport)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📢Kanalımız', url='https://t.me/maragliweb'),
        InlineKeyboardButton('Sahib👤', url='https://t.me/Cahilemdi'),
        InlineKeyboardButton('👥Qrupumuz', url='https://t.me/AzerbaijanSupport')
        ],[
        InlineKeyboardButton('Kömək', callback_data='help'),
        InlineKeyboardButton('Ətraflı məlumat', callback_data='about'),
        InlineKeyboardButton('Bağla', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Ana Menyu', callback_data='home'),
        InlineKeyboardButton('Ətraflı məlumat', callback_data='about'),
        InlineKeyboardButton('Bağla', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Ana Menyu', callback_data='home'),
        InlineKeyboardButton('Kömək', callback_data='help'),
        InlineKeyboardButton('Bağla', callback_data='close')
        ]]
    )
ERROR_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Kömək', callback_data='help'),
        InlineKeyboardButton('Bağla', callback_data='close')
        ]]
    )
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📢Güncəlləmələr', url='https://t.me/')
        ]]
    )

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@FayasNoushad.on_message(filters.private & (filters.photo | filters.document))
async def remove_background(bot, update):
    if not API:
        await update.reply_text(
            text="Xəta :- Remove BG Api \nXahiş edirəm bunu adminə bildir!",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Analysing",
        quote=True,
        disable_web_page_preview=True
    )
    if (update and update.media and (update.photo or (update.document and "image" in update.document.mime_type))):
        file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "image.jpg"
        new_file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "MWRemoveBgBot.png"
        await update.download(file_name)
        await message.edit_text(
            text="Şəkil yükləndi. Hal-hazırda arxa plan silinir.",
            disable_web_page_preview=True
        )
        try:
            new_image = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": open(file_name, "rb")},
                data={"size": "auto"},
                headers={"X-Api-Key": API}
            )
            if new_image.status_code == 200:
                with open(f"{new_file_name}", "wb") as image:
                    image.write(new_image.content)
            else:
                await update.reply_text(
                    text="API is error.",
                    quote=True,
                    reply_markup=ERROR_BUTTONS
                )
                return
            await update.reply_chat_action("upload_photo")
            await update.reply_document(
                document=new_file_name,
                quote=True
            )
            await message.delete()
            try:
                os.remove(file_name)
            except:
                pass
        except Exception as error:
            print(error)
            await message.edit_text(
                text="Xəta :- Remove BG Api \nXaiş edirəm bunu adminə bildir!",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
    else:
        await message.edit_text(
            text="Media dəstəklənmir",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )

FayasNoushad.run()

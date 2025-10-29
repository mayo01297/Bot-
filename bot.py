import os
import discord
from discord.ext import commands
from discord import app_commands
from googletrans import Translator

TOKEN = os.environ.get("DISCORD_TOKEN", "")

translator = Translator()

# サポートする言語
LANG_CHOICES = [
    ("日本語", "ja"), ("英語", "en"), ("中国語", "zh-cn"),
    ("韓国語", "ko"), ("フランス語", "fr"), ("ドイツ語", "de"),
    ("スペイン語", "es"), ("ロシア語", "ru"),
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def translate_text(text: str, target: str) -> str:
    try:
        result = translator.translate(text, dest=target)
        return result.text
    except Exception as e:
        return f"[翻訳エラー] {e}"

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synced: {len(synced)}")
    except Exception as e:
        print("Slash sync failed:", e)
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

@bot.tree.command(name="tr", description="テキストを翻訳します")
@app_commands.describe(text="翻訳したいテキスト", target="翻訳先の言語")
@app_commands.choices(target=[app_commands.Choice(name=n, value=v) for n, v in LANG_CHOICES])
async def tr(inter: discord.Interaction, text: str, target: app_commands.Choice[str]):
    await inter.response.defer(thinking=True)
    translated = translate_text(text, target.value)
    await inter.followup.send(
        f"**翻訳 ({target.name})**\n> {discord.utils.escape_markdown(text)}\n\n{translated}"
    )

@bot.tree.context_menu(name="日本語に翻訳")
async def ctx_to_japanese(inter: discord.Interaction, message: discord.Message):
    await inter.response.defer(thinking=True, ephemeral=True)
    translated = translate_text(message.content, "ja")
    await inter.followup.send(f"**→ 日本語訳**\n{translated}", ephemeral=True)

if not TOKEN:
    raise RuntimeError("環境変数 DISCORD_TOKEN を設定してください。")
bot.run(TOKEN)

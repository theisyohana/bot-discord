import discord
from discord.ext import commands

# Puxar o TOKEN do bot pelo ".env"
from dotenv import load_dotenv
import os

load_dotenv(".env")

TOKEN = os.getenv("TOKEN")

# CONFIGURAÇÕES

APRESENTACAO_CHANNEL_ID = 1563376590262505623
ENTRADAS_CHANNEL_ID = 1398127541545472093
SAIDAS_CHANNEL_ID = 1398127792394207404

# INTENTS

intents = discord.Intents.default()
intents.members = True

# Servidor para atualizar

async def setup_hook(self):
    servidor = discord.Object(id=1397987038309122178)

    await self.tree.sync(guild=servidor)

    print("Comandos sincronizados!")

# Modal de apresentação

class apresentacao_modal(discord.ui.Modal, title="Apresente-se!"):

    apresentação = discord.ui.TextInput(
        label="Me fale um pouco sobre você!",
        placeholder="Escreva sobre você aqui...",
        style=discord.TextStyle.paragraph,
        min_length=10,
        max_length=4000,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        resposta = self.apresentação.value
        canal = interaction.guild.get_channel(APRESENTACAO_CHANNEL_ID)

        embed = discord.Embed(
            title="🎨 Apresentação",
            description=resposta,
            color=discord.Color.dark_purple()
        )

        embed.add_field(
            name="👤 Usuário",
            value=f"{interaction.user.mention} (`{interaction.user.id}`)",
            inline=False
        )

        embed.set_footer(
            text=f"Apresentação enviada por {interaction.user}"
        )

        # Mostra a foto de perfil
        embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        # Responde primeiro à interação
        await interaction.response.send_message(
            "✅ Sua apresentação foi enviada com sucesso!",
            ephemeral=True
        )

        # Depois envia o Embed para o canal
        await canal.send(embed=embed)

# BOT

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        await self.tree.sync()

        print("✅ Comandos sincronizados!")


bot = Bot()

# COMANDO / apresentação
@bot.tree.command(
    name="apresentação",
    description="Envie uma apresentação falando sobre você!"
)
async def apresentacao(interaction: discord.Interaction):

    print("🔥 APRENTAÇÃO FOI EXECUTADO!")

    await interaction.response.send_modal(
        apresentacao_modal()
    )

# BOT ONLINE

@bot.event
async def on_ready():

    print(f"🟢 BOT ONLINE: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")

# QUANDO ALGUÉM ENTRA

@bot.event
async def on_member_join(membro):

    canal = bot.get_channel(ENTRADAS_CHANNEL_ID)

# Cria embed
    embed = discord.Embed(
        title="Caiu de paraquedas!",
        description=f"Seja muito bem-vindo(a), {membro.mention}!\nEsperamos que você aproveite sua estadia por aqui.",
        color=discord.Color.dark_purple()
    )
# Mostra a foto de perfil
    embed.set_thumbnail(
        url=membro.display_avatar.url
    )

    await canal.send(embed=embed)

@bot.event
async def on_member_remove(membro):
    print(f"{membro.name} saiu do servidor")
    
    
    canal = bot.get_channel(SAIDAS_CHANNEL_ID)
    
    # Cria embed
    embed = discord.Embed(
        title="Até mais!",
        description=f"Membro saiu do servidor, {membro.mention}!\nName: {membro.name} \n ID: {membro.id}",
        color=discord.Color.dark_purple()
    )
    # Mostra a foto de perfil
    embed.set_thumbnail(
        url=membro.display_avatar.url
    )
    
    await canal.send(embed=embed)

# Verificar ping

@bot.tree.command(
    name="ping",
    description="Veja a latência do bot"
)
async def ping(interaction: discord.Interaction):

    latencia = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 Pong! **{latencia}ms**"
    )

# INICIAR BOT
bot.run(TOKEN)

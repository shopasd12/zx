import os 
import discord
from discord.ui import Button, View, Modal, TextInput
from discord.ext import commands, tasks
import asyncio
import random

from myserver import server_on



GUILD_ID = 1320391859322753075 
CHANNEL_ID = 1320391859754897484  
WEBHOOK_URL = 'https://discord.com/api/webhooks/1324846311526109285/i9iwmQ6SBJxSx7V5ewfVYbXnbGI_i_qAc_bBD6aZFsX8jCE_M0RyLj3JNrYHCibrLQ-f'  

# สร้างบอท
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


streaming_status = [
    "Playing a game 🎮",
    "Chatting with users 💬",
    "Helping with support tickets 📝",
    "SHGOP SHOP NO.1 🎥",
    "Playing music 🎶"
]


@tasks.loop(seconds=30)
async def update_stream_status():
    status = random.choice(streaming_status) 
    await bot.change_presence(activity=discord.Game(name=status))  


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    update_stream_status.start()  

  
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
     
        embed = discord.Embed(
            title="🧊 สวัสดี! 🥙",
            description="🍟>ตอนนี้บอทของเราพร้อมให้บริการแล้ว! ⚡\n\n"
                        "🧇หากคุณต้องการเปิดตั๋วเพื่อคุยกับแอดมิน โปรดกดปุ่มด้านล่าง 👇\n\n"
                        "🍣หากคุณพบปัญหาใด ๆ กดปุ่ม 'แจ้งปัญหา' เพื่อแจ้งได้เลย!👁",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://th.bing.com/th/id/OIP.1mofGys7_n3_uhqIAkAnlgHaEK?rs=1&pid=ImgDetMain")  # ใส่ URL รูปภาพหรือ GIF ที่ต้องการแสดง
        embed.set_footer(text="ทีมแอดมินพร้อมช่วยเหลือคุณ!")
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.R8NNB53byP0myVXy_bcJ9AHaD4?rs=1&pid=ImgDetMain")  # ปกที่จะแสดงด้านขวาบน (thumbnail)

        view = TicketView()
        await channel.send(embed=embed, view=view)


class TicketView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="🤍เปิดตั๋วคุยแอดมิน❤", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        user_name = interaction.user.name

        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Support") 
        
        if not category:

            category = await guild.create_category("Support")


        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),  
                interaction.user: discord.PermissionOverwrite(read_messages=True), 
            }
        )

 
        embed = discord.Embed(
            title=f"❤เปิดตั๋วคุยแอดมิน🤍",
            description=f"สวัสดี {interaction.user.mention} 🧇คุณสามารถคุยกับแอดมินที่นี่ได้เลย👑",
            color=discord.Color.green()
        )
        embed.set_image(url="https://th.bing.com/th/id/OIP.d1L3BTZnO9yxkNz740yymAHaEK?rs=1&pid=ImgDetMain")  # ปกภาพ (เช่น รูปภาพหรือ GIF ที่ต้องการแสดง)
        embed.set_footer(text=f"ID ของผู้ใช้: {user_id}")
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.R8NNB53byP0myVXy_bcJ9AHaD4?rs=1&pid=ImgDetMain")  # ปกที่จะแสดงด้านขวาบน (thumbnail)


        await channel.send(embed=embed)


        close_button = Button(label="🥗ปิดตั๋ว❄", style=discord.ButtonStyle.red)
        
        async def close_ticket(interaction: discord.Interaction):
            await channel.send("💞ตั๋วนี้จะถูกปิดเนื่องจากคำขอของผู้ใช้ หรือแอดมิน🍜")
            await channel.delete()

        close_button.callback = close_ticket

   
        await channel.send("💩หากคุณต้องการปิดตั๋วนี้ กรุณากดปุ่มด้านล่าง💩", view=View().add_item(close_button))

 
        await interaction.response.send_message("❄🧊คุณได้เปิดตั๋วแล้ว! รอแอดมินตอบกลับ🧊", ephemeral=True)

    @discord.ui.button(label="🍤แจ้งปัญหา🔞", style=discord.ButtonStyle.blurple)
    async def report_issue(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        modal = IssueReportModal()
        await interaction.response.send_modal(modal)


class IssueReportModal(Modal):
    def __init__(self):
        super().__init__(title="🥪แจ้งปัญหาของคุณ🥠")

       
        self.issue_input = TextInput(
            label="กรุณากรอกข้อความปัญหาของคุณ",
            style=discord.TextStyle.paragraph,
            placeholder="กรอกข้อความของคุณที่นี่...",
            required=True,
            max_length=1000
        )
        self.add_item(self.issue_input)

    async def callback(self, interaction: discord.Interaction):
        issue_message = self.issue_input.value 

      
        webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
        embed = discord.Embed(
            title="🍖แจ้งปัญหาใหม่🧇",
            description=issue_message,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"โดย {interaction.user.name}")
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.R8NNB53byP0myVXy_bcJ9AHaD4?rs=1&pid=ImgDetMain")  # ปกที่จะแสดงด้านขวาบน (thumbnail)

        await webhook.send(embed=embed)

        
        await interaction.response.send_message("ปัญหาของคุณถูกแจ้งเรียบร้อยแล้ว! ขอบคุณที่แจ้งมา.", ephemeral=True)
server_on()


bot.run(os.getenv('TOKEN'))

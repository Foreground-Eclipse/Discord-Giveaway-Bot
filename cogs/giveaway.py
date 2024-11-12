from disnake.ext import commands, tasks
import disnake
from datetime import timedelta, datetime, timezone
import json
from db.dbhandler import *
from random import choice

def getTimeoutTimestamp(hours: int) -> str:
    now_utc = datetime.now(timezone.utc)
    future_time_utc = now_utc + timedelta(hours=hours)
    timestamp = int(future_time_utc.timestamp())

    return (f"<t:{timestamp}:F>")

def getTimeout(hours: int) -> str:
    now = datetime.now()
    future_time = now + timedelta(hours=hours)

    return future_time


class GiveawayPrizeSelectionModal(disnake.ui.Modal):
    def __init__(self,channel: disnake.TextChannel, role: disnake.Role, hours : int):
        self.channel = channel
        self.role = role
        self.hours = hours
        title = "Set giveaway prize"
        components = [
            disnake.ui.TextInput(label="Set prize", placeholder="500b zenny", custom_id="giveawayprize")
        ]

        super().__init__(title=title, components=components, custom_id="giveawayprizemodal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        prize = interaction.text_values["giveawayprize"]
        embed = disnake.Embed(title="New giveaway!", description=f"This is a new giveaway. This time prize will be: {prize}!, participate by clicking the button below! \n Giveaway will end at {getTimeoutTimestamp(self.hours)}")
        
        await interaction.response.send_message(embed=embed, view = ButtonsVerifyTimeout(self.channel, self.role, self.hours, prize), ephemeral=True)


class GiveawayTimeoutModal(disnake.ui.Modal):
    def __init__(self, channel: disnake.TextChannel, role: disnake.Role):
        self.channel = channel
        self.role = role
        title = "Set giveaway timeout"
        components = [
            disnake.ui.TextInput(label="Set timeout in hours", placeholder="48", custom_id="timeouthours"),
             disnake.ui.TextInput(label="Set prize", placeholder="500b zenny", custom_id="giveawayprize")
        ]

        super().__init__(title=title, components=components, custom_id="giveawaytimeoutmodal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        hours = interaction.text_values["timeouthours"]
        prize = interaction.text_values["giveawayprize"]
        if hours.isnumeric:
            embed = disnake.Embed(title="New giveaway!", description=f"New giveaway just started by <@{interaction.user.id}>. \n This time prize will be: {prize}! \n participate by clicking the button below! \n Giveaway will end at {getTimeoutTimestamp(int(hours))}")

            await interaction.response.send_message(embed=embed, view = ButtonsVerifyTimeout(self.channel, self.role, hours, prize),content=f"<@&{self.role.id}>", ephemeral=True)
            
        else:

            await interaction.response.send_message("Your input was incorrect, please input the timeout before giveaway ends in hours", ephemeral=True)



class ButtonsVerifyTimeout(disnake.ui.View):
    def __init__(self,channel: disnake.TextChannel, role: disnake.Role, hours : int, prize: str):
        self.channel = channel
        self.role = role
        self.hours = int(hours)
        self.prize = prize
        super().__init__(timeout=None)
        
    @disnake.ui.button(label='Confirm', style=disnake.ButtonStyle.green)
    async def confirmTimeout(self, button, interaction: disnake.Interaction):
       embed = disnake.Embed(title="New giveaway!", description=f"New giveaway just started by <@{interaction.user.id}>. \n This time prize will be: {self.prize}! \n participate by clicking the button below! \n Giveaway will end at {getTimeoutTimestamp(self.hours)}")
       embed.set_footer(text = "Total participants:0")
       message = await self.channel.send(embed=embed, view = ButtonsVerify(), content=f"<@&{self.role.id}>")
       insertGiveaways(getTimeout(self.hours), interaction.user.id, message.id,message.channel.id, interaction.guild.id)
       
    @disnake.ui.button(label='Decline', style=disnake.ButtonStyle.red)
    async def declineTimeout(self, button, interaction: disnake.Interaction):
       await interaction.response.send_message("Please re-use the command", ephemeral=True)
    

# buttons to participate
class ButtonsVerify(disnake.ui.View):
    def __init__(self, ):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Participate', style=disnake.ButtonStyle.green, custom_id="participatepersistent") 
    async def participateButton(self, button, interaction: disnake.Interaction):
       await interaction.response.defer()
       message = await interaction.original_message()
       if checkIfAlreadyParticipate(interaction.user.id, getGiveawayID(str(message.id))) != 0:
           await interaction.followup.send("You already participate in this giveaway", ephemeral=True)
           return
       else:
            insertParticipant(interaction.user.id, getGiveawayID(str(message.id)))
            embed = message.embeds[0]
            total = getAllParticipants(messageID=str(message.id))

            try:

                embed.set_footer(text=f"Total participants:{len(total)}")
            except Exception:

                print(f"message: {message}")
                print(total)

            await message.edit(embed=embed)
            await interaction.followup.send("You now participate in giveaway", ephemeral=True)

            return




class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
        
    

    @commands.slash_command()
    async def startgiveaway(self, interaction: disnake.CommandInteraction, channel:disnake.TextChannel, giveawayrole: disnake.Role):

        await interaction.response.send_modal(GiveawayTimeoutModal(channel, giveawayrole))
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Listener has started")
        giveawayCheck.start(self.bot)
        if not self.persistent_views_added:
            self.bot.add_view(ButtonsVerify())
            self.persistent_views_added = True
        

@tasks.loop(minutes=5.0)
async def giveawayCheck(bot):
    current_time = datetime.now()

    for timeout in getAllGiveawaysTimeout():

        saved_time = datetime.strptime(timeout[0], '%Y-%m-%d %H:%M:%S.%f')
        time_difference = current_time - saved_time

        if time_difference >= timedelta(minutes=1):  

            guild = bot.get_guild(int(timeout[3]))
            channel = guild.get_channel(int(timeout[2]))

            if channel:
                message = await channel.fetch_message(int(timeout[1]))
                if message:

                    updateGiveawayStatus(timeout[1])
                    participants = getAllParticipants(messageID=str(timeout[1]))
                    winner = choice(participants)

                    await message.reply(f"Giveaway has ended! <@{winner}> won the giveaway!")

            
            
    
     

def setup(bot):
    bot.add_cog(Giveaway(bot))
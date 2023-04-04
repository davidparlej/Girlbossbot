import discord 
from discord import app_commands


import traceback

#test guild where slash commang will be registered

TEST_GUILD = discord.Object(0)


class MyClient(discord.Client):
	def __init__(self) -> None:
		#default intents and a discord.client instance 
		#no need for commands.bot because are not doing text based commands
		intents = discord.Intents.default()
		super().__init__(intents=intents)



		#discord.app_commands.Command Tree for commands
		self.tree = app_commands.CommandTree(self)

	async def on_ready(self):
		print(f'Logged in as {self.user} (ID: {self.user.id})')
		print('--------')


	async def setup_hook(self) -> None:
		#syncs app with Discord
		await self.tree.sync(guild=TEST_GUILD)

class Feedback(discord.ui.Modal, title= 'Feedback'):
	#modal class must subclass discord.ui.Modal
	#title can be whatever though

	#short input style 
	name = discord.ui.TextInput(
		label = 'Name',
		placeholder = 'Your name here...',
	)


	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.send_message(f'Thanks for your feedback,{self.name.value}!', ephemeral = True)

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		await interaction.response.send_message('Oops! something went wrong.', ephmeral = True)


		#checking error back 
		traceback.print_exception(type(error), error, error.__traceback__)

client = MyClient()


@client.tree.command(guild=TEST_GUILD, description="Submit Feedback")
async def feedback(interaction: discord.Interaction):
	#sends the modal with an instance of the feedback class
	#since modals require an interaction, they cannot be done as a response to a text command 
	#they can only be done as a response to either an application command or a button press.
	await interaction.response.send_modal(Feedback())

token = None

if "BOT_KEY" in os.environ:
	token = os.environ["BOT_KEY"]
	print("Using enviroment var for key")
elif os.path.isfile("key"):
	print("Using file for key")
	with open("key", "r") as f:
		token = f.read().strip().strip("\n")

if token is not None:
	bot.run(token)
else:
	print("Could not retrieve token")
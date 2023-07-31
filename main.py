import discord
import requests
import asyncio

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# Function to fetch the GMCoin-USD price

def get_gmcoin_try_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "Your_Coinmarketcap_API_Key"
    }
    params = {
        "symbol": "GMCOIN",  #Replace it which coin you want
        "convert": "TRY"     #Replace it which fiat currency you want
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    price = data["data"]["GMCOIN"]["quote"]["TRY"]["price"] #Replace them which coin and fiat currency you want
    
    return price

@client.event
async def on_ready():
    print("Bot is ready!")

    # Start a background task to update nickname every 5 minutes
    await update_nickname_task()

async def update_nickname_task():
    while not client.is_closed():
        # Fetch price
        price = get_gmcoin_try_price()
        if price is not None:
            # Format the price with two decimal places
            gmcoin_price_formatted = "{:.2f}".format(float(price))
            new_nick = f"GMCoin: {gmcoin_price_formatted}$"
            print("Updated price-", new_nick)
            for guild in client.guilds:
                me = guild.me
                await me.edit(nick=new_nick)
        else:
            print("Failed to fetch price.")

        # Wait for 5 minutes before the next update
        await asyncio.sleep(300)  # 5 minutes in seconds

# Run the bot using your token
client.run("Your_Discord_Bot_Token")

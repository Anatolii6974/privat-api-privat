import platform
import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_exchange_rates(date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return None
        except aiohttp.ClientConnectorError as err:
            return None    

async def get_exchange_rates_for_days(days):
    exchange_rates = []
    today = datetime.now()
    
    for i in range(days):
        date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
        data = await fetch_exchange_rates(date)
        exchange_rates.append({date: data})
    
    return exchange_rates

def display_results(data):
    for day_data in data:
        date, rates = day_data.popitem()
        print(f"{date}:")

        print(f"  EUR:{rates['exchangeRate'][8]['currency']} sale={rates['exchangeRate'][8]['saleRate']}, purchase={rates['exchangeRate'][8]['purchaseRate']}")
        print(f"  USD:{rates['exchangeRate'][23]['currency']} sale={rates['exchangeRate'][23]['saleRate']}, purchase={rates['exchangeRate'][23]['purchaseRate']}")

async def main():
    if len(sys.argv) != 2:
        print("Usage: py main.py <days>")
        return
    
    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Error: Number of days should not exceed 10.")
            return

        exchange_rates = await get_exchange_rates_for_days(days)
        display_results(exchange_rates)
    
    except ValueError:
        print("Error: Invalid number of days.")
    

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
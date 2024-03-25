# Import necessary libraries and modules
from signal_processor import get_signal, periodically_get_signal
from binance import AsyncClient
from decimal import Decimal, ROUND_DOWN
import asyncio
from config import *  # Import configuration variables like API keys

# Initial setup for trading state
in_position = False  # Flag to track if currently holding a position
position_type = True  # Variable to indicate the type of position (BUY or SELL), initially set to True arbitrarily
trade_price = 0  # Store the price at which the last trade was executed
signal = None  # Variable to store the current trading signal
code = 0  # Code used for indexing assets, if needed

# Function to round and format numbers accurately for trading calculations
async def decimal(num, num2):
    try:
        float_number = float(num)  # Convert number to float for processing
        number = Decimal(float_number)  # Create a Decimal object for accurate financial calculations
        truncated = number.quantize(Decimal(num2), rounding=ROUND_DOWN)  # Round or truncate number as specified
        return float(truncated)  # Return the processed number as float
    except Exception as e:
        print(f"Error converting decimal: {e}")

# Function to open a trading order (buy or sell)
async def open_order(client, side):
    try:
        global code, symbol, trade_price, crypto
        info = await client.get_isolated_margin_account()  # Fetch isolated margin account details
        # Calculate USDT amount to use for the trade, based on account balance and predefined multiplier (9x here)
        usdt = await decimal((float(info['assets'][code]['quoteAsset']['netAsset']) * 9), "1.0000")
        info = await client.get_margin_price_index(symbol=symbol)  # Get current price index for the symbol
        price = float(info['price'])  # Current price of the cryptocurrency
        order = await decimal(usdt/price, "1.00000")  # Calculate the quantity to order based on available USDT and price
        
        # Process buy order
        if side == 'BUY':
            if usdt > 0:
                # Create a margin loan for buying, then place a buy order
                result = await client.create_margin_loan(asset='USDT', amount=str(usdt), isIsolated='TRUE', symbol=symbol)
                order = await client.create_margin_order(symbol=symbol, side=side, type='MARKET', quantity=order, isIsolated='TRUE')
        
        # Process sell order
        elif side == 'SELL':
            if usdt > 0:
                # Create a margin loan for selling, then place a sell order
                result = await client.create_margin_loan(asset=crypto, amount=str(order), isIsolated='TRUE', symbol=symbol)
                order = await client.create_margin_order(symbol=symbol, side=side, type='MARKET', quantity=order, isIsolated='TRUE')
        
        # Update the trade_price with the price at which the order was executed
        trade_price = float(order['fills'][0]['price'])
        print(f"Order executed successfully: {order}")
        print(f"{side}ing {crypto} @ {trade_price}")
    except Exception as e:
        # If an error occurs during the order process, log the error
        print("error opening order", e)

# Function to close an open trading position
async def close_order(client, side):
    try:
        global crypto, code, symbol
        # Fetch recent trades to determine the quantity of the last trade
        trades = await client.get_margin_trades(symbol=symbol, isIsolated=True)
        order_qty = float(trades[-1]['Qty'])  # Quantity from the last trade
        
        # Create a market order to close the position
        order = await client.create_margin_order(symbol=symbol, side=side, type='MARKET', quantity=order_qty, isIsolated='TRUE')
        
        # Calculate the amount to repay the margin loan, including borrowed amount and interest
        if side == 'BUY':
            info = await client.get_isolated_margin_account()
            repay_amount = await decimal(info['assets'][code]['baseAsset']['borrowed'] + info['assets'][code]['baseAsset']['interest'], '1.00000')
            result = await client.repay_margin_loan(asset=crypto, amount=str(repay_amount), isIsolated='TRUE', symbol=symbol)
        elif side == 'SELL':
            info = await client.get_isolated_margin_account()
            repay_amount = await decimal(info['assets'][code]['quoteAsset']['borrowed'] + info['assets'][code]['quoteAsset']['interest'], '1.0000')
            result = await client.repay_margin_loan(asset='USDT', amount=str(repay_amount), isIsolated='TRUE', symbol=symbol)
        
        print("Order closed", result)
    except Exception as e:
        # If an error occurs while closing the order, log the error
        print("error while closing order", e)

# The main function where trading logic is executed
async def main():
    global in_position, trade_price, position_type
    try:
        # Initialize the Binance client with API keys
        client = await AsyncClient.create(API_KEY, API_SECRET)
        
        # Start periodically checking for trading signals in the background
        asyncio.create_task(periodically_get_signal())
        
        # Reset trading state variables
        in_position = False
        trade_price = 0
        position_type = None
        
        # Main trading loop
        while True:
            # If not currently in a position, check the signal and open a corresponding order
            if not in_position:
                if signal == 'BUY':
                    await open_order(client, 'BUY')
                    in_position = True
                    position_type = 'BUY'
                elif signal == 'SELL':
                    await open_order(client, 'SELL')
                    in_position = True
                    position_type = 'SELL'
                else:
                    # If no valid signal, wait and then continue checking
                    print("Waiting on signal")
                    await asyncio.sleep(1)
            # If already in a position, monitor for signal to close the position
            elif in_position:
                # Logic to close positions could be added here, similar to opening orders
                if position_type == 'SELL' :
                    if signal == "BUY":
                        await close_order(client , signal )
                        in_position = False
                        position_type = False
                        trade_price = 0 
                elif position_type == 'BUY' :
                    if signal == "SELL":
                        await close_order(client , signal )
                        in_position = False
                        position_type = False
                        trade_price = 0 
                
                # Fetch current price for logging
                info = await client.get_margin_price_index(symbol=symbol)
                price = float(info['price'])
                print(f"Position: {position_type}, Signal: {signal}, Trade Price: {trade_price}, Current Price: {price}")
                await asyncio.sleep(1)
                
    except Exception as e:
        print("Interrupted by the user", e)
    finally:
        # Ensure to close the client connection when done
        if client:
            await client.close_connection()
            print("Client session closed.")

# Entry point for the script
if __name__ == "__main__":
    asyncio.run(main())


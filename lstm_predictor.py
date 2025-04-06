
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_historical_data(symbol):
    return pd.DataFrame({'close': [1, 2, 3, 2, 4, 5, 6, 5, 4, 6, 7]})

def run_prediction_pipeline(min_volume=500000, with_plot=False, leverage=75):
    data = [
        {'Pair': 'BTCUSDT', 'Signal': 'LONG', 'Expected % (75x)': 12.5},
        {'Pair': 'ETHUSDT', 'Signal': 'SHORT', 'Expected % (75x)': 8.3}
    ]
    df_result = pd.DataFrame(data)

    if with_plot:
        os.makedirs("static", exist_ok=True)
        for symbol in df_result['Pair']:
            df = get_historical_data(symbol)
            plt.figure(figsize=(10, 4))
            plt.plot(df['close'], label='Price')
            plt.title(f'{symbol} — История цены')
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'static/{symbol}.png')
            plt.close()

    return df_result

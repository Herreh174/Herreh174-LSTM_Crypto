import os
import logging
from datetime import datetime

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_folder, "signals.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from flask import Flask, render_template, request
from lstm_predictor import run_prediction_pipeline
import requests
import os

app = Flask(__name__)
config = {
    'TELEGRAM_TOKEN': '',
    'TELEGRAM_CHAT_ID': '',
    'MIN_VOLUME': 500000,
    'LEVERAGE': 75
}

def send_telegram_message(text):
    token = config['TELEGRAM_TOKEN']
    chat_id = config['TELEGRAM_CHAT_ID']
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        config['TELEGRAM_TOKEN'] = request.form.get('telegram_token')
        config['TELEGRAM_CHAT_ID'] = request.form.get('telegram_chat_id')
        config['MIN_VOLUME'] = int(request.form.get('min_volume'))
        config['LEVERAGE'] = int(request.form.get('leverage'))

    df_result = run_prediction_pipeline(min_volume=config['MIN_VOLUME'], with_plot=True, leverage=config['LEVERAGE'])
    table_html = df_result.to_html(classes='table table-striped', index=False, escape=False)

    if config['TELEGRAM_TOKEN'] and config['TELEGRAM_CHAT_ID']:
        message = "📊 <b>Crypto LSTM Signals</b>\n"
        for _, row in df_result.iterrows():
            message += f"{row['Pair']}: {row['Signal']} ({row['Expected % (75x)']}%)\n"
        send_telegram_message(message)
        logging.info(message)

    return render_template('index.html', tables=table_html, config=config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

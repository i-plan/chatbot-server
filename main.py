from app import create_app
from app.api.chat import socketio
import logging
import os

from dotenv import load_dotenv

from app.openai_helper import OpenAIHelper, default_max_tokens
from app.telegram_bot import ChatGPTTelegramBot

'''
- 127.0.0.1：回环地址。该地址指电脑本身，主要预留测试本机的TCP/IP协议是否正常。只要使用这个地址发送数据，则数据包不会出现在网络传输过程中。
- 10.x.x.x、172.16.x.x～172.31.x.x、192.168.x.x：这些地址被用做内网中。用做私网地址，这些地址不与外网相连。
- 255.255.255.255：广播地址
- 0.0.0.0：这个IP地址在IP数据报中只能用作源IP地址，这发生在当设备启动时但又不知道自己的IP地址情况下。

IPV4中，0.0.0.0地址被用于表示一个无效的，未知的或者不可用的目标。
* 在服务器中，0.0.0.0指的是本机上的所有IPV4地址，如果一个主机有两个IP地址，192.168.1.1 和 10.1.2.1，并且该主机上的一个服务监听的地址是0.0.0.0,那么通过两个ip地址都能够访问该服务。
* 在路由中，0.0.0.0表示的是默认路由，即当路由表中没有找到完全匹配的路由的时候所对应的路由。


用途：
- DHCP分配前，表示本机。
- 用做默认路由，表示任意主机。
- 用做服务端，表示本机的任意IPV4地址。

比如我有一台服务器，一个外网A,一个内网B，如果我绑定的端口指定了0.0.0.0，那么通过内网地址或外网地址都可以访问我的应用。
启动生产环境服务器：python3 -m app
'''
app = create_app(config_file='prod_config.py')


def telegram_bot():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
        exit(1)

    # Setup configurations
    model = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    max_tokens_default = default_max_tokens(model=model)
    openai_config = {
        'api_key': os.environ['OPENAI_API_KEY'],
        'show_usage': os.environ.get('SHOW_USAGE', 'false').lower() == 'true',
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'proxy': os.environ.get('PROXY', None),
        'max_history_size': int(os.environ.get('MAX_HISTORY_SIZE', 15)),
        'max_conversation_age_minutes': int(os.environ.get('MAX_CONVERSATION_AGE_MINUTES', 180)),
        'assistant_prompt': os.environ.get('ASSISTANT_PROMPT', 'You are a helpful assistant.'),
        'max_tokens': int(os.environ.get('MAX_TOKENS', max_tokens_default)),
        'n_choices': int(os.environ.get('N_CHOICES', 1)),
        'temperature': float(os.environ.get('TEMPERATURE', 1.0)),
        'image_size': os.environ.get('IMAGE_SIZE', '512x512'),
        'model': model,
        'presence_penalty': int(os.environ.get('PRESENCE_PENALTY', 0)),
        'frequency_penalty': int(os.environ.get('FREQUENCY_PENALTY', 0)),
    }

    telegram_config = {
        'token': os.environ['TELEGRAM_BOT_TOKEN'],
        'admin_user_ids': os.environ.get('ADMIN_USER_IDS', '-'),
        'allowed_user_ids': os.environ.get('ALLOWED_TELEGRAM_USER_IDS', '*'),
        'monthly_user_budgets': os.environ.get('MONTHLY_USER_BUDGETS', '*'),
        'monthly_guest_budget': float(os.environ.get('MONTHLY_GUEST_BUDGET', '100.0')),
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'proxy': os.environ.get('PROXY', None),
        'voice_reply_transcript': os.environ.get('VOICE_REPLY_WITH_TRANSCRIPT_ONLY', 'true').lower() == 'true',
        'ignore_group_transcriptions': os.environ.get('IGNORE_GROUP_TRANSCRIPTIONS', 'true').lower() == 'true',
        'group_trigger_keyword': os.environ.get('GROUP_TRIGGER_KEYWORD', ''),
        'token_price': float(os.environ.get('TOKEN_PRICE', 0.002)),
        'image_prices': [float(i) for i in os.environ.get('IMAGE_PRICES', "0.016,0.018,0.02").split(",")],
        'transcription_price': float(os.environ.get('TOKEN_PRICE', 0.002)),
    }

    # Setup and run ChatGPT and Telegram bot
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = ChatGPTTelegramBot(config=telegram_config, openai=openai_helper)
    telegram_bot.run()

import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, '0.0.0.0', 9000):
        await asyncio.Future()  # run forever



if __name__ == '__main__':
    # threading.Thread(target=telegram_bot).start()
    # app = create_app(config="settings.yaml")
    print("正式服务启动" + "." * 100)
    socketio.init_app(app)
    socketio.run(app, host=os.getenv("HOST", default='0.0.0.0'), port=os.getenv("PORT", default=9000),debug=True,allow_unsafe_werkzeug=True)
    # app.run(host=os.getenv("HOST", default='0.0.0.0'), port=os.getenv("PORT", default=9000))

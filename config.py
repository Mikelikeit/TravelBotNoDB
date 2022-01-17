from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN = env.list('ADMINS')
IP = env.str('ip')

PGUSER = env.str('PGUSER')
PGPASSWORD = env.str('PGPASSWORD')
DATABASE = env.str('DATABASE')

POSTGRESURI = f'postgtesql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'

open_weather_token = '698a1fe85babbdbc4cbed2a82baddf6b'

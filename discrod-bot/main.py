import shutil, pytz
import os, subprocess
from datetime import datetime
from google.cloud import storage
# import discord.ext.commands

# Backup this collections.
collection_list = [ "apps", "workflows", "operations", "app_actions", "users", "orgs", "versions", "translations" ]

def date_today():
    '''
    defines the date today
    '''
    _date = str(datetime.now(pytz.timezone('Asia/Jerusalem')).strftime("%d-%m-%Y"))
    _dir = "./" + _date
    return _date, _dir

def defines_env(env):
    '''
    defines the env of the backup
    '''
    if env == "dev":
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/releai/keys/releai-bot-dev.json"
        subprocess.run(f"gcloud auth activate-service-account --key-file=/etc/releai/keys/releai-bot-dev.json",shell=True)
        os.environ['BUCKET_NAME'] = "database_backup_rb"
    if env == "prod":
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/releai/keys/releai-bot-prod.json"
        subprocess.run(f"gcloud auth activate-service-account --key-file=/etc/releai/keys/releai-bot-prod.json",shell=True)
        os.environ['BUCKET_NAME'] = "prod_database_backup_rb"

def create_backup():
    '''
    create a local backup
    '''
    _date, _dir = date_today()
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    for col in collection_list:
        subprocess.run(f'firestore-export -a {os.environ["GOOGLE_APPLICATION_CREDENTIALS"]} -b "{_dir}/{col}.json" -n "{col}"', shell=True)
    return ""

def day_time():
    '''
    defines the time in the day
    '''
    currentTime = datetime.now(pytz.timezone('Asia/Jerusalem'))
    if currentTime.hour <= 12 and currentTime.minute <= 10:
        return 'Morning'
    elif 12 <= currentTime.hour < 16:
        return 'Noon'
    elif 16 <= currentTime.hour < 18:
        return 'AfterNoon'
    elif 18 <= currentTime.hour < 20:
        return 'Evening'
    elif 20 <= currentTime.hour < 23:
        return 'Night'
    elif 23 >= currentTime.hour < 12:
        return 'Morning'
    else:
        return ''

def upload_to_bucket(env):
    '''
    upload the backUp to bucket
    '''
    _date, _dir = date_today()
    env = defines_env(env)
    create_backup()
    storage_client = storage.Client()
    if storage_client.get_bucket(os.environ['BUCKET_NAME']).exists():
        print(f"OK, Found {os.environ['BUCKET_NAME']} bucket")
        if os.path.exists(_dir):
            for col in collection_list:
                subprocess.run(f"gsutil cp {_dir}/{col}.json gs://{os.environ['BUCKET_NAME']}/{_date}/{col}.json", shell=True)
        else:
            print("But I haven't the dir")
        if os.path.exists(_dir):
            print(f"Removing {_dir}")
            shutil.rmtree(_dir)
    return f"https://console.cloud.google.com/storage/browser/{os.environ['BUCKET_NAME']}/{_date}"

def main():
    '''
    function contains async functions
    and the control on the bot from the discord channel.
    '''
    from discord.ext import commands
    bot = commands.Bot(command_prefix='!', case_insensitive=True)
    env = [ "dev", "prod" ]
    user_whitelist = {
        "saar-win": 730022647995432970,
        "matany90": 743017820895576065,
        "gal-shalom": 838308213132230668,
        "elon-salfati": 488619184335618048,
    }

    bot_token = {"saar": f"{os.environ['SAAR_CHANNEL']}", "releai": f"{os.environ['RELEAI_CHANNEL']}"}
    @bot.event
    async def on_ready():
        '''
        bot defines settings
        '''
        if '{0.user}'.format(bot) == "saar-bot#6047":
            os.environ['channel_id'] = '847879602395021322'
            os.environ['backup_ch'] = '780390613891153923'
            os.environ['bot_user_id'] = '847858449060331640'
            os.environ['bot_ch_id'] = '847859994770145290'
            print("saar")
        ##
        elif '{0.user}'.format(bot) == "RELE-BOT#2110":
            os.environ['channel_id'] = '786217757158277143'
            os.environ['backup_ch'] = '786217757158277143'
            os.environ['bot_user_id'] = '834815901676601384'
            print("releai")
        ##
        else:
            exit()
        print('We have logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(message):
        '''
        wait for pm to bot
        '''
        await bot.process_commands(message)
#
    @bot.command(backup="dev/prod", backup1="")
    @commands.dm_only()
    async def backup(ctx, message):
        '''
        Backup to the bucket
        '''
        if message in env:
            if bot.user.id == int(os.environ['bot_user_id']):
                try:
                    channel = bot.get_channel(int(os.environ['backup_ch']))
                    if ctx.author.id in user_whitelist.values():
                        await ctx.send(f"**Ok, Starting to backup {message} env, \nWhen it ready, I'll send a message on backup channel**")
                        _date, _dir = date_today()
                        link = upload_to_bucket(env=message)
                        time_in_day = day_time()
                        await channel.send(f"**Daily Backup ({message.upper()}/{_date}/{time_in_day}) for {ctx.author.name}**\n" + link)
                    else:
                        print(f"Have no access: {ctx.author.name}, {ctx.author.id}")
                        await ctx.send("**Sorry. You dont have permission to use this command.**")
                except Exception as e:
                    print(e)
            else:
                pass
        else:
            print(f"tried to backup unknown env: {message}, name: {ctx.author.name}, id: {ctx.author.id}")
            await ctx.send("**You tried to backup unknown env**")
#
    @bot.event
    async def on_command_error(ctx, error):
        '''
        Bot errors handling
        '''
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.author.send('Sorry. You dont have permission to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            command = ctx.message.content.split()[1]
            await ctx.author.send("Missing an argument: " + command)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.author.send("I don't know this command")
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.author.send("Role 'core' is required to run this command.")

    bot.command(name="backup")
    # bot.run(bot_token.get("saar")) ## Saar channel
    bot.run(bot_token.get("releai")) ## releai channel

if __name__ == '__main__':
    main()
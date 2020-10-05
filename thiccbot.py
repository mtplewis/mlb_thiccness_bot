# Work with Python 3.6
import discord
import mlbgame
import json
import mlbgame.data
import os


# Discord info
TOKEN = os.environ.get('thicc_disc_token')
client = discord.Client()
team_bmis = {}
team_thiccest = {}


def get_team_id(team_name):
    teams = mlbgame.teams()
    for team in teams:
        if team_name in str(team):
            return team.team_id


def roster(team_id):
    """Returns a dictionary of roster information for team id"""
    data = mlbgame.data.get_roster(team_id)
    parsed = json.loads(data.read().decode('utf-8'))
    players = parsed['roster_40']['queryResults']['row']
    return {'players': players, 'team_id': team_id}


def calculate_bmi(weight, height_feet, height_inches):
    # Convert from str to float:
    height_inches = float(height_inches)
    height_feet = float(height_feet)
    weight = float(weight)

    # Convert to meters:
    height_inches += height_feet * 12
    h_cm = round(height_inches * 2.54, 1)
    h_m = h_cm / 100

    # Convert to Kilograms:
    w_kg = weight / 2.2

    # Calculate BMI:
    bmi = round(w_kg / (h_m * h_m), 2)
    return bmi


def Average(lst):
    return sum(lst) / len(lst)


def team_average_bmi(team_name):
    bmis = list()
    team_id = get_team_id(team_name)
    full_roster = roster(team_id)
    for x in full_roster['players']:
        height_inches = x['height_inches']
        height_feet = x['height_feet']
        weight = x['weight']
        bmi = calculate_bmi(weight, height_feet, height_inches)
        bmis.append(bmi)
    average_bmi = Average(bmis)
    average_bmi = round(average_bmi, 3)
    team_bmis[team_name] = average_bmi


def thiccest_boi(team_name):
    bmis = {}
    team_id = get_team_id(team_name)
    full_roster = roster(team_id)
    for x in full_roster['players']:
        height_inches = x['height_inches']
        height_feet = x['height_feet']
        weight = x['weight']
        bmi = calculate_bmi(weight, height_feet, height_inches)
        # name_and_weight = (x['name_display_first_last'], x['weight'])
        name = str(x['name_display_first_last'])
        bmis[name] = bmi
    thiccest = max(bmis.values())
    for x in bmis:
        if bmis[x] == thiccest:
            team_thiccest[team_name] = (x, bmis[x])


def get_thiccest_team():
    thiccest_team = max(team_bmis.values())
    for x in team_bmis:
        if team_bmis[x] == thiccest_team:
            return "The THICCEST team in the MLB is {} with an average BMI of {}. " \
                   "Wow, That's THICC daddy!".format(x, team_bmis[x])


def get_thiccest_man():
    bmis = list()
    for each in team_thiccest.values():
        bmis.append(each[1])
    thiccest_man = max(bmis)
    for each in team_thiccest.values():
        for x in each:
            if each[1] == thiccest_man:
                return "The THICCEST man in the MLB is {} with a BMI of {}. " \
                       "Wow!".format(each[0], each[1])

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        print(message.content)
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        channel = message.channel
        await channel.send(msg)
    elif message.content == 'thicc':
        msg = 'im a thicc boi'
        channel = message.channel
        await channel.send(msg)
    elif message.content.lower() == 'thicc boi help':
        option_message = ("Here are your options:\n"
                          "- Thiccest team in the league\n"
                          "- Thiccest player in the league\n"
                          "- Cutest player in the league\n")
        channel = message.channel
        await channel.send(option_message)
    if message.content.lower() == "thiccest team in the league":
        channel = message.channel
        await channel.send("Calculating each team's rating on the THICC-ter scale...")
        for team in mlbgame.teams():
            team_average_bmi(str(team))
        response = get_thiccest_team()
        await channel.send(response)
    elif message.content.lower() == "thiccest player in the league":
        channel = message.channel
        await channel.send("Calculating each bois thicc rating...")
        for team in mlbgame.teams():
            thiccest_boi(str(team))
        response = get_thiccest_man()
        await channel.send(response)
    # elif message.content.startswith("Thiccest player on"):
    #     team_thiccest = {}
    #     contents = message.content.split("on")
    #     team_name = contents[1]
    #     print(team_name)
    #     teams = mlbgame.teams()
    #     thiccest_boi(team_name)
    #     for boy in team_thiccest:
    #         await client.send_message(message.channel, boy)


    # elif message.content.lower() == "show average team bmis":
    #     await client.send_message(
    #         message.channel, "Calculating each team's rating on the THICC-ter scale...")
    #     for team in mlbgame.teams():
    #         team_average_bmi(str(team))
    #     await client.send_message(
    #         message.channel, "Average Team BMIs:")
    #     for x in team_bmis:
    #         await client.send_message(
    #         message.channel, ("Team:", x, "BMI", team_bmis[x]))
    # elif message.content.lower() == "show thiccest players on all teams":
    #     await client.send_message(
    #         message.channel, "Calculating each bois thicc rating...")
    #     for team in mlbgame.teams():
    #         thiccest_boi(str(team))
    #     await client.send_message(
    #         message.channel, "Thiccest Bois in the LEAGUE:")
    #     for x in team_thiccest:
    #         await client.send_message(
    #             message.channel, ("Team:",
    #               x,
    #               "Thiccest:",
    #               team_thiccest[x][0],
    #               "BMI:",
    #               team_thiccest[x][1]
    #               ))
    elif message.content.lower() == "cutest player in the league":
        channel = message.channel
        await channel.send("The Cutest boi in the league is Willians Astudillo, aka La Tortuga")
        await  channel.send("http://stmedia.stimg.co/ctyp-torguga-chugging.jpg?w=800")



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


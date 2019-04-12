#!/usr/bin/env python3
import mlbgame
import json
import mlbgame.data

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
        pounds = str(x['weight'])
        bmis[name] = bmi
    thiccest = max(bmis.values())
    for x in bmis:
        if bmis[x] == thiccest:
            team_thiccest[team_name] = (x, bmis[x])


def get_thiccest_team():
    thiccest_team = max(team_bmis.values())
    for x in team_bmis:
        if team_bmis[x] == thiccest_team:
            print("The THICCEST team in the MLB is {} with an average BMI of {}. "
                  "Wow, That's THICC daddy!".format(x, team_bmis[x]))


def get_thiccest_man():
    bmis = list()
    for each in team_thiccest.values():
        bmis.append(each[1])
    thiccest_man = max(bmis)
    for each in team_thiccest.values():
        for x in each:
            if each[1] == thiccest_man:
                print("The THICCEST man in the MLB is {} with a BMI of {}. "
                      "Wow!".format(each[0], each[1]))
                return


if __name__ == '__main__':
    while True:
        user_option = input("Choose an option:\n"
                            "1. Thiccest team in the league\n"
                            "2. Thiccest player in the league\n"
                            "3. Show average team BMIs\n"
                            "4. Show thiccest players on all teams\n"
                            "5. Cutest player in the league\n")
        if user_option == "1":
            teams = mlbgame.teams()
            print("Calculating each team's rating on the THICC-ter scale...")
            for team in mlbgame.teams():
                team_average_bmi(str(team))
            get_thiccest_team()
            again = input("Would you like to choose another option? y/n: ")
            if again.lower() == "n":
                break
        elif user_option == "2":
            teams = mlbgame.teams()
            print("Calculating each bois thicc rating...")
            for team in mlbgame.teams():
                thiccest_boi(str(team))
            get_thiccest_man()
            again = input("Would you like to choose another option? y/n: ")
            if again.lower() == "n":
                break
        elif user_option == "3":
            teams = mlbgame.teams()
            print("Calculating each team's rating on the THICC-ter scale...")
            for team in mlbgame.teams():
                team_average_bmi(str(team))
            print("\nAverage Team BMIs:")
            for x in team_bmis:
                print("Team:", x, "BMI", team_bmis[x])
            again = input("Would you like to choose another option? y/n: ")
            if again.lower() == "n":
                break
        elif user_option == "4":
            teams = mlbgame.teams()
            print("Calculating each bois thicc rating...")
            for team in mlbgame.teams():
                thiccest_boi(str(team))
            print("\nThiccest Bois in the LEAGUE:")
            for x in team_thiccest:
                print("Team:",
                      x,
                      "Thiccest:",
                      team_thiccest[x][0],
                      "BMI:",
                      team_thiccest[x][1]
                      )
            again = input("Would you like to choose another option? y/n: ")
            if again.lower() == "n":
                break
        elif user_option == "5":
            print("The Cutest boi in the league is Willians Astudillo, aka La Tortuga")
            again = input("Would you like to choose another option? y/n: ")
            if again.lower() == "n":
                break
        else:
            print("Didn't recognize input, just type a number 1-5 then press enter.")


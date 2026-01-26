import requests

API_KEY = "YOUR_API_KEY" #get one from developer clash of clans
#don't change code below
def get_player_info(player_token):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    url = f"https://api.clashofclans.com/v1/players/{player_token.replace('#', '%23')}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "❌ Player topilmadi yoki token noto‘g‘ri."

    data = response.json()

    player_info = {
        "TAG": data["tag"],
        "NAME": data["name"],
        "TOWN HALL LEVEL": data["townHallLevel"],
        "EXP": data["expLevel"],
        "TROPHIES": data["trophies"],
        "HIGHEST TROPHIES": data["bestTrophies"],
        "WAR STARS": data["warStars"],
        "ATTACKS WON": data["attackWins"],
        "Donations": data["donations"],
        "Clan contributions": data["clanCapitalContributions"],
        "heroes": [{"name": hr["name"], "level": hr["level"]} for hr in data["heroes"]],
        "heroEquipment": [{"name": eq["name"], "level": eq["level"]} for eq in data.get("heroEquipment", [])],
    }

    message = (
        f"🧑‍💻 User info\n"
        f"👤 Username: {player_info['NAME']}, 🆔 ID: {player_info['TAG']}\n"
        f"🏰 Townhall: {player_info['TOWN HALL LEVEL']}, ⭐ EXP: {player_info['EXP']}\n"
        f"🏆 Trophies: {player_info['TROPHIES']} (Best: {player_info['HIGHEST TROPHIES']})\n\n"
        f"⚔️ Clan War\n"
        f"🌟 War stars: {player_info['WAR STARS']}, 🗡️ Attacks won: {player_info['ATTACKS WON']}\n\n"
        f"💪 Contributions\n"
        f"🏹 Clan contributions: {player_info['Clan contributions']}, 🤝 Donations: {player_info['Donations']}\n\n"
        f"🛡️ Heroes:\n"
    )

    for hero in player_info["heroes"]:
        message += f"👑 {hero['name']}: Level {hero['level']}\n"

    if player_info["heroEquipment"]:
        message += "\n🛠️ Hero Equipment:\n"
        for eq in player_info["heroEquipment"]:
            message += f"⚔️ {eq['name']}: Level {eq['level']}\n"

    return message


def clan_war_status(clan_tag):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/{clan_tag.replace('#', '%23')}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Ma'lumotni ololmadik"

    data = response.json()


    clan_status = {
        "Holati": data["state"],
        "Jamoa olchami": data["teamSize"]
    }

    message = (
        f"Holati: {clan_status['Holati']}, Oyinchilan soni: {clan_status['Jamoa olchami']}"
    )

    return message

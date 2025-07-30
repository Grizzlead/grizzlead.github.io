import re
from bs4 import BeautifulSoup
from selenium import webdriver

def info_players(side):
    kda_team = soup_main.select(f'.team-results .{side} tfoot td.r-group-1')
    print(f'\n{side.upper() + ": " + (team_radiant if side == "radiant" else team_dire):35} KDA: {" - ".join(item.text for item in kda_team)}')
    team = soup_main.select(f'.team-results tr.faction-{side}')
    heroes = []
    for player in team:
        lst = []
        lst.append(('name', ' '.join(player.select(f"td.single-lines .player-{side}")[0].text.split())))
        lst.append(('hero', player.select("td.cell-fill-image .tw-w-auto")[0]["alt"]))
        lst.append(('aspect', player.select("td.cell-fill-image .tw-text-center")[0]["alt"]))
        role = player.select('.role-icon')
        lst.append(('role', role[0]["title"] if role[0]["title"] else role[0]["oldtitle"]))
        line = ' '.join([item.text for item in player.select("td.single-lines acronym")])
        lst.append(('line', ' '.join(line.split())))
        kda = player.select(".r-group-1")
        lst.append(('kda', " - ".join(i.text.strip().ljust(2) for i in kda[:-1])))
        lst.append(('gold', float((kda[-1].text.strip())[:-1])))
        heroes.append(dict(lst))

    for player in sorted(heroes, key=lambda x: x['gold'], reverse=True):
        print(f"{player['hero']:20} - {player['role']:15} / {player['kda']} - {str(player['gold']) + 'k':10} / {player['line']:20} / {player['name']:30} / {player['aspect']}")

# SITE ---------------------------------------------------------------------------------------------------------------------------------------
code="8395247968"

driver = webdriver.Chrome()

driver.get(url="https://www.dotabuff.com/matches/" + code)
page_source = driver.page_source

with open('_Парсинг/main.html', 'w', encoding='utf-8') as file:
    file.write(page_source)

driver.quit()
driver = webdriver.Chrome()

driver.get(url="https://www.dotabuff.com/matches/" + code + '/kills')
page_source = driver.page_source

with open('_Парсинг/death_log.html', 'w', encoding='utf-8') as file:
    file.write(page_source)

driver.quit()
driver = webdriver.Chrome()

driver.get(url="https://www.dotabuff.com/matches/" + code + '/objectives')
page_source = driver.page_source

with open('_Парсинг/log_obj.html', 'w', encoding='utf-8') as file:
    file.write(page_source)

driver.quit()
# # SITE ---------------------------------------------------------------------------------------------------------------------------------------

# # FILE ---------------------------------------------------------------------------------------------------------------------------------------
with open('_Парсинг/main.html', 'r', encoding='utf-8') as file:
    html_main = file.read()

soup_main = BeautifulSoup(html_main, 'lxml')

with open('_Парсинг/log_obj.html', 'r', encoding='utf-8') as file:
    html_obj = file.read()

soup_obj = BeautifulSoup(html_obj, 'lxml')

with open('_Парсинг/death_log.html', 'r', encoding='utf-8') as file:
    html_kills = file.read()

soup_kills = BeautifulSoup(html_kills, 'lxml')
# FILE ---------------------------------------------------------------------------------------------------------------------------------------

# 1. Teams
team_radiant = soup_main.select_one('.team-results .radiant header .team-text-full').text
team_dire = soup_main.select_one('.team-results .dire header .team-text-full').text
teams = {'Radiant':team_radiant, 'Dire':team_dire}

# 2. Roshans
print('\nLog Roshans:')
roshans = soup_obj.select("div.line:has(.roshan)")
first_roshan = None
for roshan in roshans:
    lst = roshan.select('.event')[0].text.split()
    side = ('Dire', 'Radiant')[len(roshan.select('.color-faction-radiant'))]
    lst.insert(0, f'({side} - {teams[side]})')
    out = f'{roshan.select(".time")[0].text} {" ".join(lst)}'
    if first_roshan is None:
        first_roshan = out
    print(out)

# 3. Aegis
print('\nLog aegis:')

aegis = soup_obj.select("div.line:has(.aegis-of-the-immortal)")
first_aegis = None
for item in aegis:
    lst = item.text.split()
    side = ('Dire', 'Radiant')[len(item.select('.color-faction-radiant'))]
    lst.insert(1, f'({side} - {teams[side]})')
    out = ' '.join(lst)
    if first_aegis is None:
        first_aegis = out
    print(out)

# 4. Towers
towers = soup_obj.select("div.line:has(.tower)")
print(f'\nLog {len(towers)} destroys towers:')
first_tower = None
for tower in towers:
    lst = tower.select('.event')[0].text.split()
    side = ('Dire', 'Radiant')[len(tower.select('.object.color-faction-radiant'))]
    lst.insert(0, f'({side} - {teams[side]})')
    out = f'{tower.select(".time")[0].text} {" ".join(lst)}'
    if first_tower is None:
        first_tower = out
    print(out)

# 5. Kills
print('\nLog kills:')
kills = soup_kills.select("div.line")
dire_kills, radiant_kills, streaks = 0, 0, []
first_kill, killing_race = None, []
for kill in kills:
    if kill.select('.line .event .gold'):
        tower_kill = kill.find(string=re.compile('Tower'))
        creep_kill = kill.find(string=re.compile('Creep'))
        tormentor_kill = kill.select('span.object img[alt="Reflect"], span.object img[alt="The Shining"]')
        roshan_kill = kill.select('span.object img[alt="Roshan"]')
        suicide_kill = 'suicide' in kill.text
        killer = kill.select('.event a:nth-child(2)')
        killed = kill.select('.event a:nth-child(1)')
        kills = None

        if tower_kill or creep_kill:
            metka, out = '', ''
            if tower_kill == 'Dire Tower' or creep_kill == 'Dire Creep':
                dire_kills += 1
                kills = dire_kills
                if kills in (5, 10, 15, 20) and kills > radiant_kills:
                    metka = f'{kills}=> '
            elif tower_kill == 'Radiant Tower' or creep_kill == 'Radiant Creep':
                radiant_kills += 1
                kills = radiant_kills
                if kills in (5, 10, 15, 20) and kills > dire_kills:
                    metka = f'{kills}=> '
            out = f'{kill.select(".time")[0].text} {metka}***({" ".join(tower_kill.split()) if tower_kill else " ".join(creep_kill.split())})-{kills} kills {killer[0].text.strip()}, assisted by {killed[0].text.strip() if killed else ""}'
            if metka:
                killing_race.append(out)
            print(out)
        elif tormentor_kill:
            print(f'{kill.select(".time")[0].text} ***(Tormentor) kills {killed[0].text.strip()}')
        elif roshan_kill:
            print(f'{kill.select(".time")[0].text} ***(Roshan) kills {killer[0].text.strip()}')
        elif suicide_kill:
            print(f'{kill.select(".time")[0].text} ***(Suicide) kills {killed[0].text.strip()}')
        else:
            side = ('Dire', 'Radiant')["color-faction-radiant" in killer[0].attrs['class']]
            metka, out = '', ''
            if side == 'Dire':
                dire_kills += 1
                kills = dire_kills
                if kills in (5, 10, 15, 20) and kills > radiant_kills:
                    metka = f'{kills}=> '
            else:
                radiant_kills += 1
                kills = radiant_kills
                if kills in (5, 10, 15, 20) and kills > dire_kills:
                    metka = f'{kills}=> '
            out = f'{kill.select(".time")[0].text} {metka}({side} - {teams[side]})-{str(kills)} {killer[0].text.strip()} kills {killed[0].text.strip()}'
            if first_kill is None:
                first_kill = out
            if metka:
                killing_race.append(out)     
            print(out)
    else:
        if len(kill.select('.line .event a')) == 1:
            streaks.append(' '.join(kill.text.split()))

# Info
print(f'\nFirst kill:\n{first_kill}')
print('\nKilling race:')
for race in killing_race:
    print(race)
print(f'\nFirst tower:\n{first_tower}')
print(f'\nFirst aegis:\n{first_aegis}')
print(f'\nFirst Roshan:\n{first_roshan}')
print('\nLog Megacreeps:')
megacreeps = soup_obj.find(string=re.compile('megacreeps'))
print('YES' if megacreeps else 'NO')

# 6. Streaks
print('\nCount streaks:')
for streak in streaks:
    print(streak)

print(f'\nКоличество Рошанов: {len(roshans)}')
print(f'\nКоличество разрушенных башен: {len(towers)}')

# Time and frags
times = soup_main.select('span.duration')
print(f'\nTime of game: {times[0].text}')

# Radiant team
info_players('radiant')

# Dire team
info_players('dire')
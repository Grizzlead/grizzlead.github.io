import re
from bs4 import BeautifulSoup
from selenium import webdriver

def info_players(side):
    kda_team = soup_main.select(f'.team-results .{side} tfoot td.r-group-1')
    print(f'\n{side.upper() + ": " + (team_radiant if side == "radiant" else team_dire):35} KDA: {" - ".join(item.text for item in kda_team)}')
    team = soup_main.select(f'.team-results tr.faction-{side}')
    team_picks = soup_main.select(f'.team-results > .{side} .picks-inline > div')
    for pick in team_picks:
        temp_text = pick.text + ' ' + pick.select('a > img')[0]['alt']
        if 'Pick' in temp_text:
            temp_text = temp_text.upper()
        print(temp_text)
    heroes = []
    for player in team:
        lst = []
        lst.append(('name', ' '.join(player.select(f"td.single-lines .player-{side}")[0].text.split())))
        lst.append(('hero', player.select("td.cell-fill-image .tw-w-auto")[0]["alt"]))
        lst.append(('aspect', player.select("td.cell-fill-image .tw-text-center")[0]["alt"]))
        role = player.select('.role-icon')
        if role:
            lst.append(('role', role[0]["title"] if role[0]["title"] else role[0]["oldtitle"]))
        else:
            lst.append(('role', 'No type'))
        line = ' '.join([item.text for item in player.select("td.single-lines acronym")])
        lst.append(('line', ' '.join(line.split())))
        kda = player.select(".r-group-1")
        lst.append(('kda', " - ".join(i.text.strip().ljust(2) for i in kda[:-1])))
        lst.append(('gold', float((kda[-1].text.strip())[:-1])))
        heroes.append(dict(lst))

    for player in sorted(heroes, key=lambda x: x['gold'], reverse=True):
        print(f"{player['hero']:20} - {player['role']:15} / {player['kda']} - {str(player['gold']) + 'k':10} / {player['line']:20} / {player['name']:30} / {player['aspect']}")

def info_objectives(objective):
    result = []
    lst = objective.select('.event')[0].text.split()
    if 'spawned' not in lst:
        side = ('Dire', 'Radiant')[len(objective.select('.object.color-faction-radiant'))]
        lst.insert(0, f'({side} - {teams[side]})')
    out = f'{objective.select(".time")[0].text} {" ".join(lst)}'
    result.append(out)
    return result

def scrap_site(id):
    driver = webdriver.Chrome()

    driver.get(url="https://www.dotabuff.com/matches/" + id)
    page_source = driver.page_source

    with open('_Парсинг/main.html', 'w', encoding='utf-8') as file:
        file.write(page_source)

    driver.quit()
    driver = webdriver.Chrome()

    driver.get(url="https://www.dotabuff.com/matches/" + id + '/kills')
    page_source = driver.page_source

    with open('_Парсинг/death_log.html', 'w', encoding='utf-8') as file:
        file.write(page_source)

    driver.quit()
    driver = webdriver.Chrome()

    driver.get(url="https://www.dotabuff.com/matches/" + id + '/objectives')
    page_source = driver.page_source

    with open('_Парсинг/log_obj.html', 'w', encoding='utf-8') as file:
        file.write(page_source)

    driver.quit()

# SITE ---------------------------------------------------------------------------------------------------------------------------------------
# code="8451671758"

# scrap_site(code)
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

# 2. Objectives
objectives = soup_obj.select(f"div.line")
info_roshans, info_aegis, info_towers, info_barracks, info_rune_wisdom, info_active_rune = [], [], [], [], [], []
for obj in objectives:
    if obj.select('.roshan'):
        info_roshans.append(info_objectives(obj))
    elif obj.select('.aegis-of-the-immortal'):
        info_aegis.append(info_objectives(obj))
    elif obj.select('.tower'):
        info_towers.append(info_objectives(obj))
    elif obj.select('.barracks'):
        info_barracks.append(info_objectives(obj))
    elif obj.select('.rune-wisdom'):
        temp = info_objectives(obj)
        if 'spawned' not in temp[0]:
            info_rune_wisdom.append(temp)
    elif obj.select('.rune-haste, .rune-invisibility, .rune-shield, .rune-double-damage, .rune-illusion, .rune-regeneration, .rune-arcane'):
        info_active_rune.append(info_objectives(obj))

# 2.1 Roshans
print('\nLog Roshans:')
for roshan in info_roshans:
    print(*roshan)

# 2.2. Aegis
print('\nLog aegis:')
for aegis in info_aegis:
    print(*aegis)

# 2.3. Towers
print(f'\nLog {len(info_towers)} destroys towers:')
for tower in info_towers:
    print(*tower)

# 2.4. Barracks
print(f'\nLog {len(info_barracks)} destroys barracks:')
for barrack in info_barracks:
    print(*barrack)

# 2.5. Rune wisdom
print(f'\nLog rune wisdom:')
for rune_wisdom in info_rune_wisdom:
    print(*rune_wisdom)

# 2.6. Active rune
print(f'\nLog active rune:')
for active_rune in  info_active_rune:
    print(*active_rune)

# 3. Kills
print('\nLog kills:')
kills = soup_kills.select("div.line")
dire_kills, radiant_kills, multi_kill, beyond_godlike, streaks = 0, 0, [], [], {}
first_kill, killing_race = None, []
for kill in kills:
    kill_events = kill.select('.event > a.color-faction-dire, .event > a.color-faction-radiant')
    if kill.select('.line .event .gold'):
        tower_kill = kill.find(string=re.compile('Tower'))
        creep_kill = kill.find(string=re.compile('Creep'))
        tormentor_kill = kill.select('span.object img[alt="Reflect"], span.object img[alt="The Shining"]')
        roshan_kill = kill.select('span.object img[alt="Roshan"]')
        suicide_kill = 'suicide' in kill.text
        
        killed = kill_events[0].select('img')
        killed = killed[0]['alt']
        if len(kill_events) > 1:
            killer = kill_events[1].select('img')
            killer = killer[0]['alt']
        else:
            killer = ''
        kills = '*'

        if tower_kill or creep_kill:
            metka, out = '', ''
            if len(kill_events) < 3:
                streaks[killer] = streaks.get(killer, 0) + 1
                streaks[killed] = 0
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
            count_kills = "-" + str(dire_kills + radiant_kills) + "- " if not ((dire_kills + radiant_kills) % 10) else ""
            out = f'{kill.select(".time")[0].text} {metka}{count_kills}***({" ".join(tower_kill.split()) if tower_kill else " ".join(creep_kill.split())})-{kills} kills {killed}, assisted by {killer if killer else ""}'
            if metka:
                killing_race.append(out)
            if killed in streaks and streaks[killed] > 9:
                beyond_godlike.append(out)
            print(out)
        elif tormentor_kill:
            print(f'{kill.select(".time")[0].text} ***(Tormentor) kills {killed}')
        elif roshan_kill:
            print(f'{kill.select(".time")[0].text} ***(Roshan) kills {killer}')
        elif suicide_kill:
            print(f'{kill.select(".time")[0].text} ***(Suicide) kills {killed}')
        else:
            side = ('Dire', 'Radiant')["color-faction-radiant" in kill_events[1].attrs['class']]
            metka, out = '', ''
            streaks[killer] = streaks.get(killer, 0) + 1
            streaks[killed] = 0
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
            count_kills = "-" + str(dire_kills + radiant_kills) + "- " if not ((dire_kills + radiant_kills) % 10) else ""
            out = f'{kill.select(".time")[0].text} {metka}{count_kills}({side} - {teams[side]})-{str(kills)} {killer}(#{streaks[killer]}) kills {killed}'
            if first_kill is None:
                first_kill = out
            if metka:
                killing_race.append(out)    
            if streaks[killer] > 9:
                beyond_godlike.append(out)
            print(out)
    else:
        if len(kill.select('.line .event a')) == 1:
            multi_kill.append(' '.join(kill.text.split()))

# 4. Info
print(f'\nFirst kill:\n{first_kill}')
print('\nKilling race:')
for race in killing_race:
    print(race)
print(f'\nFirst tower:\n{info_towers[0][0]}')
print(f'\nFirst aegis:\n{info_aegis[0][0] if info_aegis else "No kill Roshan"}')
print(f'\nFirst Roshan:\n{info_roshans[0][0] if info_roshans else "No kill Roshan"}')
print('\nLog Megacreeps:')
megacreeps = soup_obj.find(string=re.compile('megacreeps'))
print('YES' if megacreeps else 'NO')

# 5. Streaks
log_ultrakill = 'NO'
print('\nCount streaks:')
for streak in multi_kill:
    if '5x' in streak:
        log_ultrakill = 'RAMPAGE'
    elif '4x' in streak:
        log_ultrakill = 'YES'
    print(streak)

print(f'Beyond Godlike: \n{("NO","YES")[len(beyond_godlike)>0]}')
for streak in beyond_godlike:
    print(streak)
print(f'\nLog Ultrakill: \n{log_ultrakill}')

print(f'\nКоличество Рошанов: {len(info_roshans)}')
print(f'\nКоличество разрушенных башен: {len(info_towers)}')

# Time and frags
times = soup_main.select('span.duration')
print(f'\nTime of game: {times[0].text}')

# Radiant team
info_players('radiant')

# Dire team
info_players('dire')

print(streaks)
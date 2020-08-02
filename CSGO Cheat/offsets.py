import requests, re, math

r = requests.get("https://raw.githubusercontent.com/JokinAce/CSGO-Offsets/master/csgo.hpp")
r = r.text


offsets = ["dwEntityList", "dwLocalPlayer","m_flFlashMaxAlpha", "m_iTeamNum", "dwGlowObjectManager", "m_iGlowIndex", "dwForceJump", "m_fFlags", "dwForceAttack", "m_iCrosshairId", "m_bSpotted", "m_iShotsFired", "m_aimPunchAngle", "dwClientState", "dwClientState_ViewAngles","m_iObserverMode"]


d = {}
offs = []
for i in range(len(offsets)):
    if offsets[i] in r:
        search = re.findall(str(offsets[i]) + '\s'"= (.*);", r)
        offs += search


i = 0
while i <= len(offsets)-1:
    (key, val) = offsets[i], offs[i]
    d[key] = val
    i += 1

dwEntityList = int(d["dwEntityList"], base = 16)
dwLocalPlayer = int(d["dwLocalPlayer"], base = 16)
m_flFlashMaxAlpha = int(d["m_flFlashMaxAlpha"], base = 16)
m_iTeamNum = int(d["m_iTeamNum"], base = 16)
dwGlowObjectManager = int(d["dwGlowObjectManager"], base = 16)
m_iGlowIndex = int(d["m_iGlowIndex"], base = 16)
dwForceJump = int(d["dwForceJump"], base = 16)
m_fFlags = int(d["m_fFlags"], base = 16)
dwForceAttack = int(d["dwForceAttack"], base = 16)
m_iCrosshairId = int(d["m_iCrosshairId"], base = 16)
m_bSpotted = int(d["m_bSpotted"], base = 16)
m_iShotsFired = int(d["m_iShotsFired"], base = 16)
m_aimPunchAngle = int(d["m_aimPunchAngle"], base = 16)
dwClientState = int(d["dwClientState"], base = 16)
dwClientState_ViewAngles = int(d["dwClientState_ViewAngles"], base = 16)
m_iObserverMode = int(d["m_iObserverMode"], base = 16)
m_iDefaultFOV = (0x332C)

m_totalHitsOnServer = (0xA3A8)

def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
     
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey

def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    try:
        delta_x = localpos1 - enemypos1
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except:
        pass

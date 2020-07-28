import requests, re, math

r = requests.get("https://raw.githubusercontent.com/JokinAce/CSGO-Python-Pymem-Cheat-Hack/master/csgo.hpp?token=ANWTVITBFMELXF2IGF24LJC7EAU66") #Link to mine
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

import pymem, keyboard, time, os, configparser, winsound
from colorama import Fore, init
from offsets import m_bGunGameImmunity, normalizeAngles, checkangles, nanchecker, dwEntityList, dwLocalPlayer, m_flFlashMaxAlpha, m_iTeamNum, dwGlowObjectManager, m_iGlowIndex, dwForceJump, m_fFlags, dwForceAttack, m_iCrosshairId, m_bSpotted, m_iShotsFired, m_aimPunchAngle, dwClientState, dwClientState_ViewAngles, m_iObserverMode, m_iDefaultFOV, m_totalHitsOnServer, m_bIsDefusing
init()

def Main():
    enablessep = False
    enableflasje = False
    enabrad = False
    enablfov = False
    enablereco = False
    enabltp = False

    oldpunchx = 0.0
    oldpunchy = 0.0

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    antivac = "!1Li%yMx8sy#a2513I$rv@aS4GSVq5*DWH&UVMsTcsV^!s6%Ia#UL#y9s3P*fymZRM*q8*RO2HpNsyP5j1TeUjhDaIiae2vJv"
        # Edit every week so Hash of the file changes
    print(antivac)
    config = configparser.ConfigParser()
    try:
        config.read("config.ini")
        mainconfig = config["MAIN"]
        eteam = mainconfig.getboolean("eteam")
        gekey = mainconfig["gekey"]
        nfkey = mainconfig["nfkey"]
        rckey = mainconfig["rckey"]
        triggerkey = mainconfig["triggerkey"]
        rskey = mainconfig["rskey"]
        cfkey = mainconfig["cfkey"]
        customfov = int(mainconfig["customfov"])
        tpkey = mainconfig["tpkey"]
        hss = mainconfig["hss"]
        logeverything = mainconfig.getboolean("logeverything")
    except:
        print("Config could not load properly.")
        time.sleep(5)
        pass

    os.system("cls")
    print(Fore.LIGHTBLUE_EX + "CSGO Multi-Hack | AlphaWolf # JokinAce")
    print("-----------------------------------------------")
    print(gekey + " = GlowESP (Toggle)")
    print(rckey + " = RadarCheat (Toggle)")
    print(nfkey + " = NoFlash (Toggle)")
    print(cfkey + " = CustomFOV (Toggle)")
    print(rskey + " = RecoilSystem (Toggle)")
    print(tpkey + " = ThirdPerson (Toggle)")
    print(triggerkey + " = TriggerBot (Hold)")
    print("Space = Bhop (On)")
    print("---------------------------")
    print("Console:")

    while True:
        #MANAGER
        if client and engine and pm:
            try:
                player = pm.read_int(client + dwLocalPlayer)
                hitshit = pm.read_int(player + m_totalHitsOnServer)
                engine_pointer = pm.read_int(engine + dwClientState)
                glow_manager = pm.read_int(client + dwGlowObjectManager) 
                crosshairID = pm.read_int(player + m_iCrosshairId) 
                getTarget = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
                immunitygunganme = pm.read_int(getTarget + m_bGunGameImmunity)
                localTeam = pm.read_int(player + m_iTeamNum)
                crosshairTeam = pm.read_int(getTarget + m_iTeamNum)
            except:
                print("Round not started yet")
                time.sleep(5)

        #GlowESP
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity and enabrad == True:
                pm.write_uchar(entity + m_bSpotted, 1)
            elif entity and enabrad == False:
                pm.write_uchar(entity + m_bSpotted, 0)

            if entity:
                entity_glow = pm.read_int(entity + m_iGlowIndex)   
                entity_team_id = pm.read_int(entity + m_iTeamNum)

                entity_isdefusing = pm.read_int(entity + m_bIsDefusing)
                if entity_isdefusing and localTeam != 3:
                    winsound.PlaySound(hss, winsound.SND_FILENAME)
                    # Countdown
                    time.sleep(1)
                    if logeverything:
                        print("Bomb is geting defused")

                if entity_team_id == 2 and (eteam == True or localTeam != 2): #Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    if enablessep == True:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enable
                    else:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)

                elif entity_team_id == 3 and (eteam == True or localTeam != 3): #Anti Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    if enablessep == True:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enable
                    else:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)

        #TRIGE
        if keyboard.is_pressed(triggerkey):
            if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam and immunitygunganme == 0:
                pm.write_int(client + dwForceAttack, 6)
                if logeverything:
                    print("TriggerBot | Shot")

        #KEYBOARD SHORTCUTS

        if keyboard.is_pressed(gekey):
            enablessep = not enablessep
            time.sleep(0.2)
            print("GlowESP | " + str(enablessep))

        if keyboard.is_pressed(rckey):
            enabrad = not enabrad
            time.sleep(0.2)
            print("RadarCheat | " + str(enabrad))

        #BHOP
        if keyboard.is_pressed("space"):
            force_jump = client + dwForceJump
            on_ground = pm.read_int(player + m_fFlags)
            if player and on_ground and on_ground == 257:
                pm.write_int(force_jump, 5)
                time.sleep(0.08)
                pm.write_int(force_jump, 4)
                if logeverything:
                    print("BHop | hopped")

        #FLASH CONTROL
        if keyboard.is_pressed(nfkey) and player:
            enableflasje = not enableflasje
            time.sleep(0.2)
            print("NoFlash | " + str(enableflasje))

            flashshit = player + m_flFlashMaxAlpha

            if enableflasje == True:
                pm.write_float(flashshit, float(0))
            else:
                pm.write_float(flashshit, float(255))

        if keyboard.is_pressed(cfkey):
            enablfov = not enablfov
            time.sleep(0.2)
            print("CustomFOV | " + str(enablfov))

            fovshit = player + m_iDefaultFOV

            if enablfov == True:
                pm.write_int(fovshit, customfov)
            else:
                pm.write_int(fovshit, 90)

        if keyboard.is_pressed(rskey):
            enablereco = not enablereco
            time.sleep(0.2)
            print("RecoilSystem | " + str(enablereco))

        if enablereco:
            if pm.read_int(player + m_iShotsFired) > 2:
                rcs_x = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                rcs_y = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                punchx = pm.read_float(player + m_aimPunchAngle)
                punchy = pm.read_float(player + m_aimPunchAngle + 0x4)
                newrcsx = rcs_x - (punchx - oldpunchx) * 2
                newrcsy = rcs_y - (punchy - oldpunchy) * 2
                oldpunchx = punchx
                oldpunchy = punchy
                if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):
                    pm.write_float(engine_pointer + dwClientState_ViewAngles, newrcsx)
                    pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, newrcsy)
                    if logeverything:
                        print("RecoilSystem | Setting Angle")
            else:
                oldpunchx = 0.0
                oldpunchy = 0.0
                newrcsx = 0.0
                newrcsy = 0.0

        if keyboard.is_pressed(tpkey):
            enabltp = not enabltp
            time.sleep(0.2)
            print("ThirdPerson | " + str(enabltp))

            if enabltp == True:
                pm.write_int(player + m_iObserverMode, 1)
            else:
                pm.write_int(player + m_iObserverMode, 0)

        if hitshit > 0:
            pm.write_int(player + m_totalHitsOnServer, 0)
            winsound.PlaySound(hss, winsound.SND_FILENAME)
            if logeverything:
                print("HitSound | Played")

    
if __name__ == "__main__":
    Main()

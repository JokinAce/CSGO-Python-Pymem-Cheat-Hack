import pymem, keyboard, time, os, configparser, winsound, mouse
from colorama import Fore, init
from offsets import calcangle, calc_distance, normalizeAngles, checkangles, nanchecker, dwEntityList, dwLocalPlayer, m_flFlashMaxAlpha, m_iTeamNum, dwGlowObjectManager, m_iGlowIndex, dwForceJump, m_fFlags, dwForceAttack, m_iCrosshairId, m_bSpotted, m_iShotsFired, m_aimPunchAngle, dwClientState, dwClientState_ViewAngles, m_iObserverMode, m_iDefaultFOV, m_totalHitsOnServer, m_bIsDefusing, m_bGunGameImmunity, m_iHealth, m_dwBoneMatrix, m_vecOrigin, m_vecViewOffset, m_bDormant, dwbSendPackets
init()

def Main():
    enablessep = False
    enableflasje = False
    enabrad = False
    enablfov = False
    enablereco = False
    enabltp = False
    testdontenable = False

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
        abkey = mainconfig["abkey"]
        aimfov = int(mainconfig["aimfov"])
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
        time.sleep(10)
        exit()

    os.system("cls")
    print(Fore.LIGHTBLUE_EX + "CSGO Multi-Hack | AlphaWolf # JokinAce")
    print("--------------------------[AIMBOT]--------------------------")
    print(abkey + " = Aimbot (Hold)")
    print(triggerkey + " = TriggerBot (Hold)")
    print(rskey + " = RecoilSystem (Toggle)")
    print("--------------------------[VISION]--------------------------")
    print(gekey + " = GlowESP (Toggle)")
    print(rckey + " = RadarCheat (Toggle)")
    print(nfkey + " = NoFlash (Toggle)")
    print(cfkey + " = CustomFOV (Toggle)")
    print(tpkey + " = ThirdPerson (Toggle)")
    print("--------------------------[MISC]----------------------------")
    print("Space = Bhop (On)")
    print("---------------------------")
    print("Console:")

    while True:
        if testdontenable:
            pm.write_uchar(engine + dwbSendPackets, 0)
            time.sleep(0.1)
            pm.write_uchar(engine + dwbSendPackets, 1)
                        
        target = None
        olddistx = 111111111111
        olddisty = 111111111111
        #MANAGER
        if client and engine and pm:
            try:
                player = pm.read_int(client + dwLocalPlayer)
                hitshit = pm.read_int(player + m_totalHitsOnServer)
                engine_pointer = pm.read_int(engine + dwClientState)
                glow_manager = pm.read_int(client + dwGlowObjectManager) 
                crosshairID = pm.read_int(player + m_iCrosshairId) 
                getcrosshairTarget = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
                immunitygunganme = pm.read_int(getcrosshairTarget + m_bGunGameImmunity)
                localTeam = pm.read_int(player + m_iTeamNum)
                crosshairTeam = pm.read_int(getcrosshairTarget + m_iTeamNum)
            except:
                print("Round not started yet")
                time.sleep(5)
                continue

        #GlowESP
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                try:
                    entity_glow = pm.read_int(entity + m_iGlowIndex)
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_isdefusing = pm.read_int(entity + m_bIsDefusing)
                    entity_hp = pm.read_int(entity + m_iHealth)
                    entity_dormant = pm.read_int(entity + m_bDormant)
                except:
                    print("Could not load Players Infos (Should only do this once)")
                    time.sleep(2)
                    continue

                if entity_hp > 50 and not entity_hp == 100:
                	r,g,b = 255,165,0
                elif entity_hp < 50:
                	r,g,b = 255,0,0
                elif entity_hp == 100 and entity_team_id == 2:
                	r,g,b = 0,255,255
                else:
                	r,g,b = 0,0,255

                if keyboard.is_pressed(abkey) or mouse.is_pressed(abkey) and player:
                    if localTeam != entity_team_id and entity_hp > 0:
                        entity_bones = pm.read_int(entity + m_dwBoneMatrix)
                        localpos_x_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                        localpos_y_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                        localpos1 = pm.read_float(player + m_vecOrigin)
                        localpos2 = pm.read_float(player + m_vecOrigin + 4)
                        localpos_z_angles = pm.read_float(player + m_vecViewOffset + 0x8)
                        localpos3 = pm.read_float(player + m_vecOrigin + 8) + localpos_z_angles
                        entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xC)
                        entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1C)
                        entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2C)
                        X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                        newdist_x, newdist_y = calc_distance(localpos_x_angles, localpos_y_angles, X, Y)
                        if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= aimfov and newdist_y <= aimfov:
                            olddistx, olddisty = newdist_x, newdist_y
                            target, target_hp, target_dormant = entity, entity_hp, entity_dormant
                            target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z
                    if target and target_hp > 0 and not target_dormant:
                        x, y = calcangle(localpos1, localpos2, localpos3, target_x, target_y, target_z)
                        normalize_x, normalize_y = normalizeAngles(x, y)
                        pm.write_float(engine_pointer + dwClientState_ViewAngles, normalize_x)
                        pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y)

                if enabrad == True:
                    pm.write_int(entity + m_bSpotted, 1)

                if entity_isdefusing and localTeam != 3 and not entity_dormant:
                    winsound.PlaySound(hss, winsound.SND_FILENAME)
                    # Countdown
                    #time.sleep(1)
                    if logeverything:
                        print("Bomb is geting defused")

                if entity_team_id == 2 and (eteam or localTeam != 2) and not entity_dormant: #Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    if enablessep == True:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enable
                    else:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)

                elif entity_team_id == 3 and (eteam or localTeam != 3) and not entity_dormant: #Anti Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    if enablessep == True:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enable
                    else:
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)
        #TRIGE
        if keyboard.is_pressed(triggerkey) and crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam and immunitygunganme == 256:
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
            if player and on_ground and on_ground == 257 or on_ground == 263:
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

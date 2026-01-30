import numpy as np
import pandas as pd
from ecoengine import getWeatherStations, EcosizerEngine, getListOfModels, SimulationRun, getAnnualSimLSComparison, PrefMapTracker, UtilityCostTracker, get_oat_buckets, getSizingCurvePlot, createSizingCurvePlot
import time
import math
from plotly.offline import plot
from plotly.graph_objs import Figure, Scatter
import os


from ecoengine.engine.BuildingCreator import createBuilding
from ecoengine.engine.SystemCreator import createSystem
from ecoengine import SimulationRun



# hpwh = EcosizerEngine(
#             #incomingT_F = 0, #not needed, weather weather file inlet temp is used
#             magnitudeStat = 255, #seems to be used as number of people?
#             supplyT_F = 122,
#             storageT_F = 160, #150
#             percentUseable = 0.85, #NEED
#             aquaFract = 0.40,
#             #aquaFractLoadUp = 0.04,
#             #aquaFractShed = 0.79,
#             #loadUpT_F = 170, #150
#             #loadUpHours = 2,
#             schematic = "primary",
#             buildingType  = "multi_family",
#             gpdpp = 32.5,
#             nApt = 98,
#             Wapt = 167,
#             #loadShiftSchedule = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1],
#             doLoadShift=False,
#             #doLoadShift   = True,
#             climateZone=15, # Overwrote OAT DB and incoming water temp for CZ 15 to be NYC TMYx added into .csv files by Chris Lyle
#             annual=False,
#             systemModel='MODELS_ColmacCxV_5_C_SP',
#             PVol_G_atStorageT=2300,
#             numHeatPumps=7,
#             #TMCap_kW=40, #IS THIS TRUE?
#             #TMVol_G=500,  
#         )

## ****************Neale's initial test code ********************
# simResults = hpwh.getSimResult(
#     #initPV = 30, #Primary volume at start of the simulation
#     #initST = 110, #Swing tank temperature at start of the simulation.
#     minuteIntervals = 60,
#     nDays = 365,
#     #kWhCalc = True, #set to true to add the kgCO2/kWh calculation to the result.
#     #kGDiff = True, #set to True if you want to include the kGCO2/kWh saved in the result. Will also include loadshift capacity. Only available for loadshifting systems with annual loadshapes
#     #optimizeNLS = True #set to True to optimize non-loadshift sizing. Only applies if kGDiff = True
#     )

# pV = simResults[0]
# hwGen = simResults[1]
# hwDemand = simResults[2]
# pGen = simResults[3]

#*****************************************************


# ********Chris Test Code *************

# simRun1 = hpwh.getSimRun(initPV=2000, initST=160, minuteIntervals=60, nDays=365,exceptOnWaterShortage=True)

# # Export all results to CSV with headers
# simRun1.writeCSV("simulation_results_hourly.csv")
# print("Results saved to simulation_results_hourly.csv")

# ***********************************

building = createBuilding(
    incomingT_F=44,           # float: Incoming city water temperature on the design day [°F]
    magnitudeStat=255,         # int or list: Value used to assess building magnitude based on type
    supplyT_F=122,             # float: Hot water supply temperature [°F]
    buildingType="multi_family",          # str or list: Type of building (e.g., "multi_family", "office_building")
    loadshape=None,        # ndarray: Optional, defaults to design load shape for building type
    avgLoadshape=None,     # ndarray: Optional, defaults to average load shape for building type
    returnT_F=115,           # float: Water temperature returning from recirculation loop [°F]
    flowRate=16,            # float: Pump flow rate of the recirculation loop (GPM)
    gpdpp=31,               # float: Gallons per day per person at 120°F
    nBR=None,              # array_like: List of unit counts by bedroom size [0BR, 1BR, ..., 5BR]
    nApt=98,                # int: Number of apartments (used for multi-family buildings)
    Wapt=167,                # float: Watts of heat lost in recirculation piping system
    standardGPD=None,      # str: Optional, standard gpdpp spec for multi-family buildings
    annual=True,          # bool: Use annual loadshape for multi-family buildings
    #zipCode=None,          # int: California ZIP code to determine climate zone
    climateZone=15,      # int: California climate zone
    ignoreRecirc=False,    # bool: Set True if recirculation losses are irrelevant
    designOAT_F=13       # float: Design outdoor air temperature for the building
)


system = createSystem(
    schematic='singlepass_rtp',               # str: Schematic type ('swingtank', 'paralleltank', 'multipass', 'primary')
    storageT_F=160,              # float: Hot water storage temperature [°F]
    defrostFactor=1,           # float: Multiplier to account for defrost in final heating capacity
    percentUseable=0.85,          # float: Fraction of storage volume usable for hot water
    compRuntime_hr=16,          # float: Compressor runtime on design day [hr]
    aquaFract=0.4,               # float: Height fraction of tank where Aquastat is located
    building=building,           # Building: Optional Building object to associate with the system
    doLoadShift=False,       # bool: Enable load shifting
    #aquaFractLoadUp=None,    # float: Height fraction for load-up Aquastat
    #aquaFractShed=None,      # float: Height fraction for shed Aquastat
    #loadUpT_F=None,          # float: Storage temp between normal and load-up Aquastat [°F]
    #loadShiftPercent=1,      # float: Percent of days load shift will be met
    #loadShiftSchedule=None,  # array_like: 0/1 list for load shifting schedule (0 = off)
    #loadUpHours=None,        # float: Hours spent loading up before first shed
    safetyTM=1.75,           # float: Safety factor for temperature maintenance system
    setpointTM_F=150,        # float: Setpoint for temperature maintenance tank [°F]
    TMonTemp_F=140,          # float: Temp where parallel loop tank turns on [°F]
    offTime_hr=0.333,        # int: Max hours/day temp maintenance equipment can run
    #PVol_G_atStorageT=None,  # float: Pre-sized system storage volume at storage temp [gal]
    #PCap_kBTUhr=None,        # float: Pre-sized system output capacity [kBTU/hr]
    #TMVol_G=None,            # float: Temp maintenance system volume [gal]
    #TMCap_kBTUhr=None,       # float: Temp maintenance system output capacity [kBTU/hr]
    #systemModel=None,        # str: Model name of HPWH for primary system
    #numHeatPumps=None,       # int: Number of heat pumps in primary system
    #tmModel=None,            # str: Model name of HPWH for temp maintenance system
    #tmNumHeatPumps=None,     # int: Number of heat pumps in temp maintenance system
    #inletWaterAdjustment=None,  # float: Adjustment factor for inlet water temp
    ignoreShortCycleEr=False,   # bool: Ignore short cycling errors
    useHPWHsimPrefMap=True,    # bool: Use HPWHsim performance map if available
    #sizeAdditionalER=True,      # bool: Size additional ER element for swingtank_er schematic
    #additionalERSaftey=1.0      # float: Safety factor for additional ER sizing
)


hpwh = EcosizerEngine(
            #incomingT_F = 0, #not needed, weather weather file inlet temp is used
            magnitudeStat = 255, #seems to be used as number of people?
            supplyT_F = building.supplyT_F,
            storageT_F = system.storageT_F, #150
            percentUseable = system.percentUseable, #NEED
            aquaFract = system.aquaFract,
            #aquaFractLoadUp = 0.04,
            #aquaFractShed = 0.79,
            #loadUpT_F = 170, #150
            #loadUpHours = 2,
            schematic = "singlepass_rtp",
            buildingType = "multi_family",
            gpdpp = 31,
            nApt = 98,
            Wapt = 167,
            #loadShiftSchedule = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            doLoadShift=False,
            #doLoadShift   = True,
            climateZone=building.climateZone , # Overwrote OAT DB and incoming water temp for CZ 15 to be NYC TMYx added into .csv files by Chris Lyle
            annual=True,
            systemModel='MODELS_ColmacCxV_5_C_SP',
            PVol_G_atStorageT=2000,
            numHeatPumps=7,
            #TMCap_kW=40, #IS THIS TRUE?
            #TMVol_G=500,  
        )

initPV=hpwh.getSizingResults()[0]
simRun1 = hpwh.getSimRun(initPV=initPV, initST=160, minuteIntervals=60, nDays=365,exceptOnWaterShortage=True)
#df = pd.DataFrame(simRun1.)  # or simRun1.hourlyResults if that's the attribute
simRun1.writeCSV("simulation_results_hourly.csv")
print("Results saved to simulation_results_hourly.csv")
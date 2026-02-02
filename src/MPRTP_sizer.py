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
from ecoengine.constants.Constants import W_TO_BTUHR
from ecoengine import SimulationRun





building = createBuilding(
    incomingT_F=44,           # float: Incoming city water temperature on the design day [°F]
    magnitudeStat=297,         # int or list: Value used to assess building magnitude based on type. For MF this appears to be total occupants.
    gpdpp=31,               # float: Gallons per day per person at 120°F
    standardGPD=None,      # str: Optional, standard gpdpp spec for multi-family buildings
    
    supplyT_F=122,             # float: Hot water supply temperature [°F]
    buildingType="multi_family",          # str or list: Type of building (e.g., "multi_family", "office_building")
    
    #You can only use the below parameters for MF buildings and when not using MPRTP schematic.
    #nApt=111,                # int: Number of apartments (used for multi-family buildings)
    #Wapt=134,                # float: Watts of heat lost in recirculation piping system
    #nBR=None,              # array_like: List of unit counts by bedroom size [0BR, 1BR, ..., 5BR]
    
    returnT_F=115,           # float: Water temperature returning from recirculation loop [°F]
    flowRate=15,            # float: Pump flow rate of the recirculation loop (GPM)
    ignoreRecirc=False,    # bool: Set True if recirculation losses are irrelevant
    
    #loadshape=None,        # ndarray: Optional, defaults to design load shape for building type
    #avgLoadshape=None,     # ndarray: Optional, defaults to average load shape for building type

    annual=True,          # bool: Use annual loadshape for multi-family buildings
    #zipCode=None,          # int: California ZIP code to determine climate zone
    climateZone=15,      # int: California climate zone - now NYC zone 15 [jan 2026 - is this still true?]
    designOAT_F=13       # float: Design outdoor air temperature for the building
)


system = createSystem(
    schematic='mprtp',               # str: Schematic type ('swingtank', 'paralleltank', 'multipass', 'primary')
    storageT_F=160,              # float: Hot water storage temperature [°F]
    defrostFactor=1,           # float: Multiplier to account for defrost in final heating capacity
    compRuntime_hr=16,          # float: Compressor runtime on design day [hr]. 16 is default, best to leave it there.
    percentUseable=0.85,          # float: he fraction of the storage volume that can be filled with hot water.
    onFract=0.16,               # float: The fraction of the total height of the primary hot water tanks at which the ON temperature sensor is located.
    # restrictions: onFract > (1-percentUseable)
    
    #offFract=None,          # float: The fraction of the total height of the primary hot water tanks at which the OFF temperature is located (defaults to onFract if not specified)
    #onT=None,               # float: The temperature detected at the onFract at which the HPWH system will be triggered to turn on. (defaults to supplyT_F if not specified)
    #offT=None,              # float: The temperature detected at the offFract at which the HPWH system will be triggered to turn off. (defaults to storageT_F if

    building=building,           # Building: Optional Building object to associate with the system
    doLoadShift=False,       # bool: Enable load shifting
    


    safetyTM=1.75,           # float: Safety factor for temperature maintenance system
    setpointTM_F=140,        # float: Setpoint for temperature maintenance tank [°F]
    TMonTemp_F=130,          # float: Temp where parallel loop tank turns on [°F]
    offTime_hr=0.333,        # int: Max hours/day temp maintenance equipment can run
    #PVol_G_atStorageT=None,  # float: Pre-sized system storage volume at storage temp [gal]
    #PCap_kBTUhr=None,        # float: Pre-sized system output capacity [kBTU/hr]
    #TMVol_G=None,            # float: Temp maintenance system volume [gal]
    #TMCap_kBTUhr=None,       # float: Temp maintenance system output capacity [kBTU/hr]
    #systemModel=None,        # str: Model name of HPWH for primary system
    #numHeatPumps=None,       # int: Number of heat pumps in primary system
    #tmModel=None,            # str: Model name of HPWH for temp maintenance system
    #tmNumHeatPumps=None,     # int: Number of heat pumps in temp maintenance system
    
    #ignoreShortCycleEr=False,   # bool: Ignore short cycling errors
    useHPWHsimPrefMap=True,    # bool: Use HPWHsim performance map if available
    #sizeAdditionalER=True,      # bool: Size additional ER element for swingtank_er schematic
    #additionalERSaftey=1.0      # float: Safety factor for additional ER sizing
)



pvol_m, pcap_m_kBTUhr, recirc_cap_kBTUhr = system.getSizingResults()

print(
    "mprtp sizing results:",
    f"PVol_G_atStorageT={pvol_m}, PCap_kBTUhr={pcap_m_kBTUhr}, Recirc_Cap_kBTUhr={recirc_cap_kBTUhr}",
)

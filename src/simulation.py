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

hpwh = EcosizerEngine(
            #incomingT_F = 0, #not needed, weather weather file inlet temp is used
            magnitudeStat = 297, #seems to be used as number of people?
            supplyT_F = building.supplyT_F,
            storageT_F = system.storageT_F,
            percentUseable = system.percentUseable, #NEED
            onFract = system.onFract,
            #offFract =   #optional
            schematic = "mprtp",
            buildingType = "multi_family",
        
            gpdpp = 31,
            nApt = 111,
            Wapt = 134,
            
            doLoadShift=False,
            #doLoadShift   = True,
            climateZone=15 , # NYC TMYx data updated for zone 15
            annual=True,
            systemModel='MODELS_ColmacCxV_15_VFD_60_Hz_C_MP',
            
            PVol_G_atStorageT=3000,
            numHeatPumps=5,
            #TMCap_kW=40, 
            #TMVol_G=500,  
        )


initPV=hpwh.getSizingResults()[0]
simRun1 = hpwh.getSimRun(initPV=initPV, initST=160, minuteIntervals=60, nDays=365,exceptOnWaterShortage=True)
#df = pd.DataFrame(simRun1.)  # or simRun1.hourlyResults if that's the attribute
simRun1.writeCSV("simulation_results_hourly.csv")
print("Results saved to simulation_results_hourly.csv")
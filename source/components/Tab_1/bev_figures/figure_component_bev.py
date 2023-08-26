import numpy
import plotly.express as px
import pandas as pd
import math
import plotly.graph_objects as go

# bev
co2e_bev_vehicle_production_per_kg = 6.2
weight_emotor = 50
weight_drivechain = 27
co2e_bev_emotor_production = 4.5 * weight_emotor
co2e_bev_drivechain_production = 42 * weight_drivechain
co2e_bev_battery_production = 82.5 # * Batteriegwicht
co2e_saving_recycling_battery = -48.4 # * Batteriegewicht

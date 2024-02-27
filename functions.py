from wrf import getvar, ALL_TIMES, smooth2d, extract_times, latlon_coords, get_cartopy, interplevel, to_np, vinterp
from metpy.units import units
import metpy.calc as calc
import metpy as mp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import Dataset

def hgt_temp(lons, lats, cproj, height, temp, level, timestep):
    if level == 700:
        temp_to_plot = temp[timestep, 0]
        hgt_to_plot = height[timestep, 0]
    elif level == 500:
        temp_to_plot = temp[timestep, 1]
        hgt_to_plot = height[timestep, 1]
    elif level == 300:
        temp_to_plot = temp[timestep, 2]
        hgt_to_plot = height[timestep, 2]
    elif level == 200:
        temp_to_plot = temp[timestep, 3]
        hgt_to_plot = height[timestep, 3]
    else:
        raise ValueError
    
    fig = plt.figure(figsize=(12, 9))
    ax = plt.axes(projection=cproj)

    contour = plt.contour(to_np(lons), to_np(lats), to_np(hgt_to_plot), colors='black', linewidths=2, transform=ccrs.PlateCarree(), levels=np.arange(500, 603, 3))
    plt.clabel(contour, inline=1, fontsize=10, fmt="%i")

    plt.contourf(to_np(lons), to_np(lats), to_np(temp_to_plot), transform=ccrs.PlateCarree(), cmap="jet", extend='both')

    plt.colorbar(ax=ax, shrink=0.5, label='(°C)', extend='both')
    plt.title(f'{level} mb Temperature')


    ax.coastlines()

    return fig
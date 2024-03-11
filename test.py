from ituamt import AMTPlotter, colormaps
import os
from netCDF4 import Dataset
import pandas as pd
from wrf import getvar, extract_times, ALL_TIMES, latlon_coords, get_cartopy, vinterp, smooth2d
from metpy.units import units
from metpy import calc
import numpy as np
from matplotlib.colors import ListedColormap
from datetime import datetime
from multiprocessing import Pool

print(datetime.now())

cwd = os.getcwd()
if not os.path.exists("figures"): os.mkdir("figures")
figures_path = os.path.join(os.getcwd(), "figures")

wrfout = Dataset(r"C:\Users\gkbrk\Desktop\modelleme\github\modelleme\hadise1\set_a1\set_a1_d01")
unit_list = {"temp": "K", "tempc": "°C", "height": "dam", "td": "°C", "rh": "%", "pressure": "hPa", "wind_kt": "knot", "wind_ms": "m/s", "eth": "°C", "omega": "hPa/saat", "avo": "1/saat$^2$", 
             "rvo": "10$^{-5}$/s", "slp": "hPa", "precip": "mm", "tempc_adv": "K/saat", "avo_adv": "1/saat**2"}
levels = {850: 0, 700: 1, 500: 2, 300: 3, 200: 4}
dx = wrfout.DX * units.m
dy = wrfout.DY * units.m
times = pd.to_datetime(extract_times(wrfout, ALL_TIMES))
temp = smooth2d(vinterp(wrfout, field=getvar(wrfout, 'tk', timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), extrapolate=True, field_type='tc', log_p=True, timeidx=ALL_TIMES), 15)
tempc = smooth2d(vinterp(wrfout, field=getvar(wrfout, 'tc', timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), extrapolate=True, field_type='tc', log_p=True, timeidx=ALL_TIMES), 15)
lats, lons = latlon_coords(temp)
cproj = get_cartopy(temp)
height = smooth2d(vinterp(wrfout, field=getvar(wrfout, 'z', units='dam', timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), extrapolate=True, field_type='z', log_p=True, timeidx=ALL_TIMES).metpy.convert_units("dam"), 355)
td = smooth2d(vinterp(wrfout, field=getvar(wrfout, 'td', timeidx=ALL_TIMES, units="degC"), vert_coord='pressure', interp_levels=list(levels.keys()), extrapolate=True, field_type='tc', log_p=True, timeidx=ALL_TIMES), 15)
rh = vinterp(wrfout, field=getvar(wrfout, "rh", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
pressure = vinterp(wrfout, field=getvar(wrfout, 'pressure', timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), extrapolate=True, field_type='pressure_hpa', log_p=True, timeidx=ALL_TIMES)
u_kt = vinterp(wrfout, field=getvar(wrfout, "ua", units="kt", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
u_ms = vinterp(wrfout, field=getvar(wrfout, "ua", units="m/s", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
v_kt = vinterp(wrfout, field=getvar(wrfout, "va", units="kt", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
v_ms = vinterp(wrfout, field=getvar(wrfout, "va", units="m/s", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
ws_ms = vinterp(wrfout, field=getvar(wrfout, "wspd_wdir", units="m/s", timeidx=ALL_TIMES)[0], vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES)
eth = smooth2d(vinterp(wrfout, field=getvar(wrfout, "eth", units="degC", timeidx=ALL_TIMES), vert_coord="pressure", interp_levels=list(levels.keys()), extrapolate=True, field_type='eth', log_p=True, timeidx=ALL_TIMES), 10)
omega = smooth2d(vinterp(wrfout, field=getvar(wrfout, "omega", timeidx=ALL_TIMES), vert_coord='pressure', interp_levels=list(levels.keys()), timeidx=ALL_TIMES).metpy.convert_units("hPa/h"), 15)

avo = ((vinterp(wrfout, getvar(wrfout, "avo", timeidx=ALL_TIMES), vert_coord="pressure", interp_levels=list(levels.keys()), timeidx=ALL_TIMES)) * 10**-5) * units("1/second")
f = (2 * 7 * 10**-5 * np.sin(np.deg2rad(lats))).values * units("1/second")
rvo = (avo - f)* 10**5

t2 = getvar(wrfout, "T2", timeidx=ALL_TIMES).metpy.convert_units("degC")
td2 = getvar(wrfout, "td2", units="degC", timeidx=ALL_TIMES)
slp = smooth2d(getvar(wrfout, "slp", units="hPa", timeidx=ALL_TIMES), 3)
pw = getvar(wrfout, "pw", timeidx=ALL_TIMES)
rainc = getvar(wrfout, "RAINC", timeidx=ALL_TIMES)
rainnc = getvar(wrfout, "RAINNC", timeidx=ALL_TIMES)
u10, v10 = getvar(wrfout, "uvmet10", units="kt", timeidx=ALL_TIMES)

tempc_adv = calc.advection(tempc, u_ms, v_ms, dx=dx, dy=dy, x_dim=-1, y_dim=-2, vertical_dim=-3).metpy.convert_units("K/h")
avo_adv = (calc.advection(avo, u_ms, v_ms, dx=dx, dy=dy, x_dim=-1, y_dim=-2, vertical_dim=-3)).metpy.convert_units("1/hour**2")

def process_plot(i):
    for_saving = times[i].strftime("_%y%m%d%H")

    eth850 = AMTPlotter(lons=lons, lats=lats, contourf_data=eth[i, 0], cproj=cproj, contour_data=slp[i], title="850 hPa Equivalent Potential Temperature", time=times[i], 
                        cmap=colormaps["tigris"], cbar_label="(" + unit_list["eth"] + ")", contourf_levels=np.arange(-9, 84, 3), cbar_ticks=np.arange(-9, 84, 6))
    eth850.save_plot(path=os.path.join(figures_path, "eth850" + for_saving))
    eth850.close_plot()

    tempadv850 = AMTPlotter(lons=lons, lats=lats, contourf_data=tempc_adv[i, 0], cproj=cproj, contour_data=slp[i], title="850 hPa Temperature Advection", time=times[i],
                            cmap=colormaps["holton"], cbar_label="("+unit_list["tempc_adv"]+")", contourf_levels=np.concatenate((np.arange(-2.5, -0.5, 0.5), np.arange(-0.9, 1, 0.1), np.arange(1, 3, 0.5))), 
                            contour_linewidths=2)
    tempadv850.save_plot(path=os.path.join(figures_path, "tempadv850" + for_saving))
    tempadv850.close_plot()

    temphgt850 = AMTPlotter(lons=lons, lats=lats, contourf_data=tempc[i, 0], cproj=cproj, contour_data=height[i, 0], title="850 hPa Temperature", time=times[i],
                            cmap=colormaps["tigris"], cbar_label="("+unit_list["tempc"]+")", contourf_levels=np.arange(-36, 34, 2), cbar_ticks=np.arange(-36, 36, 4))
    temphgt850.save_plot(path=os.path.join(figures_path, "temphgt850" + for_saving))
    temphgt850.close_plot()

    rh700 = AMTPlotter(lons=lons, lats=lats, contourf_data=rh[i, 1], cproj=cproj, title="700 hPa Relative Humidty", time=times[i], contourf_levels=[60, 75, 90, 100], cmap=colormaps["greens"], 
                       cbar_extend="max", cbar_label="("+unit_list["rh"]+")")
    rh700.save_plot(path=os.path.join(figures_path, "rh700" + for_saving))
    rh700.close_plot()

    temphgt700 = AMTPlotter(lons=lons, lats=lats, contourf_data=tempc[i, 1], contour_data=height[i, 1], cproj=cproj, title="700 hPa Temperature", time=times[i],
                            cbar_label="("+unit_list["tempc"]+")", contourf_levels=np.arange(-42, 24, 2), cbar_ticks=np.arange(-42, 26, 4))
    temphgt700.save_plot(path=os.path.join(figures_path, "temphgt700" + for_saving))
    temphgt700.close_plot()

    rvo500 = AMTPlotter(lons=lons, lats=lats, contourf_data=rvo[i, 2], cproj=cproj, title="500 hPa Rel. Vorticity", time=times[i], u=u_kt[i, 2], v=v_kt[i, 2], barb_gap=10,
                        cbar_label="("+unit_list["rvo"]+")", cmap=ListedColormap(colormaps["holton"].colors[45:]), contourf_levels=np.concatenate((np.arange(-34, 32, 2), np.arange(35, 55, 5))))
    
    rvo500.save_plot(path=os.path.join(figures_path, "rvo500" + for_saving))
    rvo500.close_plot()

    avo_adv500 = AMTPlotter(lons=lons, lats=lats, contourf_data=avo_adv[i, 2], contour_data=height[i, 2], cproj=cproj, title="500 hPa Abs. Vorticity Adv.", time=times[i],
                            cbar_label="("+unit_list["avo"]+")", cmap=colormaps["holton"], contourf_levels=np.concatenate((np.arange(-0.25, -0.05, 0.05), np.arange(-0.09, 0.1, 0.01), np.arange(0.1, 0.3, 0.05))))
    avo_adv500.save_plot(path=os.path.join(figures_path, "avo_adv500" + for_saving))
    avo_adv500.close_plot()

    temphgt500 = AMTPlotter(lons=lons, lats=lats, contourf_data=tempc[i, 2], contour_data=height[i, 2], cproj=cproj, title="500 hPa Temperature", time=times[i],
                         cbar_label="("+unit_list["tempc"]+")", cmap=colormaps["tigris"], contourf_levels=np.arange(-54, 4, 2), cbar_ticks=np.arange(-54, 6, 4))
    temphgt500.save_plot(path=os.path.join(figures_path, "temphgt500" + for_saving))
    temphgt500.close_plot()

    vertical_v500 = AMTPlotter(lons=lons, lats=lats, contourf_data=omega[i, 2], contour_data=height[i, 2], cproj=cproj, title="500 hPa Vertical Velocity", time=times[i], 
                               cbar_label="("+unit_list["omega"]+")", cmap=colormaps["holton"], contourf_levels=np.arange(-46, 48, 2), cbar_ticks=np.arange(-46, 50, 4))
    vertical_v500.save_plot(path=os.path.join(figures_path, "vertical_v500" + for_saving))
    vertical_v500.close_plot()

    rvo300 = AMTPlotter(lons=lons, lats=lats, contourf_data=rvo[i, 3], cproj=cproj, title="300 hPa Rel. Vorticity", time=times[i], u=u_kt[i, 3], v=v_kt[i, 3], barb_gap=10,
                        cbar_label="("+unit_list["rvo"]+")", cmap=ListedColormap(colormaps["holton"].colors[45:]), contourf_levels=np.concatenate((np.arange(-34, 32, 2), np.arange(35, 55, 5))))
    rvo300.save_plot(path=os.path.join(figures_path, "rvo300" + for_saving))
    rvo300.close_plot()

    temphgt300 = AMTPlotter(lons=lons, lats=lats, contourf_data=tempc[i, 3], contour_data=height[i, 3], cproj=cproj, title="300 hPa Temperature", time=times[i], 
                            contourf_levels=np.arange(-62, -25), cmap=colormaps["tigris"], cbar_ticks=np.arange(-62, -25, 2), cbar_label="("+unit_list["tempc"]+")")
    temphgt300.save_plot(path=os.path.join(figures_path, "temphgt300" + for_saving))
    temphgt300.close_plot()

    jet300 = AMTPlotter(lons=lons, lats=lats, contourf_data=ws_ms[i, 3], contour_data=height[i, 3], cproj=cproj, title="300 hPa Jets", time=times[i],
                        cbar_label="("+unit_list["wind_ms"]+")", cmap=ListedColormap(colormaps["holton"].colors[130:]), contourf_levels=np.arange(20, 62, 2), cbar_ticks=np.arange(20, 64, 4))
    jet300.save_plot(path=os.path.join(figures_path, "jet300" + for_saving))
    jet300.close_plot()

    pwat = AMTPlotter(lons=lons, lats=lats, contourf_data=pw[i], cproj=cproj, title="PWAT", time=times[i],
                      cbar_label="("+unit_list["precip"]+")", cmap=ListedColormap(colormaps["holton_r"].colors[130:]), contourf_levels=np.arange(0, 50, 2), cbar_ticks=np.arange(0, 52, 4), cbar_extend="max")
    pwat.save_plot(path=os.path.join(figures_path, "pwat" + for_saving))
    pwat.close_plot()

    total_precip = AMTPlotter(lons=lons, lats=lats, contourf_data=rainnc[i], cproj=cproj, title="Acc. Total Precipitation", time=times[i], contourf_levels=np.arange(0, 105, 5),
                              cbar_label="("+unit_list["precip"]+")", cmap=ListedColormap(colormaps["holton_r"].colors[130:]), cbar_extend="max", cbar_ticks=np.arange(0, 110, 10))
    total_precip.save_plot(path=os.path.join(figures_path, "total_precip" + for_saving))
    total_precip.close_plot()

if __name__ == '__main__':
    with Pool(4) as pool:  # Number of processes is 4 as you have 4 cores to spare
        pool.map(process_plot, range(len(times)))
        
print(datetime.now())
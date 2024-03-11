from wrf import to_np
from metpy.units import units
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from datetime import timedelta
from matplotlib.colors import ListedColormap
import numpy as np


colormaps = {
            "greens": ListedColormap(["#afeeee", "#87cefa", "#00bfff"]),
            "tigris": ListedColormap(["#a000a0", "#c800c8", "#fa00fe", "#d200fe", "#aa00fe", "#8200fe", "#5a00fe", "#0032fe", "#0064fe", "#0096fe", "#00c8fe", "#0ae6f0", "#28e6a0", "#46e678", "#64e650", "#82f028", 
                                        "#a0fa00", "#fef400", "#ffe100", "#fec800", "#feaf00", "#fe9600", "#e67d00", "#e66400", "#dc4b1e", "#c8321e", "#b4191e", "#aa001e", "#dc4b1e", "#b40032", "#c80064", "#fe0096", 
                                        "#fe00c8", "#fe00e1", "#fe00fa", "#e100e1", "#c800c8"]),
            "holton": ListedColormap(["#2a0080", "#290086", "#27008c", "#230091", "#200097", "#1c009c", "#1900a1", "#1400a6", "#1000aa", "#0b00af", "#0600b3", "#0300b7", "#0100bb", "#0000bf", "#0000c3", "#0003c6",
                                        "#0006ca", "#000dcd", "#0013d0", "#001ed5", "#0021d6", "#0028d9", "#002ddc", "#0034de", "#003ae1", "#0041e3", "#0047e5", "#004de7", "#0053e9", "#005aeb", "#005fed", "#0068f1", 
                                        "#006aef", "#0070f0", "#0075f2", "#007af3", "#007ff4", "#0084f5", "#0089f6", "#008ef7", "#0092f8", "#0097f9", "#009bf9", "#009ffa", "#00a3fb", "#00a8fb", "#00acfc", "#00b0fd", 
                                        "#00b3fd", "#00b6fd", "#00bafd", "#00bdfd", "#00c1fe", "#00c4fe", "#00c7fe", "#00cafe", "#00cdfe", "#00d1fe", "#00d4fe", "#00d7fe", "#00dafe", "#00ddfe", "#00e0fe", "#00e2fe", 
                                        "#00e5ff", "#00e8ff", "#00ebff", "#00eeff", "#00f0ff", "#01f3ff", "#01f6ff", "#01f9ff", "#02fcff", "#03fffe", "#04fffb", "#06fff8", "#07fff5", "#09fff2", "#0bffef", "#0dffed", 
                                        "#0fffea", "#12ffe7", "#15ffe4", "#17ffe1", "#1affde", "#1cffdb", "#20ffd8", "#22ffd5", "#25ffd2", "#29ffcf", "#2bffcd", "#2effca", "#32ffc7", "#35ffc5", "#38ffc2", "#3dffc0", 
                                        "#3dffc0", "#43ffbc", "#47ffba", "#4cffb9", "#4fffb6", "#53ffb5", "#57ffb3", "#5affb2", "#60ffb1", "#64ffb0", "#68ffb0", "#6cffb0", "#71ffaf", "#76ffaf", "#7bffb0", "#80ffb0", 
                                        "#85ffb1", "#8affb3", "#90feb5", "#95ffb6", "#9bffb8", "#a0ffbb", "#a6ffbd", "#adffc1", "#b3ffc5", "#baffc9", "#c1ffce", "#c9ffd3", "#d2ffd9", "#dbffe0", "#e6ffe9", "#f3fff4", 
                                        "#fbfff3", "#f8ffe6", "#f5ffdb", "#f3ffd2", "#f2ffc9", "#f1ffc1", "#f0ffba", "#f0ffb3", "#efffae", "#efffa6", "#efffa0", "#f0ff9b", "#f0ff95", "#f1ff8f", "#f2ff8a", "#f2ff85", 
                                        "#f3ff80", "#f4ff7b", "#f4ff7b", "#f7ff72", "#f8ff6c", "#f9ff68", "#fbff64", "#fcff60", "#feff5b", "#fffe57", "#fffc53", "#fffa4f", "#fff84b", "#fff747", "#fff543", "#fff340", 
                                        "#fff13d", "#ffef38", "#ffee35", "#ffec32", "#ffea2e", "#ffe82b", "#ffe529", "#ffe325", "#ffe122", "#ffdf20", "#ffdc1c", "#ffda1a", "#ffd818", "#ffd516", "#ffd312", "#ffd010", 
                                        "#ffcd0d", "#ffcb0c", "#ffc80a", "#ffc507", "#ffc207", "#ffbf05", "#ffbc04", "#ffb803", "#ffb502", "#ffb202", "#ffaf01", "#ffac01", "#ffa701", "#ffa300", "#ff9f00", "#ff9b00", 
                                        "#fe9700", "#fe9300", "#fe8f00", "#fe8b00", "#fe8600", "#fe8200", "#fe7d00", "#fe7800", "#fe7300", "#fe6d00", "#fe6800", "#fe6300", "#fd5e00", "#fd5700", "#fd5200", "#fd4c00", 
                                        "#fc4500", "#fc3f00", "#fc3f00", "#fb3200", "#fa2b00", "#f92400", "#f91c00", "#f81500", "#f70d00", "#f60600", "#f50200", "#f40000", "#f30000", "#f20003", "#f00009", "#ef0011", 
                                        "#ee0018", "#ed0020", "#eb0027", "#e9002d", "#e80035", "#e5003a", "#e30041", "#e10047", "#de004e", "#dc0053", "#d90058", "#d6005e", "#d30063", "#d10069", "#cd006c", "#ca0070", 
                                        "#c60075", "#c10075", "#bf007b", "#bb007e", "#b70080", "#b30082", "#af0083", "#aa0085", "#a30182", "#a10086", "#9c0085", "#970085", "#910084", "#8c0082", "#860080", "#80007e"]),
            "holton_r": ListedColormap(["#80007e", "#860080", "#8c0082", "#910084", "#970085", "#9c0085", "#a10086", "#a30182", "#aa0085", "#af0083", "#b30082", "#b70080", "#bb007e", "#bf007b", "#c10075", "#c60075", 
                                        "#ca0070", "#cd006c", "#d10069", "#d30063", "#d6005e", "#d90058", "#dc0053", "#de004e", "#e10047", "#e30041", "#e5003a", "#e80035", "#e9002d", "#eb0027", "#ed0020", "#ee0018", 
                                        "#ef0011", "#f00009", "#f20003", "#f30000", "#f40000", "#f50200", "#f60600", "#f70d00", "#f81500", "#f91c00", "#f92400", "#fa2b00", "#fb3200", "#fc3f00", "#fc3f00", "#fc4500", 
                                        "#fd4c00", "#fd5200", "#fd5700", "#fd5e00", "#fe6300", "#fe6800", "#fe6d00", "#fe7300", "#fe7800", "#fe7d00", "#fe8200", "#fe8600", "#fe8b00", "#fe8f00", "#fe9300", "#fe9700", 
                                        "#ff9b00", "#ff9f00", "#ffa300", "#ffa701", "#ffac01", "#ffaf01", "#ffb202", "#ffb502", "#ffb803", "#ffbc04", "#ffbf05", "#ffc207", "#ffc507", "#ffc80a", "#ffcb0c", "#ffcd0d", 
                                        "#ffd010", "#ffd312", "#ffd516", "#ffd818", "#ffda1a", "#ffdc1c", "#ffdf20", "#ffe122", "#ffe325", "#ffe529", "#ffe82b", "#ffea2e", "#ffec32", "#ffee35", "#ffef38", "#fff13d", 
                                        "#fff340", "#fff543", "#fff747", "#fff84b", "#fffa4f", "#fffc53", "#fffe57", "#feff5b", "#fcff60", "#fbff64", "#f9ff68", "#f8ff6c", "#f7ff72", "#f4ff7b", "#f4ff7b", "#f3ff80", 
                                        "#f2ff85", "#f2ff8a", "#f1ff8f", "#f0ff95", "#f0ff9b", "#efffa0", "#efffa6", "#efffae", "#f0ffb3", "#f0ffba", "#f1ffc1", "#f2ffc9", "#f3ffd2", "#f5ffdb", "#f8ffe6", "#fbfff3", 
                                        "#f3fff4", "#e6ffe9", "#dbffe0", "#d2ffd9", "#c9ffd3", "#c1ffce", "#baffc9", "#b3ffc5", "#adffc1", "#a6ffbd", "#a0ffbb", "#9bffb8", "#95ffb6", "#90feb5", "#8affb3", "#85ffb1", 
                                        "#80ffb0", "#7bffb0", "#76ffaf", "#71ffaf", "#6cffb0", "#68ffb0", "#64ffb0", "#60ffb1", "#5affb2", "#57ffb3", "#53ffb5", "#4fffb6", "#4cffb9", "#47ffba", "#43ffbc", "#3dffc0", 
                                        "#3dffc0", "#38ffc2", "#35ffc5", "#32ffc7", "#2effca", "#2bffcd", "#29ffcf", "#25ffd2", "#22ffd5", "#20ffd8", "#1cffdb", "#1affde", "#17ffe1", "#15ffe4", "#12ffe7", "#0fffea", 
                                        "#0dffed", "#0bffef", "#09fff2", "#07fff5", "#06fff8", "#04fffb", "#03fffe", "#02fcff", "#01f9ff", "#01f6ff", "#01f3ff", "#00f0ff", "#00eeff", "#00ebff", "#00e8ff", "#00e5ff", 
                                        "#00e2fe", "#00e0fe", "#00ddfe", "#00dafe", "#00d7fe", "#00d4fe", "#00d1fe", "#00cdfe", "#00cafe", "#00c7fe", "#00c4fe", "#00c1fe", "#00bdfd", "#00bafd", "#00b6fd", "#00b3fd", 
                                        "#00b0fd", "#00acfc", "#00a8fb", "#00a3fb", "#009ffa", "#009bf9", "#0097f9", "#0092f8", "#008ef7", "#0089f6", "#0084f5", "#007ff4", "#007af3", "#0075f2", "#0070f0", "#006aef", 
                                        "#0068f1", "#005fed", "#005aeb", "#0053e9", "#004de7", "#0047e5", "#0041e3", "#003ae1", "#0034de", "#002ddc", "#0028d9", "#0021d6", "#001ed5", "#0013d0", "#000dcd", "#0006ca", 
                                        "#0003c6", "#0000c3", "#0000bf", "#0100bb", "#0300b7", "#0600b3", "#0b00af", "#1000aa", "#1400a6", "#1900a1", "#1c009c", "#200097", "#230091", "#27008c", "#290086", "#2a0080"])}

class AMTPlotter:
    def __init__(self, lons, lats, cproj, contourf_data, title="Title", cmap="jet", contour_colors="black", 
                 contour_data=None, u=None, v=None, contourf_levels=None, contour_levels=None, barb_gap=1, barb_length=6, time=None,
                 cbar_orientation=None, cbar_shrink=1.0, cbar_location="bottom", cbar_extend="both", cbar_ticks=None, cbar_label=None, cbar_aspect=50,
                 contour_linewidths=1.5, contour_linestyles="solid"):
        """
        Initializes the MapPlotter object with necessary attributes.
        """
        self.lons = lons
        self.lats = lats
        self.cproj = cproj
        self.contourf_data = contourf_data
        self.contour_data = contour_data
        self.contourf_levels = contourf_levels
        self.contour_levels = contour_levels
        self.contour_linewidths = contour_linewidths
        self.contour_linestyles = contour_linestyles

        self.u = u
        self.v = v
        self.barb_gap = barb_gap
        self.barb_length = barb_length

        self.time = time
        self.title = title
        self.cmap = cmap
        self.contour_colors = contour_colors

        self.fig = plt.figure(figsize=(12.80, 7.2), layout="compressed", dpi=96.)
        self.ax = plt.axes(projection=cproj)
        self.ax.coastlines()

        if self.time is not None:
            atime = time + timedelta(hours=3)
            dtime = atime.strftime("%d-%m-%Y %H:%M") 
            self.ax.set_title(f"{dtime} +03 UTC", loc="right")
        
        contourf = self.ax.contourf(self.lons, self.lats, self.contourf_data, levels=self.contourf_levels, cmap=self.cmap, transform=ccrs.PlateCarree(), extend=cbar_extend)
        if self.contour_data is not None:
            contour = self.ax.contour(self.lons, self.lats, self.contour_data, levels=self.contour_levels, colors=self.contour_colors, linewidths=self.contour_linewidths, linestyles=self.contour_linestyles, transform=ccrs.PlateCarree())
            self.ax.clabel(contour, inline=1, fontsize=10, fmt="%i")
        if u is not None and v is not None:
            self.ax.barbs(to_np(self.lons[::self.barb_gap, ::self.barb_gap]), to_np(self.lats[::self.barb_gap, ::self.barb_gap]), 
                          to_np(self.u[::self.barb_gap, ::self.barb_gap]), to_np(self.v[::self.barb_gap, ::self.barb_gap]), transform=ccrs.PlateCarree(), length=self.barb_length)

        cbar = self.fig.colorbar(contourf, ax=self.ax, extend=cbar_extend, aspect=cbar_aspect, orientation=cbar_orientation, shrink=cbar_shrink, location=cbar_location, ticks=cbar_ticks, label=cbar_label)
        cbar.ax.text(0, -2.5, f'Min: {np.floor(np.min(contourf_data)).values:.0f}', va='bottom', ha='left', transform=cbar.ax.transAxes)
        cbar.ax.text(1, -2.5, f'Max: {np.ceil(np.max(contourf_data)).values:.0f}', va='bottom', ha='right', transform=cbar.ax.transAxes)
        self.ax.set_title(self.title, loc="left")
        
    def add_contourf(self, data, levels=None, extend="both"):
        """
        Plots the filled contour plot using the specified attributes.
        If contourf_levels is None, the levels parameter is omitted.
        Stores the contourf plot object for later use, e.g., by add_colorbar.
        """
        if levels is not None:
            self.contourf_plot = self.ax.contourf(self.lons, self.lats, data, levels=levels, cmap=self.cmap, extend=extend, transform=ccrs.PlateCarree())
        else:
            self.contourf_plot = self.ax.contourf(self.lons, self.lats, data, cmap=self.cmap, extend=extend, transform=ccrs.PlateCarree())    

    def add_contour(self, data, levels=None, colors="black", linewidths=1.5, linestyles="solid"):
        """
        Adds contour lines to the plot.
        :param line_levels: Optional levels for the contour lines.
        :param colors: Color of the contour lines.
        """

        if levels is not None:
            contour_lines = self.ax.contour(self.lons, self.lats, data, levels=levels, colors=colors, linewidths=linewidths, linestyles=linestyles, transform=ccrs.PlateCarree())
        else:
            contour_lines = self.ax.contour(self.lons, self.lats, data, colors=colors, linewidths=linewidths, linestyles=linestyles, transform=ccrs.PlateCarree())
        self.ax.clabel(contour_lines, inline=1, fontsize=10, fmt="%i")
    
    def add_wind_barbs(self, u, v, gap):
        """
        Adds wind barbs to the plot.  
        """
        self.ax.barbs(to_np(self.lons[::gap, ::gap]), to_np(self.lats[::gap, ::gap]), to_np(u[::gap, ::gap]), to_np(v[::gap, ::gap]), transform=ccrs.PlateCarree(), length=6)
    
    def add_timestamp(self, time):
        time = time + timedelta(hours=3)
        dtime = time.strftime("%d-%m-%Y %H:%M") 
        self.ax.set_title(f"{dtime} +03 UTC", loc="right")
    
    def add_text(self, x, y, text, color, fontsize, fontstyle, horizontalalignment, rotation, verticalalignment):
        """
        Adds text to the plot. 
        """
        self.ax.text(x, y, text, color=color, fontsize=fontsize, fontstyle=fontstyle, horizontalalignment=horizontalalignment, rotation=rotation, verticalalignment=verticalalignment)

    def show_plot(self):
        """
        Displays the plot.
        """
        plt.show()
    def close_plot(self):
        """
        Closes the plot.
        """
        plt.close()

    def save_plot(self, path):
        """
        Saves the plot as png.     
        """
        self.fig.savefig(f"{path}.png", format="png", dpi=150)




import os
from pathlib import Path

import contextily
import geopandas
import matplotlib.pyplot as plt

import nrcs_api
import pasturemap_api

BASEMAP_URL = 'https://api.mapbox.com/styles/v1/joelkek' \
              '/cjdmziapz1yc72rn22lj95qkt/tiles/256/tileZ/tileX/tileY' \
              '?access_token=pk.eyJ1Ijoiam9lbGtlayIsImEiOiJjamR5OXAxcnowdjZ' \
              '4MnlvNnQzbHVieXdzIn0.GqlA3iQP2WXkUfXSESJaNg'

OTHER_URL = 'http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'


def add_basemap(ax):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = contextily.bounds2img(xmin, ymin, xmax, ymax, zoom=15, url=BASEMAP_URL)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    ax.axis((xmin, xmax, ymin, ymax))


def plot_estimate(user_email: str, estimate: geopandas.GeoDataFrame, regions: geopandas.GeoDataFrame):
    estimate = estimate.to_crs(epsg=3857)
    regions = regions.to_crs(epsg=3857)

    ax = estimate[estimate['forage_regular'].notna()].plot(
        column='forage_regular',
        legend=True,
        figsize=(24, 24),
        cmap='BuGn',
        edgecolor='violet',
        linewidth=1,
    )
    ax = estimate[estimate['forage_regular'].isna()].geometry.boundary.plot(
        ax=ax,
        edgecolor='violet',
        linewidth=1,
        facecolor='none',
    )

    ax = regions.geometry.boundary.plot(
        ax=ax,
        edgecolor='yellow',
        linewidth=2,
        facecolor='none',
    )

    add_basemap(ax)
    ax.set_title('NRCS Forage Estimate (lb / acre * year)', fontsize=32)
    ax.set_axis_off()
    ax.autoscale(enable=False, tight=True)
    ax.annotate(user_email, xycoords='figure fraction', xy=(0.05, 0.05), fontsize=24)

    output_path = Path(os.getcwd()) / 'results' / '{}.png'.format(user_email.split('@')[0])

    try:
        os.mkdir(output_path.parent)
    except FileExistsError:
        pass

    plt.savefig(str(output_path))


def main():
    admin_user = pasturemap_api.login(
        email='jyoung@pasturemap.com',
        password='testpassword2',
    )
    for email in ('cornerstonegrazing@gmail.com', ):
        masquerade_user = pasturemap_api.masquerade(admin_user=admin_user, masquerade_email=email)
        test_data = pasturemap_api.paddocks(masquerade_user)
        forage_estimate = nrcs_api.estimate_forage(test_data)
        plot_estimate(masquerade_user.email, forage_estimate, test_data)


if __name__ == '__main__':
    main()

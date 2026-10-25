# -*- coding: utf-8 -*-
"""
Created on Jan2026

@author: Angelos

"""

import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import tempfile
import zipfile
import os
import io
import math
from shapely.geometry import box
from translations import TEXT

st.set_page_config(page_title="Catchment2Storm", layout="wide")

# ------------------------------
# Utility functions
# ------------------------------
@st.cache_data(show_spinner=False)
def load_idf_grid():
    """Load bundled Greek IDF grid (Ombrian parameters)."""
    base = os.path.dirname(__file__)
    gpkg = os.path.join(base, "data", "ombrian_parameters.gpkg")
    return gpd.read_file(gpkg)


def save_uploaded_shapefile(uploaded_files):
    """Write uploaded files (list of UploadedFile) to a temp directory and return path to .shp"""
    tmpdir = tempfile.mkdtemp()
    shp_path = None
    # If there's a zip in uploads, prefer it
    for uf in uploaded_files:
        if uf.name.lower().endswith(".zip"):
            zip_path = os.path.join(tmpdir, uf.name)
            with open(zip_path, "wb") as f:
                f.write(uf.getvalue())
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmpdir)
            # find shp
            for f in os.listdir(tmpdir):
                if f.lower().endswith(".shp"):
                    shp_path = os.path.join(tmpdir, f)
                    return shp_path
    # Otherwise write uploaded component files
    for uf in uploaded_files:
        outp = os.path.join(tmpdir, uf.name)
        with open(outp, "wb") as f:
            f.write(uf.getvalue())
        if uf.name.lower().endswith(".shp"):
            shp_path = outp
    # final check
    if shp_path and os.path.exists(shp_path):
        return shp_path
    # try searching directory
    for f in os.listdir(tmpdir):
        if f.lower().endswith(".shp"):
            return os.path.join(tmpdir, f)
    raise FileNotFoundError("No .shp found among uploaded files.")


def compute_phi(A_km2, D_hours):
    """Area reduction coefficient (Koutsogiannis & Ksanthopoulos, 1999)"""
    if A_km2 <= 0:
        return 1.0
    lnA = math.log(A_km2)
    exponent = 0.36 - 0.01 * lnA
    reduction = 0.048 * (A_km2 ** exponent) / (D_hours ** 0.35)
    phi = max(1 - reduction, 0.25)
    phi = min(phi, 1.0)  # Enforce upper bound
    return phi


def compute_intensity(alpha, eta, xi, lam, beta, T, kappa):
    """
    Compute rainfall intensity (mm/hr) using Greek Ombrian IDF formulation.
    
    i(T, κ) = λ * [ (T/β)^ξ - 1 ] / (1 + κ/α)^η
    α, η, ξ, λ, β = Ombrian parameters
    T = return period (yr)
    κ = duration (hr)
    """
    numerator = ((T / beta) ** xi) - 1
    denominator = (1 + (kappa / alpha)) ** eta
    return lam * (numerator / denominator)


def alternate_block_method(increments):
    """Apply ABM to list of increments (list-like). Returns rearranged list."""
    sorted_vals = sorted(increments, reverse=True)
    n = len(sorted_vals)
    abm = [0] * n
    center = (n - 1) // 2
    left = center
    right = center + 1
    toggle = True
    for val in sorted_vals:
        if toggle and left >= 0:
            abm[left] = val
            left -= 1
        elif right < n:
            abm[right] = val
            right += 1
        toggle = not toggle
    return abm


def build_site_geometry(coord_system, c1, c2, area_km2):
    """
    Build the site geometry (EPSG:2100) from typed coordinates.
    - area_km2 > 0 : circle of exactly that area, centred on the site. It is then
                     processed exactly like an uploaded catchment polygon.
    - area_km2 == 0: point site. A 1 m radius circle is used only to locate the
                     IDF grid cell(s) at the point (no areal reduction, phi = 1).
    c1, c2 = latitude, longitude (WGS84) or X, Y (EPSG:2100).
    Returns (GeoDataFrame with one polygon, site point in EPSG:2100).
    """
    if coord_system.startswith("WGS84"):
        pt = gpd.GeoSeries(gpd.points_from_xy([c2], [c1]), crs="EPSG:4326").to_crs(epsg=2100).iloc[0]
    else:
        pt = gpd.points_from_xy([c1], [c2])[0]
    if area_km2 > 0:
        target = area_km2 * 1e6
        r = math.sqrt(target / math.pi)
        r = r * math.sqrt(target / pt.buffer(r, quad_segs=64).area)  # exact area despite polygon approximation
        geom = pt.buffer(r, quad_segs=64)
    else:
        geom = pt.buffer(1.0, quad_segs=16)
    return gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:2100"), pt

# ------------------------------
# Language selector (English / Greek) - only the displayed texts change
# ------------------------------
_lang_spacer, _lang_col = st.columns([6, 1])
with _lang_col:
    lang = st.selectbox(TEXT["en"]["lang_label"], ["en", "el"], key="lang",
                        format_func=lambda k: {"en": "English", "el": "Ελληνικά"}[k])


def tr(key, **kw):
    """Displayed text in the selected language (see translations.py)."""
    txt = TEXT[lang][key]
    return txt.format(**kw) if kw else txt

# ------------------------------
# Sidebar: Inputs
# ------------------------------
st.sidebar.title(tr("sb_title"))
input_mode = st.sidebar.radio(
    tr("mode_label"),
    ["Catchment shapefile", "Site coordinates"],
    format_func=lambda k: tr("mode_" + k), key="input_mode",
    help=tr("mode_help")
)

if input_mode == "Catchment shapefile":
    st.sidebar.markdown(
        tr("upload_md")
    )

    uploaded = st.sidebar.file_uploader(
        tr("upload_label"), key="uploader", accept_multiple_files=True,
        type=["zip", "shp", "dbf", "shx", "prj"], help=tr("upload_help")
    )
else:
    uploaded = None
    coord_system = st.sidebar.selectbox(
        tr("coord_label"),
        ["WGS84 - latitude / longitude (decimal degrees)", "EPSG:2100 - Greek Grid (EGSA87) X / Y (m)"],
        format_func=lambda k: tr("coord_" + k.split(" ")[0])
    )
    if coord_system.startswith("WGS84"):
        c1 = st.sidebar.number_input(tr("lat"), key="lat", min_value=34.0, max_value=42.0, value=37.975500, step=0.001, format="%.6f")
        c2 = st.sidebar.number_input(tr("lon"), key="lon", min_value=19.0, max_value=30.0, value=23.734800, step=0.001, format="%.6f")
    else:
        c1 = st.sidebar.number_input(tr("x"), key="x", min_value=0.0, value=476558.71, step=100.0, format="%.2f")
        c2 = st.sidebar.number_input(tr("y"), key="y", min_value=0.0, value=4202841.94, step=100.0, format="%.2f")
    site_area_km2 = st.sidebar.number_input(
        tr("area_label"), key="site_area", min_value=0.0, value=0.0, step=0.1, format="%.4f",
        help=tr("area_help")
    )

st.sidebar.markdown("---")
T = st.sidebar.number_input(tr("T_label"), key="T", min_value=1, value=100, step=10)
D = st.sidebar.number_input(tr("D_label"), key="D", min_value=0.5, value=24.0, step=1.0, format="%.2f")
t = st.sidebar.number_input(tr("t_label"), key="t", min_value=0.01, value=0.25, step=0.01, format="%.3f")

# Sanity checks
if t > D:
    st.sidebar.error(tr("err_t_gt_D"))
if D % t != 0:
    st.sidebar.warning(tr("warn_D_mod_t"))

# CRS selection if missing
default_crs = st.sidebar.selectbox(
    tr("crs_label"),
    ["EPSG:2100 (Greek Grid)", "EPSG:4326 (WGS84)"],
    format_func=lambda k: tr("crs_" + k)
)

st.sidebar.markdown("---")
run_button = st.sidebar.button(tr("run"))

# ------------------------------
# Load IDF grid (bundled)
# ------------------------------
st.sidebar.markdown(tr("grid_md"))
try:
    greece_grid = load_idf_grid()
except Exception as e:
    st.error(tr("err_grid", e=e))
    st.stop()

# Create tabs: Introduction, Main (existing app), Use and Reference
tab_intro, tab_main, tab_ref = st.tabs([tr("tab_intro"), tr("tab_main"), tr("tab_ref")])

# ------------------------------
# Introduction tab
# ------------------------------
with tab_intro:
    st.title(tr("intro_title"))
    st.markdown(tr("intro_md"))

# ------------------------------
# Main tab
# ------------------------------
with tab_main:
    # Show grid basic info
    with st.expander(tr("grid_info")):
        st.write(tr("rows"), len(greece_grid))
        st.write(tr("crs"), greece_grid.crs)
        st.write(tr("cols"), list(greece_grid.columns))

    st.info(tr("idf_info"))

    # ------------------------------
    # Run model when user clicks Run
    # ------------------------------
    if run_button:
        point_site = False
        if input_mode == "Site coordinates":
            # Site from typed coordinates (no shapefile)
            try:
                catchment_gdf, site_point = build_site_geometry(coord_system, c1, c2, site_area_km2)
            except Exception as e:
                st.error(tr("err_site", e=e))
                st.stop()
            point_site = site_area_km2 <= 0
            st.info(
                tr("site_info", x=site_point.x, y=site_point.y)
                + (tr("site_point") if point_site else tr("site_circle", a=site_area_km2))
            )
        else:
            if not uploaded:
                st.error(tr("err_no_upload"))
                st.stop()

            # Attempt to save uploaded files and read shapefile
            try:
                shp_path = save_uploaded_shapefile(uploaded)
            except Exception as e:
                st.error(tr("err_files", e=e))
                st.stop()

            try:
                catchment_gdf = gpd.read_file(shp_path)
            except Exception as e:
                st.error(tr("err_read", e=e))
                st.stop()

        # If multiple features, dissolve into one
        if len(catchment_gdf) > 1:
            catch_geom = catchment_gdf.unary_union
            catchment = gpd.GeoDataFrame({"geometry":[catch_geom]}, crs=catchment_gdf.crs)
        else:
            catchment = catchment_gdf.copy()

        # Validate geometry
        if catchment.geometry.is_empty.any() or catchment.geometry.area.sum() == 0:
            st.error(tr("err_empty"))
            st.stop()

        # Ensure CRS: if missing, use user selection
        if catchment.crs is None:
            if default_crs.startswith("EPSG:2100"):
                catchment.set_crs(epsg=2100, inplace=True)
            else:
                catchment.set_crs(epsg=4326, inplace=True)
            st.warning(tr("warn_nocrs", crs=catchment.crs))

        # Reproject to grid CRS if needed
        if catchment.crs != greece_grid.crs:
            catchment = catchment.to_crs(greece_grid.crs)

        # ------------------------------
        # Spatial intersection with grid
        # ------------------------------
        try:
            # Clip grid to bounding box first (faster)
            grid_clip = greece_grid[greece_grid.intersects(catchment.unary_union)]
            intersections = gpd.overlay(catchment, grid_clip, how='intersection')
        except Exception as e:
            st.error(tr("err_intersect", e=e))
            st.stop()

        if intersections.empty:
            st.error(tr("err_nointersect"))
            if input_mode == "Site coordinates":
                st.warning(tr("warn_outside"))
            st.stop()

        # Compute area and percentages
        intersections['intersect_area'] = intersections.geometry.area
        total_catchment_area = catchment.geometry.area.sum()
        intersections['area_perc'] = intersections['intersect_area'] / total_catchment_area

        # Normalize percentages defensively
        intersections['area_perc'] /= intersections['area_perc'].sum()

        # Required IDF columns
        col_map = {}
        possible_names = {
            'alpha': ['alpha', 'α', 'a', 'ALPHA'],
            'eta':   ['eta', 'η', 'ETA'],
            'xi':    ['xi', 'ξ', 'XI'],
            'lam':   ['lam', 'λ', 'LAM', 'lambda'],
            'beta':  ['beta', 'β', 'BETA']
        }
        for ascii_name, variants in possible_names.items():
            found = None
            for v in variants:
                if v in intersections.columns:
                    found = v
                    break
            if found is None:
                st.error(tr("err_missing_col", name=ascii_name, variants=variants))
                st.stop()
            col_map[found] = ascii_name

        intersections = intersections.rename(columns=col_map)

        # Build subbasin summary
        idf_columns = ['alpha', 'eta', 'xi', 'lam', 'beta']
        summary = intersections[idf_columns + ['intersect_area', 'area_perc']].copy()
        summary = summary.reset_index(drop=True)
        summary.index = summary.index + 1
        summary.rename(columns={'intersect_area': 'area', 'area_perc': 'perc'}, inplace=True)
        summary.insert(0, 'SUB-BASIN', summary.index)

        # Handle uncovered portion using centroid
        union_grid = gpd.GeoSeries(greece_grid.unary_union)
        difference = catchment.geometry.unary_union.difference(union_grid[0])
        if difference is not None and (not difference.is_empty):
            centroid = gpd.GeoSeries([difference], crs=catchment.crs).centroid.iloc[0]
            dists = greece_grid.geometry.distance(centroid)
            nearest_idx = dists.idxmin()
            nearest_poly = greece_grid.loc[nearest_idx]
            missing_area = difference.area
            missing_perc = missing_area / total_catchment_area
            missing_row = {
                'SUB-BASIN': int(summary['SUB-BASIN'].max() + 1) if not summary.empty else 1,
                'alpha': nearest_poly.get('alpha', nearest_poly.get('α', None)),
                'eta': nearest_poly.get('eta', nearest_poly.get('η', None)),
                'xi': nearest_poly.get('xi', nearest_poly.get('ξ', None)),
                'lam': nearest_poly.get('lam', nearest_poly.get('λ', None)),
                'beta': nearest_poly.get('beta', nearest_poly.get('β', None)),
                'area': missing_area,
                'perc': missing_perc
            }
            summary = pd.concat([summary, pd.DataFrame([missing_row])], ignore_index=True)

        # Round numbers
        for c in ['alpha', 'eta', 'xi', 'lam', 'beta', 'area', 'perc']:
            summary[c] = summary[c].astype(float).round(6)

        subbasins = summary.copy()
        if point_site:
            subbasins['area'] = 0.0  # point site: no area -> phi = 1

        st.success(tr("ok_sub"))
        st.write(tr("h_sub"))
        st.dataframe(subbasins)

        # ------------------------------
        # Short documentation for non-experts
        # ------------------------------
        with st.expander(tr("exp_idf")):
            st.markdown(tr("md_idf"))

        with st.expander(tr("exp_phi")):
            st.markdown(tr("md_phi"))

        with st.expander(tr("exp_abm")):
            st.markdown(tr("md_abm"))

        # ------------------------------
        # Hyetograph generation
        # ------------------------------
        kappas = np.arange(t, D + t, t)
        A_m2 = subbasins["area"].sum()
        A_km2 = A_m2 / 1e6
        phi = compute_phi(A_km2, D)

        records = []
        for _, row in subbasins.iterrows():
            try:
                sb = int(row['SUB-BASIN'])
            except (ValueError, TypeError):
                continue
            alpha, eta, xi, lam, beta, perc = map(float, [row['alpha'], row['eta'], row['xi'], row['lam'], row['beta'], row['perc']])
            for kappa in kappas:
                i = compute_intensity(alpha, eta, xi, lam, beta, T, kappa)
                P = i * kappa
                i_area = i * perc
                P_area = P * perc
                records.append({
                    "Subbasin": sb,
                    "Kappa (hr)": round(kappa, 6),
                    "Intensity (mm/hr)": round(i, 6),
                    "Precipitation (mm)": round(P, 6),
                    "i (mm/hr) area": round(i_area, 6),
                    "P (mm) area": round(P_area, 6)
                })

        df_all = pd.DataFrame(records)
        df_total = df_all.groupby("Kappa (hr)").agg({"i (mm/hr) area": "sum", "P (mm) area": "sum"}).reset_index()
        df_total.insert(0, "A/A", range(1, len(df_total) + 1))
        df_total.columns = ["A/A", "kappa (hr)", "i (mm/hr)", "P (mm)"]
        df_total["P (mm) Incremental Depth"] = df_total["P (mm)"].diff().fillna(df_total["P (mm)"])
        df_total["P (mm) Phi Reduced"] = df_total["P (mm) Incremental Depth"] * phi
        df_total["ABM P (mm)"] = alternate_block_method(df_total["P (mm) Phi Reduced"].tolist())

        st.write(tr("h_phi"))
        st.write(tr("phi_line", phi=phi, A=A_km2, D=D))
        st.write(tr("h_total"))
        st.dataframe(df_total)

        # ------------------------------
        # Plot ABM hyetograph
        # ------------------------------
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(df_total["kappa (hr)"], df_total["ABM P (mm)"], width=t*0.9, align='center', edgecolor='black')
        ax.set_xlabel(tr("ax_duration"))
        ax.set_ylabel(tr("ax_precip"))
        ax.set_title(tr("hyeto_title", T=T, D=D))
        ax.grid(True, linestyle='--', alpha=0.4)
        st.pyplot(fig)

        # ------------------------------
        # Map preview
        # ------------------------------
        st.write(tr("h_map"))
        try:
            catch_gg = catchment.to_crs(epsg=2100)
            grid_gg = greece_grid.to_crs(epsg=2100)
            minx, miny, maxx, maxy = catch_gg.total_bounds
            buffer_m = max(maxx - minx, maxy - miny) * 2.0
            if input_mode == "Site coordinates":
                buffer_m = max(buffer_m, 10000.0)  # small sites: show the surrounding grid cells
            bbox = box(minx - buffer_m, miny - buffer_m, maxx + buffer_m, maxy + buffer_m)
            grid_subset = grid_gg[grid_gg.intersects(bbox)]
            fig_map, ax = plt.subplots(figsize=(8, 8))
            grid_subset.boundary.plot(ax=ax, color="red", linewidth=0.6, label=tr("lg_grid"))
            catch_gg.plot(ax=ax, facecolor="orange", edgecolor="black", linewidth=1.5, alpha=0.85, label=tr("lg_catch"))
            if input_mode == "Site coordinates":
                gpd.GeoSeries([site_point], crs="EPSG:2100").plot(ax=ax, marker="*", markersize=250, color="blue", zorder=6, label=tr("lg_site"))
            ax.set_title(tr("map_title"))
            ax.set_xlabel("X (m)"); ax.set_ylabel("Y (m)")
            ax.set_aspect("equal"); ax.legend(); ax.grid(True, linestyle="--", alpha=0.3)
            ax.set_xlim(minx - buffer_m, maxx + buffer_m)
            ax.set_ylim(miny - buffer_m, maxy + buffer_m)
            st.pyplot(fig_map)
        except Exception as e:
            st.error(tr("err_map", e=e))

        # ------------------------------
        # Static Greece map with catchment marker
        # ------------------------------
        st.write(tr("h_static"))
        try:
            # Build Greek outline from the IDF grid and a centroid for the catchment
            greek_outline = greece_grid.unary_union
            outline_gdf = gpd.GeoDataFrame(geometry=[greek_outline], crs=greece_grid.crs)
            catch_centroid = catchment.geometry.unary_union.centroid
            centroid_gdf = gpd.GeoDataFrame(geometry=[catch_centroid], crs=catchment.crs)

            # Reproject to WGS84 for a simple lat/lon static map
            outline_wgs = outline_gdf.to_crs(epsg=4326)
            centroid_wgs = centroid_gdf.to_crs(epsg=4326)

            fig2, ax2 = plt.subplots(figsize=(6, 6))
            outline_wgs.boundary.plot(ax=ax2, linewidth=0.6, color="lightgray")
            centroid_wgs.plot(ax=ax2, marker='*', markersize=140, color='red', label=tr("lg_loc"), zorder=5)
            ax2.set_title(tr("static_title"))
            ax2.set_xlabel(tr("ax_lon")); ax2.set_ylabel(tr("ax_lat"))
            ax2.set_aspect("equal")
            ax2.legend()
            st.pyplot(fig2)
        except Exception as e:
            st.error(tr("err_static", e=e))

        # ------------------------------
        # Exports
        # Excel
        out_excel = io.BytesIO()
        with pd.ExcelWriter(out_excel, engine='xlsxwriter') as writer:
            df_all.to_excel(writer, sheet_name='Subbasin Hyetographs', index=False)
            df_total.to_excel(writer, sheet_name='Total Hyetograph', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Total Hyetograph']
            worksheet.write('J1', 'Phi (area reduction coefficient)')
            worksheet.write('J2', phi)
        out_excel.seek(0)
        st.download_button(
            tr("dl_excel"),
            data=out_excel.getvalue(),
            file_name=f"Hyetograph_T{T}_D{D}_dt{t}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # PNG download for hyetograph plot
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', dpi=300, bbox_inches='tight')
        img_buf.seek(0)
        st.download_button(
            tr("dl_png"),
            data=img_buf.getvalue(),
            file_name=f"DesignStorm_T{T}_D{D}.png",
            mime="image/png"
        )

        st.success(tr("ok_done"))

# ------------------------------
# Use and Reference tab
# ------------------------------
with tab_ref:
    st.header(tr("ref_header"))
    st.markdown(
        "\n" + tr("ref_title") + """
	
    1) Alamanos, A. & Papaioannou, G. (2025). Generating customized design storms for any Greek catchment based on official IDF parameters: The Catchment2Storm Python App. 6th IAHR Young Professionals Congress. Hydroinformatics Session. Online, 3-5 December 2025. https://www.researchgate.net/publication/398375263_Generating_customized_design_storms_for_any_Greek_catchment_based_on_official_IDF_parameters_The_Catchment2Storm_Python_App
    
    2) Alamanos, A. & Papaioannou, G. (2025). A national-scale IDF-based design storm hyetograph inventory: Applying the Catchment2Storm tool in Greece. The 9th International Electronic Conference on Water Sciences (IECWS9). Online. 11-14 November, 2025. https://sciforum.net/paper/view/26230
    
    3) Alamanos, A. (2025). Modernizing Greece’s flood defenses: learning from past disasters and leveraging advanced hydrological tools. The 6th International Electronic Conference on Applied Sciences (ASEC2025). Online. 9-11 December, 2025. https://sciforum.net/paper/view/27679
    
    4) Alamanos, A. & Nisiforou, O. (2026). Regional rainfall disparities across Greece calling for localized design standards for major urban centres, ports and farming sites: Insights from national-scale hyetograph modelling. 7th IAHR Young Professionals Congress. Online, 2-4 December 2026.
"""
    )

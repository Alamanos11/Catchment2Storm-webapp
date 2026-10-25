# Catchment2Storm web-app

**Customized design storms for any Greek catchment or site, based on the official Greek IDF (Ombrian) parameters.**

Catchment2Storm is a free web-app. You give it a catchment shapefile, or simply the coordinates of a site, and it returns a design storm hyetograph ready for hydrologic/hydraulic models (e.g. HEC-HMS, HEC-RAS). The official Greek IDF parameter grid is bundled with the app, so users do not need to download anything.

**Live app:** https://catchment2storm.streamlit.app/ 

---

## What it does

1. **Input**, either:
   - a **catchment shapefile** (one ZIP with .shp/.shx/.dbf/.prj, or the component files), or
   - the **coordinates of a site** (WGS84 latitude/longitude or Greek Grid EGSA87 / EPSG:2100 X/Y), with an optional site area:
     - area = 0: point site. The IDF parameters of the grid cell at the point are used, with no areal reduction (φ = 1).
     - area > 0: the site is represented as a circle of that area and processed exactly like a catchment shapefile.
2. **Overlay** with the official Greek IDF grid (Ombrian parameters α, η, ξ, λ, β per 5 km cell, ΥΠΕΚΑ), with area-weighting of the cells.
3. **IDF intensity:** i(T, κ) = λ · [(T/β)^ξ − 1] / (1 + κ/α)^η
4. **Areal reduction factor** φ (Koutsoyiannis & Xanthopoulos, 1999).
5. **Alternating Block Method (ABM)** design hyetograph.
6. **Outputs:** sub-basin IDF parameter table, total hyetograph table, plots and maps, plus downloadable Excel and PNG files.

User inputs: return period T (years), storm duration D (h) and time step t (h).

The app is available in **English and Greek**. Use the 🌐 selector at the top of the page to switch language.

## Repository contents

| File / folder | Purpose |
|---|---|
| `streamlit_catchment2storm.py` | The app |
| `translations.py` | App texts in English and Greek (🌐 language selector) |
| `data/ombrian_parameters.gpkg` | Greek IDF (Ombrian) parameter grid, EPSG:2100 |
| `requirements.txt` | Python packages, used by Streamlit Community Cloud |
| `.streamlit/config.toml` | Streamlit settings |
| `examples/watershedt.zip` | Example catchment shapefile for testing |

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_catchment2storm.py
```

Then open http://localhost:8501 in your browser.

## Data source

Greek IDF (Ombrian) curve parameters: Ministry of Environment & Energy (ΥΠΕΚΑ), Flood Risk Management Plans, 2nd cycle. Source: https://floods.ypeka.gr/sdkp-lap/omvries-2round/

## How to cite

1. Alamanos, A. & Papaioannou, G. (2025). Generating customized design storms for any Greek catchment based on official IDF parameters: The Catchment2Storm Python App. 6th IAHR Young Professionals Congress. Hydroinformatics Session. Online, 3-5 December 2025. https://www.researchgate.net/publication/398375263_Generating_customized_design_storms_for_any_Greek_catchment_based_on_official_IDF_parameters_The_Catchment2Storm_Python_App
2. Alamanos, A. & Papaioannou, G. (2025). A national-scale IDF-based design storm hyetograph inventory: Applying the Catchment2Storm tool in Greece. The 9th International Electronic Conference on Water Sciences (IECWS9). Online. 11-14 November, 2025. https://sciforum.net/paper/view/26230
3. Alamanos, A. (2025). Modernizing Greece’s flood defenses: learning from past disasters and leveraging advanced hydrological tools. The 6th International Electronic Conference on Applied Sciences (ASEC2025). Online. 9-11 December, 2025. https://sciforum.net/paper/view/27679
4. Alamanos, A. & Nisiforou, O. (2026). Regional rainfall disparities across Greece calling for localized design standards for major urban centres, ports and farming sites: Insights from national-scale hyetograph modelling. 7th IAHR Young Professionals Congress. Online, 2-4 December 2026.

## Contact

Angelos Alamanos, ModelBridge Labs (https://modelbridgelabs.com/)

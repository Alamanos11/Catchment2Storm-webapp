# -*- coding: utf-8 -*-
"""
User-interface texts of the Catchment2Storm app in English (en) and Greek (el).
Only displayed texts are translated; the calculations do not depend on the language.
To edit a text, change it here (keep the {placeholders} unchanged).
"""

TEXT = {
    # ------------------------------------------------------------------ English
    "en": {
        "lang_label": "🌐",
        # sidebar
        "sb_title": "Inputs",
        "mode_label": "How do you want to define your site?",
        "mode_help": "Upload a catchment shapefile, or - if you don't have a catchment but a smaller site - type its coordinates.",
        "mode_Catchment shapefile": "Catchment shapefile",
        "mode_Site coordinates": "Site coordinates",
        "upload_md": "Upload your catchment shapefile (either a ZIP containing .shp/.dbf/.shx/.prj OR upload the component files together).",
        "upload_label": "Catchment shapefile (.zip or components)",
        "upload_help": "Select either a single ZIP or multiple shapefile component files.",
        "coord_label": "Coordinate system of the site",
        "coord_WGS84": "WGS84 - latitude / longitude (decimal degrees)",
        "coord_EPSG:2100": "EPSG:2100 - Greek Grid (EGSA87) X / Y (m)",
        "lat": "Latitude (°N)",
        "lon": "Longitude (°E)",
        "x": "X - Easting (m)",
        "y": "Y - Northing (m)",
        "area_label": "Site area (km²) - optional",
        "area_help": "Leave 0 for a point site (IDF parameters of the grid cell at the point, no areal reduction: phi = 1). "
                     "If > 0, the site is represented by a circle of this area centred on the coordinates and is processed "
                     "exactly like a catchment shapefile (area-weighted IDF parameters and areal reduction phi).",
        "T_label": "Return period T (years)",
        "D_label": "Design storm duration D (hours)",
        "t_label": "Time step t (hours)",
        "err_t_gt_D": "Time step t must be smaller than duration D.",
        "warn_D_mod_t": "Design storm duration D is not an exact multiple of t. Last increment will be truncated.",
        "crs_label": "Assumed CRS if shapefile has no CRS",
        "crs_EPSG:2100 (Greek Grid)": "EPSG:2100 (Greek Grid)",
        "crs_EPSG:4326 (WGS84)": "EPSG:4326 (WGS84)",
        "run": "Run model",
        "grid_md": "**Using bundled Greek IDF grid** from `data/`.",
        "err_grid": "Failed to load IDF grid: {e}",
        # tabs
        "tab_intro": "Introduction",
        "tab_main": "Inputs and Run Model",
        "tab_ref": "Use and Reference",
        # introduction
        "intro_title": "Introduction",
        "intro_md": """
This is the web-app of the Catchment2Storm tool. Upload a shapefile for your catchment, and get customized design storm hyetographs. Based on the official Greek Ombrian IDF parameter grid.

**What it does**
- Accepts a catchment shapefile (ZIP or component files) - or, if you don't have a catchment but a smaller site, the site coordinates.
- Intersects the catchment with the official Greek IDF grid (Ombrian parameters per grid cell by YPEKA).
- Calculates area-weighted IDF intensities and generates a design storm hyetograph (incremental & centered by Alternate Block Method).
- Produces downloadable Excel and PNG outputs.

**What it needs**
- Upload a polygon shapefile of your catchment (coordinate system - CRS should be provided; if missing you can choose a default in the sidebar).
- *Or* select **Site coordinates** in the sidebar and type the coordinates of your site (WGS84 latitude/longitude or Greek Grid X/Y). Optionally give the site area (km²); leave it 0 for a point.
- Select your return period (T), duration (D) and time step (t) via the sidebar controls.
- In the side menu, press: Run Model, and explore/ download the results.

**What it produces**
- A tabular breakdown of IDF parameters per sub-basin (intersection with Ombrian/ IDF grid).
- Total incremental and ABM hyetograph (depth and intensity).
- Plots: ABM hyetograph, catchment over the IDF grid, and a static map of Greece with your catchment location.
- Downloadable Excel and PNG files with results.
""",
        # main tab
        "grid_info": "Greek IDF grid info",
        "rows": "Rows:",
        "crs": "CRS:",
        "cols": "Available columns:",
        "idf_info": "IDF formulation according to Greek Ombrian curves (ΥΠΕΚΑ / ΥΠΕΧΩΔΕ).",
        "err_site": "Could not build the site from the coordinates: {e}",
        "site_info": "Site at X = {x:.2f} m, Y = {y:.2f} m (EPSG:2100). ",
        "site_point": "Point site: IDF parameters of the grid cell at the point, no areal reduction (phi = 1).",
        "site_circle": "Site represented by a circle of {a:g} km² centred on the coordinates.",
        "err_no_upload": "Please upload the catchment shapefile (ZIP or component files).",
        "err_files": "Failed to process uploaded files: {e}",
        "err_read": "GeoPandas failed to read the shapefile: {e}",
        "err_empty": "Uploaded catchment has empty geometry or zero area.",
        "warn_nocrs": "Uploaded shapefile had no CRS. Set to {crs}.",
        "err_intersect": "Spatial intersection failed: {e}",
        "err_nointersect": "No intersection between the catchment and the IDF grid. Check the geometry and grid coverage.",
        "warn_outside": "The site lies outside the Greek IDF grid coverage. Please check the coordinates and the selected coordinate system.",
        "err_missing_col": "IDF grid is missing required parameter column for '{name}'. Expected one of: {variants}",
        "ok_sub": "Sub-basins and IDF parameters extracted.",
        "h_sub": "## Sub-basin IDF parameters",
        "exp_idf": "IDF formula — brief explanation",
        "md_idf": """
**IDF (Intensity–Duration–Frequency)** in this app uses the Greek IDF *Ombrian* parameterisation.

The intensity formula used is:

\\[
i(T, \\kappa) = \\lambda \\cdot \\frac{(T/\\beta)^{\\xi} - 1}{\\left(1 + \\kappa/\\alpha\\right)^{\\eta}}
\\]

where:
- \\(T\\) is the return period (years),
- \\(\\kappa\\) is the duration (hours),
- \\(\\alpha, \\eta, \\xi, \\lambda, \\beta\\) are the Ombrian parameters from the grid.

The model computes intensity per duration for each grid cell and area-weights them by intersection percentage.
""",
        "exp_phi": "Area reduction coefficient (phi) — brief explanation",
        "md_phi": """
For catchments larger than point scale, rainfall temporal variability is reduced.\x20\x20
This app uses a semi-empirical area-reduction expression (Koutsogiannis & Ksanthopoulos, 1999):

\\[
\\phi = \\max\\left(0.25,\\, 1 - 0.048 \\cdot \\frac{A^{0.36 - 0.01\\ln A}}{D^{0.35}}\\right)
\\]

where:
- \\(A\\) is catchment area in km²,
- \\(D\\) is the design storm duration in hours.

\\(\\phi\\) is applied to incremental depths to account for spatial averaging.
""",
        "exp_abm": "Alternate Block Method (ABM) — brief explanation",
        "md_abm": """
The ABM reorders incremental rainfall depths so the largest increments occur near the storm peak,
producing a more realistic design hyetograph for runoff modelling.

Procedure (conceptual):
1. Sort incremental depths descending.
2. Place the largest at the center time-step, then alternately place next largest left and right of center.
3. Resulting sequence is the ABM hyetograph.
""",
        "h_phi": "### Area reduction coefficient (phi):",
        "phi_line": "**Phi = {phi:.6f}** (A = {A:.4f} km², D = {D} h)",
        "h_total": "## Total Hyetograph (incremental & ABM)",
        "ax_duration": "Duration (hr)",
        "ax_precip": "Precipitation (mm)",
        "hyeto_title": "Design Storm Hyetograph (T={T} yr, D={D} hr)",
        "h_map": "## Map preview — Catchment over Greek IDF grid",
        "lg_grid": "Ombrian IDF grid",
        "lg_catch": "Catchment",
        "lg_site": "Site",
        "map_title": "Catchment location over Greek IDF grid (EPSG:2100)",
        "err_map": "Map preview failed: {e}",
        "h_static": "## Static map — Greece with catchment location",
        "lg_loc": "Catchment location",
        "static_title": "Greece — catchment location (approx.)",
        "ax_lon": "Longitude",
        "ax_lat": "Latitude",
        "err_static": "Static Greece map failed: {e}",
        "dl_excel": "Download results (Excel)",
        "dl_png": "Download hyetograph (PNG)",
        "ok_done": "Run complete. Files ready for download.",
        # reference tab
        "ref_header": "Use and Reference",
        "ref_title": "**Reference:** ",
    },
    # ------------------------------------------------------------------ Greek
    "el": {
        "lang_label": "🌐",
        # sidebar
        "sb_title": "Δεδομένα εισόδου",
        "mode_label": "Πώς θέλετε να ορίσετε την περιοχή μελέτης;",
        "mode_help": "Ανεβάστε shapefile της λεκάνης απορροής ή - αν δεν έχετε λεκάνη αλλά μια μικρότερη θέση - πληκτρολογήστε τις συντεταγμένες της.",
        "mode_Catchment shapefile": "Shapefile λεκάνης απορροής",
        "mode_Site coordinates": "Συντεταγμένες θέσης",
        "upload_md": "Ανεβάστε το shapefile της λεκάνης απορροής (είτε ένα ZIP με τα .shp/.dbf/.shx/.prj ΕΙΤΕ όλα τα επιμέρους αρχεία μαζί).",
        "upload_label": "Shapefile λεκάνης (.zip ή επιμέρους αρχεία)",
        "upload_help": "Επιλέξτε είτε ένα αρχείο ZIP είτε τα επιμέρους αρχεία του shapefile.",
        "coord_label": "Σύστημα συντεταγμένων της θέσης",
        "coord_WGS84": "WGS84 - γεωγραφικό πλάτος / μήκος (δεκαδικές μοίρες)",
        "coord_EPSG:2100": "EPSG:2100 - ΕΓΣΑ87 X / Y (m)",
        "lat": "Γεωγραφικό πλάτος (°Β)",
        "lon": "Γεωγραφικό μήκος (°Α)",
        "x": "X - Τετμημένη (m)",
        "y": "Y - Τεταγμένη (m)",
        "area_label": "Έκταση θέσης (km²) - προαιρετικά",
        "area_help": "Αφήστε 0 για σημειακή θέση (παράμετροι όμβριας καμπύλης του κελιού στο σημείο, χωρίς επιφανειακή μείωση: φ = 1). "
                     "Αν > 0, η θέση αναπαρίσταται με κύκλο αυτής της έκτασης με κέντρο τις συντεταγμένες και υπολογίζεται "
                     "ακριβώς όπως ένα shapefile λεκάνης (σταθμισμένες ως προς την έκταση παράμετροι και συντελεστής επιφανειακής μείωσης φ).",
        "T_label": "Περίοδος επαναφοράς T (έτη)",
        "D_label": "Διάρκεια καταιγίδας σχεδιασμού D (ώρες)",
        "t_label": "Χρονικό βήμα t (ώρες)",
        "err_t_gt_D": "Το χρονικό βήμα t πρέπει να είναι μικρότερο από τη διάρκεια D.",
        "warn_D_mod_t": "Η διάρκεια D δεν είναι ακέραιο πολλαπλάσιο του t. Το τελευταίο διάστημα θα περικοπεί.",
        "crs_label": "Σύστημα συντεταγμένων αν το shapefile δεν έχει CRS",
        "crs_EPSG:2100 (Greek Grid)": "EPSG:2100 (ΕΓΣΑ87)",
        "crs_EPSG:4326 (WGS84)": "EPSG:4326 (WGS84)",
        "run": "Εκτέλεση μοντέλου",
        "grid_md": "**Χρησιμοποιείται ο ενσωματωμένος κάναβος όμβριων καμπυλών** από τον φάκελο `data/`.",
        "err_grid": "Αποτυχία φόρτωσης του κανάβου όμβριων καμπυλών: {e}",
        # tabs
        "tab_intro": "Εισαγωγή",
        "tab_main": "Δεδομένα και εκτέλεση",
        "tab_ref": "Χρήση και βιβλιογραφία",
        # introduction
        "intro_title": "Εισαγωγή",
        "intro_md": """
Αυτή είναι η διαδικτυακή εφαρμογή του εργαλείου Catchment2Storm. Ανεβάστε ένα shapefile της λεκάνης απορροής σας και λάβετε εξατομικευμένα υετογραφήματα καταιγίδας σχεδιασμού, με βάση τον επίσημο ελληνικό κάναβο παραμέτρων όμβριων καμπυλών.

**Τι κάνει**
- Δέχεται shapefile λεκάνης απορροής (ZIP ή επιμέρους αρχεία) - ή, αν δεν έχετε λεκάνη αλλά μια μικρότερη θέση, τις συντεταγμένες της θέσης.
- Τέμνει τη λεκάνη με τον επίσημο ελληνικό κάναβο όμβριων καμπυλών (παράμετροι ανά κελί του κανάβου, ΥΠΕΚΑ).
- Υπολογίζει σταθμισμένες ως προς την έκταση εντάσεις βροχής και παράγει υετογράφημα καταιγίδας σχεδιασμού (διαφορικά ύψη, κεντραρισμένα με τη Μέθοδο Εναλλασσόμενων Μπλοκ).
- Παράγει αποτελέσματα σε Excel και PNG για λήψη.

**Τι χρειάζεται**
- Ανεβάστε ένα πολυγωνικό shapefile της λεκάνης σας (το σύστημα συντεταγμένων - CRS πρέπει να δίνεται· αν λείπει, μπορείτε να επιλέξετε ένα στο πλαϊνό μενού).
- *Ή* επιλέξτε **Συντεταγμένες θέσης** στο πλαϊνό μενού και πληκτρολογήστε τις συντεταγμένες της θέσης σας (WGS84 πλάτος/μήκος ή ΕΓΣΑ87 X/Y). Προαιρετικά δώστε την έκταση της θέσης (km²)· αφήστε 0 για σημείο.
- Επιλέξτε περίοδο επαναφοράς (T), διάρκεια (D) και χρονικό βήμα (t) από το πλαϊνό μενού.
- Στο πλαϊνό μενού πατήστε: Εκτέλεση μοντέλου, και δείτε/κατεβάστε τα αποτελέσματα.

**Τι παράγει**
- Πίνακα με τις παραμέτρους όμβριων καμπυλών ανά υπολεκάνη (τομή με τον κάναβο).
- Συνολικό υετογράφημα, διαφορικό και κατά ABM (ύψος και ένταση βροχής).
- Διαγράμματα: υετογράφημα ABM, λεκάνη πάνω στον κάναβο όμβριων καμπυλών και χάρτη της Ελλάδας με τη θέση της λεκάνης.
- Αρχεία Excel και PNG με τα αποτελέσματα για λήψη.
""",
        # main tab
        "grid_info": "Πληροφορίες κανάβου όμβριων καμπυλών",
        "rows": "Γραμμές:",
        "crs": "CRS:",
        "cols": "Διαθέσιμες στήλες:",
        "idf_info": "Όμβριες καμπύλες σύμφωνα με τις επίσημες ελληνικές όμβριες καμπύλες (ΥΠΕΚΑ / ΥΠΕΧΩΔΕ).",
        "err_site": "Δεν ήταν δυνατή η δημιουργία της θέσης από τις συντεταγμένες: {e}",
        "site_info": "Θέση στο X = {x:.2f} m, Y = {y:.2f} m (EPSG:2100). ",
        "site_point": "Σημειακή θέση: παράμετροι όμβριας καμπύλης του κελιού στο σημείο, χωρίς επιφανειακή μείωση (φ = 1).",
        "site_circle": "Η θέση αναπαρίσταται με κύκλο έκτασης {a:g} km² με κέντρο τις συντεταγμένες.",
        "err_no_upload": "Ανεβάστε το shapefile της λεκάνης (ZIP ή επιμέρους αρχεία).",
        "err_files": "Αποτυχία επεξεργασίας των αρχείων: {e}",
        "err_read": "Το GeoPandas δεν μπόρεσε να διαβάσει το shapefile: {e}",
        "err_empty": "Η λεκάνη έχει κενή γεωμετρία ή μηδενική έκταση.",
        "warn_nocrs": "Το shapefile δεν είχε CRS. Ορίστηκε σε {crs}.",
        "err_intersect": "Αποτυχία χωρικής τομής: {e}",
        "err_nointersect": "Η λεκάνη δεν τέμνει τον κάναβο όμβριων καμπυλών. Ελέγξτε τη γεωμετρία και την κάλυψη του κανάβου.",
        "warn_outside": "Η θέση βρίσκεται εκτός της κάλυψης του ελληνικού κανάβου όμβριων καμπυλών. Ελέγξτε τις συντεταγμένες και το επιλεγμένο σύστημα συντεταγμένων.",
        "err_missing_col": "Από τον κάναβο λείπει η στήλη παραμέτρου '{name}'. Αναμενόταν μία από: {variants}",
        "ok_sub": "Οι υπολεκάνες και οι παράμετροι όμβριων καμπυλών εξήχθησαν.",
        "h_sub": "## Παράμετροι όμβριων καμπυλών ανά υπολεκάνη",
        "exp_idf": "Τύπος όμβριων καμπυλών — σύντομη επεξήγηση",
        "md_idf": """
Οι **όμβριες καμπύλες (Ένταση–Διάρκεια–Συχνότητα, IDF)** σε αυτή την εφαρμογή ακολουθούν την παραμετροποίηση των επίσημων ελληνικών όμβριων καμπυλών.

Ο τύπος της έντασης είναι:

\\[
i(T, \\kappa) = \\lambda \\cdot \\frac{(T/\\beta)^{\\xi} - 1}{\\left(1 + \\kappa/\\alpha\\right)^{\\eta}}
\\]

όπου:
- \\(T\\) η περίοδος επαναφοράς (έτη),
- \\(\\kappa\\) η διάρκεια (ώρες),
- \\(\\alpha, \\eta, \\xi, \\lambda, \\beta\\) οι παράμετροι της όμβριας καμπύλης από τον κάναβο.

Το μοντέλο υπολογίζει την ένταση ανά διάρκεια για κάθε κελί του κανάβου και τη σταθμίζει με το ποσοστό της έκτασης τομής.
""",
        "exp_phi": "Συντελεστής επιφανειακής μείωσης (φ) — σύντομη επεξήγηση",
        "md_phi": """
Για λεκάνες μεγαλύτερες από σημειακή κλίμακα, η χρονική μεταβλητότητα της βροχής μειώνεται.\x20\x20
Η εφαρμογή χρησιμοποιεί μια ημι-εμπειρική σχέση επιφανειακής μείωσης (Κουτσογιάννης & Ξανθόπουλος, 1999):

\\[
\\phi = \\max\\left(0.25,\\, 1 - 0.048 \\cdot \\frac{A^{0.36 - 0.01\\ln A}}{D^{0.35}}\\right)
\\]

όπου:
- \\(A\\) η έκταση της λεκάνης σε km²,
- \\(D\\) η διάρκεια της καταιγίδας σχεδιασμού σε ώρες.

Ο \\(\\phi\\) εφαρμόζεται στα διαφορικά ύψη βροχής για να ληφθεί υπόψη η χωρική εξομάλυνση.
""",
        "exp_abm": "Μέθοδος Εναλλασσόμενων Μπλοκ (ABM) — σύντομη επεξήγηση",
        "md_abm": """
Η ABM αναδιατάσσει τα διαφορικά ύψη βροχής ώστε τα μεγαλύτερα να βρίσκονται κοντά στην αιχμή της καταιγίδας,
δίνοντας ένα πιο ρεαλιστικό υετογράφημα σχεδιασμού για την προσομοίωση της απορροής.

Διαδικασία (εννοιολογικά):
1. Ταξινόμηση των διαφορικών υψών κατά φθίνουσα σειρά.
2. Το μεγαλύτερο τοποθετείται στο κεντρικό χρονικό βήμα και τα επόμενα εναλλάξ αριστερά και δεξιά του κέντρου.
3. Η ακολουθία που προκύπτει είναι το υετογράφημα ABM.
""",
        "h_phi": "### Συντελεστής επιφανειακής μείωσης (φ):",
        "phi_line": "**φ = {phi:.6f}** (A = {A:.4f} km², D = {D} h)",
        "h_total": "## Συνολικό υετογράφημα (διαφορικό & ABM)",
        "ax_duration": "Διάρκεια (h)",
        "ax_precip": "Ύψος βροχής (mm)",
        "hyeto_title": "Υετογράφημα καταιγίδας σχεδιασμού (T={T} έτη, D={D} h)",
        "h_map": "## Προεπισκόπηση χάρτη — Λεκάνη πάνω στον κάναβο όμβριων καμπυλών",
        "lg_grid": "Κάναβος όμβριων καμπυλών",
        "lg_catch": "Λεκάνη",
        "lg_site": "Θέση",
        "map_title": "Θέση λεκάνης στον κάναβο όμβριων καμπυλών (EPSG:2100)",
        "err_map": "Αποτυχία προεπισκόπησης χάρτη: {e}",
        "h_static": "## Χάρτης — Ελλάδα και θέση της λεκάνης",
        "lg_loc": "Θέση λεκάνης",
        "static_title": "Ελλάδα — θέση της λεκάνης (κατά προσέγγιση)",
        "ax_lon": "Γεωγραφικό μήκος",
        "ax_lat": "Γεωγραφικό πλάτος",
        "err_static": "Αποτυχία χάρτη της Ελλάδας: {e}",
        "dl_excel": "Λήψη αποτελεσμάτων (Excel)",
        "dl_png": "Λήψη υετογραφήματος (PNG)",
        "ok_done": "Η εκτέλεση ολοκληρώθηκε. Τα αρχεία είναι έτοιμα για λήψη.",
        # reference tab
        "ref_header": "Χρήση και βιβλιογραφία",
        "ref_title": "**Βιβλιογραφία:** ",
    },
}

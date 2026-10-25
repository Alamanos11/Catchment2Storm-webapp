# How to test and publish Catchment2Storm as a free web-app

The app is published on **Streamlit Community Cloud**, which is free. It runs the app straight from a public **GitHub** repository and gives it a public link, e.g. `https://catchment2storm.streamlit.app`. Users only need a browser, and the IDF grid comes with the app.

---

## Step 0 – Test it locally first (Anaconda Prompt)

```
cd /d "E:\publications\GitHub_papers\Catchment2Storm_webapp"
pip install -r requirements.txt
streamlit run streamlit_catchment2storm.py
```

You no longer need `--server.fileWatcherType none`, because it is now set in `.streamlit/config.toml`.

Things to check:
- **Catchment shapefile mode:** upload `examples/watershedt.zip`. You should get the same results as the current app.
- **Site coordinates mode:** choose *Site coordinates* in the sidebar and press *Run model*. The default site is central Athens. Try a point (area = 0) and a site with an area.

> If you get an error about `quad_segs`, your local Shapely is older than 2.0. Update it with `pip install -U shapely geopandas`. The cloud installs the right versions automatically.

---

## Step 1 – Create the GitHub repository

1. Sign in at https://github.com and click **New repository** (the "+" at the top right).
2. Use a name such as `Catchment2Storm`, set it to **Public**, and leave "Add a README" unticked, since we already have one. Click **Create repository**.
3. On the empty repository page, click **"uploading an existing file"**.
4. Drag **the contents** of `E:\publications\GitHub_papers\Catchment2Storm_webapp` into the browser. Upload the contents, not the folder itself. That means:
   - `streamlit_catchment2storm.py`
   - `translations.py`
   - `requirements.txt`
   - `README.md`
   - `DEPLOY_GUIDE.md` (optional)
   - `.gitignore`
   - the folders `data`, `.streamlit` and `examples`
5. Click **Commit changes**.

Then check that the repository shows `data/ombrian_parameters.gpkg` and `.streamlit/config.toml`. If you prefer, use GitHub Desktop instead: *File → Add local repository →* this folder, then *Publish repository*.

---

## Step 2 – Deploy on Streamlit Community Cloud (free)

1. Go to https://share.streamlit.io and click **Continue with GitHub**. Authorise Streamlit to access your repositories.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Fill in:
   - **Repository:** `<your-github-user>/Catchment2Storm`
   - **Branch:** `main`
   - **Main file path:** `streamlit_catchment2storm.py`
   - **App URL:** choose a custom subdomain, e.g. `catchment2storm`, which gives `https://catchment2storm.streamlit.app`
4. Open **Advanced settings** and choose **Python 3.12**.
5. Click **Deploy**. The first build takes a few minutes while it installs the packages. After that the app is live.

---

## Step 3 – After deployment

- Put the live link in `README.md` (top) and on https://modelbridgelabs.com.
- **Updates:** edit or re-upload `streamlit_catchment2storm.py` on GitHub. The app redeploys automatically within a minute or two.
- **Sleeping:** free apps go to sleep after 12 hours without visitors. The next visitor sees a button to wake the app up, which takes about 30 seconds.
- **DOI (optional):** to fill the `DOI:XXX` in the reference, connect the GitHub repository to **Zenodo** (https://zenodo.org → GitHub). Then create a GitHub *Release*, and Zenodo will mint a citable DOI for that version.
- **Licence (optional):** add one on GitHub (*Add file → Create new file →* name it `LICENSE` → *Choose a licence template*). This tells others how they may reuse the code.

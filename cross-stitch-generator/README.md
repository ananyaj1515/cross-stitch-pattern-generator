# Cross-Stitch Pattern Generator

A web app that turns a user-uploaded image into a cross-stitch reference pattern. Users can upload an image, choose a canvas/grid size, and set the number of colours to use. The app quantizes the image, matches the resulting palette to DMC thread colours, and displays a stitch-style pattern together with the DMC thread key.

## What it does

- Accepts an image upload from the user.
- Lets the user control the output size with a canvas/grid parameter.
- Uses the chosen number of colours as a clustering hyperparameter.
- Runs k-means clustering on the resized image colours.
- Maps clustered colours to DMC thread colours using the `backend/dmc.csv` database.
- Returns the generated stitch grid plus DMC colour information so the user can recreate the design.

## Project structure

- `cross-stitch-generator/` — React front-end interface.
  - Upload image, choose grid size, choose number of colours.
  - Sends the image and parameters to the backend API.
  - Visualizes the generated stitch pattern.
- `backend/` — Flask API and image processing pipeline.
  - Resizes the image.
  - Runs k-means clustering.
  - Matches cluster colours to DMC entries in `dmc.csv`.
  - Returns the stitch grid and thread key.

## How the processing works

1. The user uploads an image and selects a maximum grid size and number of colour clusters.
2. The backend resizes the image to the requested scale.
3. K-means clustering reduces the image to the requested number of representative colours.
4. Each cluster colour is matched against the DMC colour table to find the closest thread code and name.
5. The final stitched pattern and DMC reference key are returned to the UI.

## Tech stack

- Frontend: React + React Scripts
- Backend: Flask, NumPy, scikit-learn, Pillow, pandas
- Colour matching: DMC thread database stored in `backend/dmc.csv`

## Local development

### Frontend

From the `cross-stitch-generator/` directory:

```bash
npm install
npm start
```

The React app opens locally and lets you upload an image and generate a pattern.

### Backend

From the `backend/` directory:

```bash
pip install -r requirements.txt
python wsgi.py
```

The Flask API serves the image processing endpoint used by the frontend.

## API usage

The frontend posts the uploaded image and two parameters to the backend:

- `max_dim` — the resized canvas/grid size
- `n_colors` — the number of cluster colours for quantization

The backend returns:

- `pattern_grid` — a grid of DMC thread codes representing the stitch layout
- `key` — mapped thread names, RGB values, and stitch counts
- `dimensions` — the generated pattern dimensions

## Notes

- The DMC matching database is stored in `backend/dmc.csv`.
- The current React app is configured to point at the hosted backend URL in `src/App.js`. If running locally, update the API endpoint to point to your local Flask server.

## Future improvements

- Add downloadable pattern exports.
- Improve colour handling and preview rendering.
- Support alternative thread palettes and higher-resolution pattern generation.

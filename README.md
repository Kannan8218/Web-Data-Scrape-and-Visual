# IMDB Data Scraping and Visualization

## Python Version
This project requires **Python 3.12**.

## Files in This Folder
This folder contains only **two files**:  
1. `IMDB_data-scrape.ipynb` - For scraping and storing IMDB data.  
2. `IMDB_data-visual.py` - For visualizing the scraped IMDB data.  

## Files Description
1. **IMDB_data-scrape.ipynb**  
   - A Jupyter Notebook that scrapes IMDB data using web scraping techniques.
   - Extracts movie details such as title, rating, votes, duration, and genre.
   - Saves the raw scraped movie details into separate CSV files for different genres:
     - `Action.csv`
     - `Adventure.csv`
     - `Animation.csv`
     - `Comedy.csv`
     - `Crime.csv`
   - Cleans the data and stores it in new CSV files:
     - `Action-1.csv`
     - `Adventure-1.csv`
     - `Animation-1.csv`
     - `Comedy-1.csv`
     - `Crime-1.csv`
   - Merges all cleaned data into a single file:
     - `merge_data.csv`
   - Stores the final processed data in a SQLite database (`IMDB.db`).

2. **IMDB_data-visual.py**  
   - A Python script using **Streamlit** to visualize IMDB movie data.
   - Connects to the SQLite database (`IMDB.db`).
   - Provides various visualizations, including bar charts, histograms, and heatmaps, to analyze trends in ratings, votes, and genres.

## Dependencies
Ensure you have the following Python packages installed:

- `pandas` - For handling data in tabular format.
- `sqlite3` - To interact with the SQLite database.
- `streamlit` - For creating an interactive web-based visualization.
- `matplotlib` - For generating plots and charts.
- `seaborn` - For advanced visualizations and heatmaps.

## Installation
Install the required dependencies using:
```sh
pip install pandas streamlit matplotlib seaborn
```

## How to Run
1. **Run the Data Scraping Notebook**  
   - Open `IMDB_data-scrape.ipynb` in Jupyter Notebook and execute all cells.
   - This will store:
     - Raw scraped data in genre-based CSV files.
     - Cleaned data in `*-1.csv` files.
     - Merged data in `merge_data.csv`.
     - Processed data in `IMDB.db`.

2. **Run the Visualization Script**  
   - Execute the Streamlit app with the following command:
   ```sh
   streamlit run IMDB_data-visual.py
   ```
3. Open the displayed **local URL** in your web browser to explore the IMDB data visualizations.

## Adding More Genres
If you want to retrieve more genre-specific movie details, follow these steps:
- Add the new IMDb genre link to the `self.urls` list.
- Include the corresponding genre name at the same index in the `self.genres` list.
- Ensure that both the URL in `self.urls` and the genre name in `self.genres` align correctly.

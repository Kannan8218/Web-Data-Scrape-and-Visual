import pandas as pd
import sqlite3 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


try:
    conn = sqlite3.connect("IMDB.db")
except Exception as e:
    print("ERROR -> Database connection: ", e)

def visualizations():
    st.header("1. Top 10 Movies by Rating and Voting Counts")
    st.subheader("Highest Ratings and Significant Voting engagement")
    if conn:
        try:
            q = """WITH ranked_movies AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY Title ORDER BY Votes DESC, Rating DESC) AS rn
                FROM Movies)SELECT * FROM ranked_movies WHERE rn = 1 ORDER BY Votes DESC, Rating DESC LIMIT 10;"""
            a = pd.read_sql_query(q, conn)
            st.dataframe(a[["Title", "Rating", "Votes"]].reset_index(drop=True))
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.bar(a["Title"], a["Votes"], color="skyblue", label="Votes", width=0.4)
            ax.set_xlabel("Movie Title")
            ax.set_ylabel("Votes")
            ax.set_title("Top 10 Unique Movies by Votes and Rating")
            plt.xticks(rotation=20, ha="right")
            ax.tick_params(axis="both", labelsize=15)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("2. Genre Distribution")
    st.subheader("Movie Count by Genre")
    if conn:
        try:
            q = """SELECT Genre, COUNT(*) AS Count FROM Movies GROUP BY Genre ORDER BY Count DESC;"""
            a = pd.read_sql_query(q, conn)
            st.write(a)
            fig, ax = plt.subplots(figsize=(15,5))
            ax.bar(a["Genre"], a["Count"], color="skyblue", width=0.4)
            ax.set_xlabel("Genre")
            ax.set_ylabel("Number of Movies")
            ax.set_title("Genre Distribution")
            plt.xticks(rotation=20, ha="right")
            ax.tick_params(axis="both", labelsize=15) 
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("3. Average Duration of movies")
    st.subheader("Average Movie Duration per Genre")
    if conn:
        try:
            q = """WITH converted_duration AS (
                SELECT Genre, (CAST(SUBSTR(Duration, 1, INSTR(Duration, '.') - 1) AS INTEGER) * 60 + 
                CAST(SUBSTR(Duration, INSTR(Duration, '.') + 1) AS INTEGER)) AS Duration_in_minutes
                FROM Movies WHERE Duration LIKE '%.%')
            SELECT Genre, ROUND(AVG(Duration_in_minutes), 2) AS "Avg Duration (min)"
            FROM converted_duration GROUP BY Genre ORDER BY "Avg Duration (min)";"""
            a = pd.read_sql_query(q, conn)
            st.write(a)
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.barh(a["Genre"], a["Avg Duration (min)"], color="skyblue", height=0.5)
            ax.set_xlabel("Average Duration (in minutes)")
            ax.set_ylabel("Genre")
            ax.set_title("Average Movie Duration by Genre")
            plt.xticks(rotation=0, ha="center")
            ax.tick_params(axis="both", labelsize=15) 
            ax.grid(axis="x", linestyle="--", alpha=0.7)  
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("4. Voting Trends by Genre")
    st.subheader("Average Voting Counts per Genre")
    if conn:
        try:
            q = """SELECT Genre, ROUND(SUM(Votes) * 1.0 / COUNT(Title), 2) AS "Avg Votes Per Movie"
            FROM Movies GROUP BY Genre ORDER BY "Avg Votes Per Movie" DESC;"""
            b = pd.read_sql_query(q, conn)
            st.write(b)
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.bar(b["Genre"], b["Avg Votes Per Movie"], color="skyblue", width=0.4)
            ax.set_xlabel("Genre")
            ax.set_ylabel("Average Votes Per Movie")
            ax.set_title("Voting Trends by Genre")
            plt.xticks(rotation=20, ha="right")
            ax.tick_params(axis="both", labelsize=15) 
            ax.grid(axis="y", linestyle="--", alpha=0.7) 
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("5. Rating Distribution")
    st.subheader("Histogram chart for Movie Ratings")
    if conn:
        try:
            q = """SELECT Rating FROM Movies WHERE Rating IS NOT NULL""" 
            ratings_data = pd.read_sql_query(q, conn)
            bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            bin_labels = [f"{bin_edges[i]} - {bin_edges[i+1]}" for i in range(len(bin_edges)-1)]
            bin_counts = pd.cut(ratings_data["Rating"], bins=bin_edges, labels=bin_labels, include_lowest=True).value_counts().sort_index()
            table_data = pd.DataFrame({"Bin Range": bin_counts.index, "Frequency": bin_counts.values})
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.hist(ratings_data["Rating"], bins=bin_edges, color="skyblue", edgecolor="black", alpha=0.7)
            ax.set_xlabel("Rating")
            ax.set_ylabel("Frequency")
            ax.set_title("Histogram of Movie Ratings")
            plt.xticks(range(0, 11))
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            st.table(table_data)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")


    
    st.header("6. Genre-Based Rating Leaders")
    st.subheader("Top-Rated movie for each Genre")
    if conn:
        try:
            q = """WITH ranked_movies AS (SELECT Genre, Title, Rating,
                RANK() OVER (PARTITION BY Genre ORDER BY Rating DESC) AS rank
                FROM Movies WHERE Rating IS NOT NULL )
            SELECT Genre, Title, Rating FROM ranked_movies
            WHERE rank = 1 ORDER BY Genre;"""
            a = pd.read_sql_query(q, conn)
            st.write(a.reset_index(drop=True))
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.barh(a["Genre"], a["Rating"], color="skyblue", height=0.5)
            ax.set_xlabel("Rating")
            ax.set_ylabel("Genre")
            ax.set_title("Top-Rated Movie by Genre")
            plt.xticks(rotation=0, ha="center")
            ax.tick_params(axis="both", labelsize=15) 
            ax.grid(axis="x", linestyle="--", alpha=0.7)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")   
    
    st.header("7. Most Popular Genres by Voting")
    st.subheader("Highest Total Voting counts in a Pie-Chart")
    if conn:
        try:
            q = """WITH genre_votes AS (SELECT Genre, SUM(Votes) AS total_votes
            FROM Movies WHERE Votes IS NOT NULL GROUP BY Genre),
            total AS (SELECT SUM(total_votes) AS grand_total FROM genre_votes)
            SELECT gv.Genre, gv.total_votes AS "Total Votes", 
            ROUND((gv.total_votes * 100.0) / t.grand_total, 1) AS "Percentage (%)"
            FROM genre_votes gv, total t ORDER BY gv.total_votes DESC; """
            d = pd.read_sql_query(q, conn)
            st.write(d)
            fig, ax = plt.subplots(figsize=(4, 4))
            w, t, au = ax.pie(d["Total Votes"], labels=d["Genre"], autopct="%1.1f%%",startangle=140, labeldistance=1.1, pctdistance=0.7)
            for i in au:
                i.set_rotation(320)  
                i.set_fontsize(12)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("8. Duration Extremes")
    st.subheader("Shortest and Longest Movies in Table view")
    if conn:
        try:
            q = """WITH Converted_Duration AS (SELECT Title, Genre, 
                CAST(Duration AS INTEGER) * 60 + ROUND((Duration - CAST(Duration AS INTEGER)) * 100, 0) AS Duration_Minutes 
                FROM Movies),
                Shortest AS (SELECT 'Shortest Movie' AS Label, Title, Genre, Duration_Minutes
                FROM Converted_Duration WHERE Duration_Minutes = (SELECT MIN(Duration_Minutes) FROM Converted_Duration)),
                Longest AS (SELECT 'Longest Movie' AS Label, Title, Genre, Duration_Minutes
                FROM Converted_Duration WHERE Duration_Minutes = (SELECT MAX(Duration_Minutes) FROM Converted_Duration))
                SELECT Label, Title, Genre, 
                CAST(Duration_Minutes / 60 AS INTEGER) || ' hr ' || CAST(Duration_Minutes % 60 AS INTEGER) || ' min' AS Duration 
                FROM Shortest UNION ALL SELECT Label, Title, Genre, 
                CAST(Duration_Minutes / 60 AS INTEGER) || ' hr ' || CAST(Duration_Minutes % 60 AS INTEGER) || ' min' AS Duration 
                FROM Longest;"""
            table_data = pd.read_sql_query(q, conn)
            st.table(table_data)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("9. Ratings by Genre")
    st.subheader("Heatmap to compare Average Ratings across Genres")
    if conn:
        try:
            q = """SELECT Genre, ROUND(AVG(Rating), 2) AS "Avg Rating" FROM Movies GROUP BY Genre
            ORDER BY "Avg Rating" DESC;"""
            a = pd.read_sql_query(q, conn)
            st.table(a)
            fig, ax = plt.subplots(figsize=(8, 4))
            pivot_table = a.pivot_table(values="Avg Rating", index="Genre")
            sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=1, linecolor="black", cbar=True, ax=ax)
            ax.set_title("Average Ratings Across Genres", fontsize=14)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")
    
    st.header("10. Correlation Analysis")
    st.subheader("Relationship between Ratings and Voting Counts ")
    if conn:
        try:
            q = """SELECT Rating, Votes FROM Movies ORDER BY Rating DESC, Votes DESC;"""
            a = pd.read_sql_query(q, conn)
            fig, ax = plt.subplots(figsize=(15, 10))
            sns.scatterplot(x=a["Rating"], y=a["Votes"], alpha=0.6, color="royalblue", edgecolor="black")
            ax.set_xlabel("Movie Ratings", fontsize=12)
            ax.set_ylabel("Total Votes", fontsize=12)
            ax.set_title("Relationship Between Ratings and Voting Counts")
            ax.grid(True, linestyle="--", alpha=0.6)
            st.pyplot(fig)
        except Exception as e:
                st.warning(f"Error -> {e}")
    else:
        st.warning("Database Connection is stopped")

def filtering():
    st.title("Filtering page")
    
    if conn:#filter data by duration
        st.subheader("1. Filtered Movies Based on Duration")
        dr = st.selectbox("Select a Duration Range (Hours)", options=["Select the range", "< 2 hrs", "2 - 3 hrs", "> 3 hrs"])
        if dr != "Select the range":
            try:
                q = """ SELECT Title, Genre, Duration FROM Movies WHERE CASE 
                        WHEN :duration = '< 2 hrs' THEN Duration <= 2.0
                        WHEN :duration = '2 - 3 hrs' THEN Duration > 2.0 AND Duration <= 3.0
                        WHEN :duration = '> 3 hrs' THEN Duration > 3.0
                    END;"""
                f = pd.read_sql_query(q, conn, params={"duration": dr})
            except Exception as e:
                st.warning(f"Error -> query part {e}")
            with st.container():
                if not f.empty:
                    st.write(f"### Movie list with duration {dr}, Total Count: {f['Title'].count()}")
                    st.dataframe(f)
                elif f.empty:
                    st.write("# No Result Found")
                else:
                    st.warning("Something wrong Re-run the code")
        elif dr == "Select the range":
            pass
        else:
            st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")

    if conn:#filter movie by Rating
        st.subheader("2. Filtered Movies Based on Rating")
        r = st.select_slider("Select a minimum IMDb Rating", options=[round(x * 0.1, 1) for x in range(0, 101)], value=5.0)
        try:
            q = """SELECT Title, Genre, Rating FROM Movies WHERE Rating >= :min_rating;"""
            f = pd.read_sql_query(q, conn, params={"min_rating": r})
            st.write(f"### Movie list with Rating >= {r}, Total Movies: {f['Title'].count()}")
        except Exception as e:
                st.warning(f"Error -> query part {e}")    
        with st.container():
            if not f.empty:
                st.dataframe(f)
            elif f.empty:
                st.write("# No Result Found")
            else:
                st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")
    
    if conn:#filter movie by voting
        st.subheader("3. Filtered Movies based on voting")
        dr = st.selectbox("Select a Votes Range", options=["Select the range", "<= 1000", "1001 to 10,000", "> 10,000"])
        try:
            q = """SELECT Title, Genre, Votes FROM Movies WHERE 
                ( :votes_range = '<= 1000' AND Votes <= 1000 )
                OR ( :votes_range = '1001 to 10,000' AND Votes > 1000 AND Votes <= 10000 )
                OR ( :votes_range = '> 10,000' AND Votes > 10000 );"""
            f = pd.read_sql_query(q, conn, params={"votes_range": dr})
        except Exception as e:
                st.warning(f"Error -> query part {e}")
        with st.container():
            if not f.empty:
                st.write(f"### Movie list with Rating {dr}, Total Movies: {f['Title'].count()}")
                st.dataframe(f)
            elif dr != "Select a range":
                pass
            elif f.empty:
                st.write("# No Result Found")
            else:
                st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")

    if conn:#filter movie by gener
        st.subheader("4. Filter Movies by Genre")
        genres = ["Action", "Adventure", "Animation", "Comedy", "Crime"]
        s = st.radio("Select a Genre", options=genres, index=None)
        q = """SELECT Title, Genre, Rating, Votes, Duration FROM Movies WHERE Genre = :selected_genre;"""
        if s:
            try:
                f = pd.read_sql_query(q, conn, params={"selected_genre": s})
            except Exception as e:
                st.warning(f"Error -> query part {e}")
            if not f.empty:
                st.write(f"### Movie list with gener {s}, Total Movies: {f['Title'].count()}")
                st.dataframe(f)
            elif f.empty:
                st.write("# No Result Found")
            else:
                st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")

def multiFilter():
    if conn:
        st.title("Filtering Page")
        st.header("Select Filters")
        d_o = ["click here to select range", "< 2 hrs", "2 - 3 hrs", "> 3 hrs"]
        r_o = [round(x * 0.1, 1) for x in range(0, 101)]
        v_o = ["click here to select range", "<= 1000", "1001 to 10,000 hrs", "> 10,000 hrs"]
        g_o = ["Action", "Adventure", "Animation", "Comedy", "Crime"]
        d = st.selectbox("Select a Duration Range (Hours)", options=d_o)
        r = st.select_slider("Select a minimum IMDb Rating", options=r_o, value=5.0)
        v = st.selectbox("Select a Votes Range", options=v_o)
        g = st.radio("Select a Genre", options=g_o, index=None)
        if (d == d_o[0]) or (v == v_o[0]) or (g == None):
            pass
        else:
            try:
                q = """SELECT Title, Genre, Rating, Votes, Duration FROM Movies
                WHERE Genre = :selected_genre AND Rating >= :min_rating AND (
                    (:duration_range = '< 2 hrs' AND Duration <= 2.0) 
                    OR (:duration_range = '2 - 3 hrs' AND Duration > 2.0 AND Duration <= 3.0) 
                    OR (:duration_range = '> 3 hrs' AND Duration > 3.0))
                AND ((:votes_range = '<= 1000' AND Votes <= 1000)
                    OR (:votes_range = '1001 to 10,000 hrs' AND Votes > 1000 AND Votes <= 10000)
                    OR (:votes_range = '> 10,000 hrs' AND Votes > 10000));"""
                f = pd.read_sql_query(q, conn, params={"selected_genre": g,"min_rating": r,"duration_range": d,"votes_range": v})
            except Exception as e:
                st.warning(f"Error -> query part {e}")
            if not f.empty:
                st.write(f"Your contion:[Gener-{g}], [Rating-{r} : 10.0], [Duration - {d}], [Votes: {v}]")
                st.write(f"Total movie count: {f.shape[0]}")
                st.dataframe(f)
            elif f.empty:
                st.write("# No Result Found")
            else:
                st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")

st.sidebar.title("Page")
page = st.sidebar.radio("Go to", ["Data Visualizations", "Data Filter","Multi-level Data Filter"])
if page == "Data Visualizations":
    visualizations()
elif page == "Data Filter":
    filtering()
elif page == "Multi-level Data Filter":
    multiFilter()
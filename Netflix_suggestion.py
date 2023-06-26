import numpy as np
import pandas as pd


def cleaning_dataset():
    df_titles = pd.read_csv("titles.csv")
    df_credits = pd.read_csv("credits.csv")
    merged_df = pd.merge(df_titles, df_credits, on='id')

    merged_df['genres'] = merged_df['genres'].str.replace(r'[', '').str.replace(r"'", '').str.replace(r']', '')
    merged_df['genre'] = merged_df['genres'].str.split(',').str[0]

    merged_df['production_countries'] = merged_df['production_countries'].str.replace(r"[", '').str.replace(r"'",
                                                                                                            '').str.replace(
        r"]", '')
    merged_df['production_country'] = merged_df['production_countries'].str.split(',').str[0]
    merged_df.drop(['genres', 'production_countries'], axis=1, inplace=True)
    # print(merged_df.head())
    # print(merged_df['genre'].unique())

    merged_df['genre'] = merged_df['genre'].replace('', np.nan)
    merged_df['production_country'] = merged_df['production_country'].replace('', np.nan)

    merged_df['seasons'] = merged_df['seasons'].fillna('0')
    # print(merged_df.isna().sum())

    merged_df.drop(['id', 'imdb_id', 'age_certification'], axis=1, inplace=True)

    merged_df.dropna(inplace=True)
    # print(merged_df.isna().sum())
    clean_df = merged_df
    return clean_df


def separating_movies_tv_shows(clean_df):
    Movies = clean_df[clean_df['type'] == 'MOVIE']
    # print(Movies)
    TV_shows = clean_df[clean_df['type'] == 'SHOW']
    # print(TV_shows)
    return Movies, TV_shows


def US(Movies, TV_shows):
    Movies_US = Movies[Movies['production_country'] == 'US']
    TV_shows_US = TV_shows[TV_shows['production_country'] == 'US']
    return Movies_US, TV_shows_US


def US_action_movies(Movies_US):
    Movies_US_action = Movies_US[Movies_US['genre'] == 'action'].reset_index()
    return Movies_US_action


def main():
    clean = cleaning_dataset()
    print(clean['genre'].unique())
    Movies, TV_shows = separating_movies_tv_shows(clean_df=clean)
    Movies_US, TV_shows_US = US(Movies, TV_shows)
    Movies_US_action = US_action_movies(Movies_US)
    print(Movies_US_action)
    return clean


main()

import pandas as pd


# Convert each element of the imdb_id column in metadata to an int by applying a lambda function.
def remove_characters(string):
    return ''.join(filter(str.isdigit, string))

def getData(ctr):
    ratings_data = pd.read_csv('/Users/ilmunkoo/Desktop/archive/ratings_small.csv')
    metadata = pd.read_csv('/Users/ilmunkoo/Desktop/archive/movies_metadata.csv')
    links_data = pd.read_csv('/Users/ilmunkoo/Desktop/archive/links.csv')

    # Removed rows from the metadata data frame where the imdb_id was null.
    metadata = metadata[metadata['imdb_id'].notna()]
    metadata['imdb_id'] = metadata['imdb_id'].apply(lambda x: int(remove_characters(str(x))))

    # Merge metadata and links_data by joining the data frames on the imbd_id and imdbId columns respectively.
    full_metadata = pd.merge(metadata, links_data, left_on='imdb_id', right_on='imdbId')

    # Running the code above produces a single data frame that we can use to retrieve the metadata for a movie based on the movie ID alone.
    ctr = pd.DataFrame(ctr)
    ratings_data['rating'] = ctr
    ratings_data.rename(columns={'movieId': 'postId'}, inplace=True)


    # 사용자 기반 협업 필터링시 (사용자 기준)
    user_ratings = ratings_data.pivot_table('rating', index = 'userId', columns='postId')
    user_ratings.fillna(0, inplace =True)

    return user_ratings, ratings_data, full_metadata


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import warnings
warnings.simplefilter('ignore')

md = pd.read_csv('movies_metadata.csv', low_memory=False)
links_small = pd.read_csv('links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')
smd = md[md['id'].isin(links_small)]
smd = smd.drop(['homepage'], axis=1)
smd = smd.drop(['belongs_to_collection'], axis=1)
smd['description'] = smd['overview'] + smd['tagline']
smd = smd[smd['description'].notnull()]
smd = smd.sort_values('vote_average', ascending=False)
smd = smd.drop_duplicates(subset='title', keep='first')
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
smd = smd.reset_index()
indices = pd.Series(smd.index, index=smd['title'])


def improved_recommendations(title, count):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    weighted_rating = (vote_counts/(vote_counts+m) * vote_averages) + (m/(m+vote_counts) * C)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = weighted_rating
    qualified = qualified.sort_values('wr', ascending=False).head(count)
    return qualified['title'].tolist()


def get_titles_list():
    return smd['title'].to_dict()


def get_imdbid_by_baseid(baseid):
    links = pd.read_csv('links_small.csv')
    imdb_id = links[links['imdbId'].notnull()]['imdbId'].astype('int')[baseid]
    return convert_to_imdb_id(imdb_id)


def several_films(films_list):
    result = []
    for title in films_list:
        names = improved_recommendations(title,2)
        result.extend(names)
    return result


def convert_to_imdb_id(id):
    string_id = str(id)
    result = ''
    current_count = 7 - len(string_id)
    for i in range(0, current_count):
        result += '0'
    result = 'tt' + result
    return result + string_id

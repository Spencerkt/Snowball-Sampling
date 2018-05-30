import pandas as pd
import numpy as np

path = './data/sample_1/{}'

def write_movies(movie_path, movies):
    """
    Need to write files:
        isAction_obs
        isRomance_obs
        isCrime_obs
        isMusical_obs
        isSciFi_obs
        Year_obs
    """
    movie_df = pd.read_csv(movie_path, sep='\t', header=None)
    movie_df.columns = ['movie_id', 'title', 'genres']

    genres = ['action', 'romance', 'crime', 'musical', 'sci-fi']

    sampled_movies = movie_df.loc[movie_df.movie_id.isin(movies)]

    with open(path.format('isAction_obs.txt'), 'w') as isAction_obs, \
        open(path.format('isRomance_obs.txt'), 'w') as isRomance_obs, \
        open(path.format('isCrime_obs.txt'), 'w') as isCrime_obs, \
        open(path.format('isMusical_obs.txt'), 'w') as isMusical_obs, \
        open(path.format('isSciFi_obs.txt'), 'w') as isSciFi_obs, \
        open(path.format('Year_obs.txt'), 'w') as year_obs:
        for _, row in sampled_movies.iterrows():
            y = row.title.split(' ')[-1].replace('(', '').replace(')', '')
            year_obs.write('{}\t{}\t{}\n'.format(row.movie_id, y, 1.0))
            for g in row.genres.split('|'):
                if g.lower() == 'action':
                    isAction_obs.write('{}\t{}\n'.format(row.movie_id, 1.0))
                if g.lower() == 'romance':
                    isRomance_obs.write('{}\t{}\n'.format(row.movie_id, 1.0))
                if g.lower() == 'crime':
                    isCrime_obs.write('{}\t{}\n'.format(row.movie_id, 1.0))
                if g.lower() == 'musical':
                    isMusical_obs.write('{}\t{}\n'.format(row.movie_id, 1.0))
                if g.lower() == 'sci-fi':
                    isSciFi_obs.write('{}\t{}\n'.format(row.movie_id, 1.0))

    print 'Done writing movie files.'
    return


def write_users(user_path, users):
    """
    Need to write files:
        isYoung_obs
        isAdult_obs
        isElderly_obs
        isFemale_obs
    """
    user_df = pd.read_csv(user_path, sep='\t', header=None)
    user_df.columns = ['user_id', 'gender', 'age', 'occupation', 'zipcode']

    sampled_users = user_df.loc[user_df.user_id.isin(users)]

    with open(path.format('isYoung_obs.txt'), 'w') as isYoung_obs, \
        open(path.format('isAdult_obs.txt'), 'w') as isAdult_obs, \
        open(path.format('isElderly_obs.txt'), 'w') as isElderly_obs, \
        open(path.format('Gender_obs.txt'), 'w') as Gender_obs:
        for _, row in sampled_users.iterrows():
            Gender_obs.write('{}\t{}\t{}\n'.format(row.user_id, row.gender, 1.0))

            if row.age < 18:
                isYoung_obs.write('{}\t{}\n'.format(row.user_id, 1.0))
            if row.age >= 18 and row.age < 50:
                isAdult_obs.write('{}\t{}\n'.format(row.user_id, 1.0))
            if row.age >= 50:
                isElderly_obs.write('{}\t{}\n'.format(row.user_id, 1.0))

    print 'Done writing user files.'
    return


def write_ratings(rating_path, users, movies):
    """
    Need to write files:
        Rating_obs
        Rating_truth
        Rating_target
    """
    ratings_df = pd.read_csv(rating_path, sep='\t', header=None)
    ratings_df.columns = ['user_id', 'movie_id', 'rating', 'timestamp']

    sampled_ratings = ratings_df.loc[ratings_df.user_id.isin(users)]
    sampled_ratings = sampled_ratings.loc[sampled_ratings.movie_id.isin(movies)]

    # random 70/30 split
    obs_mask = np.random.rand(len(sampled_ratings)) < 0.7

    # mask df to get obs and truth/target
    rating_obs = sampled_ratings[obs_mask]
    rating_tt = sampled_ratings[~obs_mask]

    rating_obs['obs'] = 1.0
    rating_obs[['user_id', 'movie_id', 'obs']].to_csv(path.format('Rating_obs.txt'), sep='\t', index=False, header=None)

    rating_tt['obs'] = 1.0
    rating_tt[['user_id', 'movie_id', 'obs']].to_csv(path.format('Rating_truth.txt'), sep='\t', index=False, header=None)
    rating_tt[['user_id', 'movie_id']].to_csv(path.format('Rating_target.txt'), sep='\t', index=False, header=None)

    print 'Done writing rating files. '
    return


def write_user_sim(sim_path, users):
    """
    User_sim_obs
    """
    sim_df = pd.read_csv(sim_path, sep='\t', header=None)
    sim_df.columns = ['u1', 'u2', 'sim']

    sampled_sim = sim_df.loc[sim_df.u1.isin(users)]
    sampled_sim = sampled_sim.loc[sampled_sim.u2.isin(users)]

    sampled_sim.to_csv(path.format('User_sim_obs.txt'), sep='\t', index=False, header=None)
    print 'Done writing user similarities.'
    return


def write_movie_sim(sim_path, movies):
    """
    Movie_sim_obs
    """
    sim_df = pd.read_csv(sim_path, sep='\t', header=None)
    sim_df.columns = ['m1', 'm2', 'sim']

    sampled_sim = sim_df.loc[sim_df.m1.isin(movies)]
    sampled_sim = sampled_sim.loc[sampled_sim.m2.isin(movies)]

    sampled_sim.to_csv(path.format('Movie_sim_obs.txt'), sep='\t', index=False, header=None)
    print 'Done writing movie similarities.'
    return

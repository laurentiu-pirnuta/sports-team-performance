# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:21:43 2021

@author: Laurentiu
"""

# import libraries
import pandas as pd
import numpy as np
import scipy.stats as stats
import warnings
warnings.filterwarnings("ignore")

# read the data
mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

# get the nhl win/loss ratio
def nhl_win_loss_ratio():
    
    # make data frame global within the procedure
    global nhl_df
    
    # preparing the nhl dataframe
    
    # select only 2018 rows
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    
    # delete division rows and reset index
    bad_index = list(nhl_df['team'].str.extract("([\w ]* Division)").dropna().index)
    nhl_df = nhl_df.drop(bad_index).reset_index(drop = True)
    
    # cleaning the team column
    nhl_df['team'].replace('\*', '', inplace = True, regex = True)
    
    # creating the Win/Loss Ratio column
    nhl_df['Win/Loss Ratio'] = pd.to_numeric(nhl_df['W']) / (pd.to_numeric(nhl_df['W']) + pd.to_numeric(nhl_df['L']))
    
    # return the team and win//loss ratio dataframe
    return nhl_df[['team','Win/Loss Ratio']]

# get the nba win/loss ratio
def nba_win_loss_ratio():
    
    # make data frame global within the procedure
    global nba_df
    
    # preparing the nba dataframe
    
    # select only 2018 rows
    nba_df = nba_df[nba_df['year'] == 2018]
    
    # delete division rows and reset index
    bad_index = list(nba_df['team'].str.extract("([\w ]* Division)").dropna().index)
    nba_df = nba_df.drop(bad_index).reset_index(drop = True)
    
    # cleaning the team column
    nba_df['team'].replace({'\*': '', '[\s]\([\d]+\)': ''}, inplace = True, regex = True)
    
    # creating the Win/Loss Ratio column
    nba_df['Win/Loss Ratio'] = pd.to_numeric(nba_df['W']) / (pd.to_numeric(nba_df['W']) + pd.to_numeric(nba_df['L']))
    #nba_df['W/L%'] = pd.to_numeric(nba_df['W/L%'])
    
    # return the team and win//loss ratio dataframe
    return nba_df[['team', 'Win/Loss Ratio']]

# get the mlb win/loss ratio
def mlb_win_loss_ratio(): 
        
    # make data frame global within the procedure
    global mlb_df
    
    # preparing the mlb dataframe
    
    # select only 2018 rows
    mlb_df = mlb_df[mlb_df['year'] == 2018]
    
    # creating the Win/Loss Ratio column
    mlb_df['Win/Loss Ratio'] = pd.to_numeric(mlb_df['W']) / (pd.to_numeric(mlb_df['W']) + pd.to_numeric(mlb_df['L']))
    #mlb_df['W-L%'] = pd.to_numeric(mlb_df['W-L%'])
    
    # return the team and win//loss ratio dataframe
    return mlb_df[['team', 'Win/Loss Ratio']]
    
# get the nfl win/loss ratio
def nfl_win_loss_ratio(): 
    
    # make data frame global within the procedure
    global nfl_df
    
    # preparing the nfl dataframe
    
    # select only 2018 rows
    nfl_df = nfl_df[nfl_df['year'] == 2018]
    
    # delete division rows and reset index
    bad_index = list(nfl_df['team'].str.extract("(AFC|NFC [\w ]*)").dropna().index)
    nfl_df = nfl_df.drop(bad_index).reset_index(drop = True)
    
    # cleaning the team column
    nfl_df['team'].replace({'\*': '', '\+': ''}, inplace = True, regex = True)
    
    # creating the Win/Loss Ratio column
    nfl_df['Win/Loss Ratio'] = pd.to_numeric(nfl_df['W']) / (pd.to_numeric(nfl_df['W']) + pd.to_numeric(nfl_df['L']))
    #nfl_df['W-L%'] = pd.to_numeric(nfl_df['W-L%'])
    
    # return the team and win//loss ratio dataframe
    return nfl_df[['team', 'Win/Loss Ratio']]

# get teams for each city for each sport
def sport_cities_df():
    
    # make data frame global within the procedure
    global cities
    
    # rename the population column and convert it's values to numbers
    cities.rename(columns = {'Population (2016 est.)[8]': 'Population'}, inplace = True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    
    # eliminating notes from team names and replacing empty data with NaNs
    cities.replace('\[note \d{1,2}\]', '', inplace = True, regex = True)
    cities.replace({'': np.nan, '—': np.nan, '— ': np.nan}, inplace = True)
    
    # expland the rows with multiple teams
    cities['NHL'][0] = ['Rangers', 'Islanders', 'Devils']
    cities['NHL'][1] = ['Kings','Ducks']
    
    cities['NBA'][0] = ['Knicks', 'Nets']
    cities['NBA'][1] = ['Lakers','Clippers']
    
    cities['MLB'][0] = ['Yankees', 'Mets']
    cities['MLB'][1] = ['Dodgers','Angels']
    cities['MLB'][2] = ['Giants','Athletics']
    cities['MLB'][3] = ['Cubs','White Sox']
    
    cities['NFL'][0] = ['Giants', 'Jets']
    cities['NFL'][1] = ['Rams','Chargers']
    cities['NFL'][2] = ['49ers','Raiders']
    
    NHL_cities = cities[['Metropolitan area', 'NHL']].explode('NHL').dropna()
    NBA_cities = cities[['Metropolitan area', 'NBA']].explode('NBA').dropna()
    MLB_cities = cities[['Metropolitan area', 'MLB']].explode('MLB').dropna()
    NFL_cities = cities[['Metropolitan area', 'NFL']].explode('NFL').dropna()
    
    # create the teams column and do some extra filtering
    NHL_cities['team'] = NHL_cities['Metropolitan area'] + ' ' + NHL_cities['NHL']
    NHL_cities['team'].replace({'Area ': '', 'City ': ''}, inplace = True, regex = True)
    
    NBA_cities['team'] = NBA_cities['Metropolitan area'] + ' ' + NBA_cities['NBA']
    NBA_cities['team'].replace({'Area ': '', 'City ': ''}, inplace = True, regex = True)
    
    MLB_cities['team'] = MLB_cities['Metropolitan area'] + ' ' + MLB_cities['MLB']
    MLB_cities['team'].replace({'Area ': '', 'City ': ''}, inplace = True, regex = True)
    
    NFL_cities['team'] = NFL_cities['Metropolitan area'] + ' ' + NFL_cities['NFL']
    NFL_cities['team'].replace({'Area ': '', 'City ': ''}, inplace = True, regex = True)
    
    # replace the wrong team names for each sport based on the dictionary
    nhl_team_dict = {'Miami–Fort Lauderdale Panthers':'Florida Panthers', 
                 'Washington, D.C. Capitals':'Washington Capitals', 
                 'New York Devils':'New Jersey Devils',
                 'Raleigh Hurricanes':'Carolina Hurricanes',
                 'Minneapolis–Saint Paul Wild':'Minnesota Wild', 
                 'Denver Avalanche':'Colorado Avalanche', 
                 'Dallas–Fort Worth Stars':'Dallas Stars',
                 'Las Vegas Golden Knights':'Vegas Golden Knights', 
                 'Los Angeles Ducks':'Anaheim Ducks', 
                 'San Francisco Bay Sharks':'San Jose Sharks', 
                 'Phoenix Coyotes':'Arizona Coyotes'}
    
    nba_team_dict = {'Indianapolis Pacers':'Indiana Pacers', 
                    'Miami–Fort Lauderdale Heat':'Miami Heat', 
                    'Washington, D.C. Wizards':'Washington Wizards', 
                    'New York Nets':'Brooklyn Nets', 
                    'San Francisco Bay Warriors':'Golden State Warriors', 
                    'Oklahoma Thunder':'Oklahoma City Thunder', 
                    'Salt Lake Jazz':'Utah Jazz',
                    'Minneapolis–Saint Paul Timberwolves':'Minnesota Timberwolves',
                    'Dallas–Fort Worth Mavericks':'Dallas Mavericks'}
    
    mlb_team_dict = {'Minneapolis–Saint Paul Twins': 'Minnesota Twins',
                    'Kansas Royals': 'Kansas City Royals',
                    'San Francisco Bay Athletics': 'Oakland Athletics',
                    'Dallas–Fort Worth Rangers': 'Texas Rangers',
                    'Washington, D.C. Nationals': 'Washington Nationals',
                    'Miami–Fort Lauderdale Marlins': 'Miami Marlins',
                    'Denver Rockies': 'Colorado Rockies',
                    'Phoenix Diamondbacks': 'Arizona Diamondbacks',
                    'San Francisco Bay Giants': 'San Francisco Giants'}
    
    nfl_team_dict = {'Boston Patriots': 'New England Patriots',
                    'Miami–Fort Lauderdale Dolphins': 'Miami Dolphins',
                    'Nashville Titans': 'Tennessee Titans',
                    'Kansas Chiefs': 'Kansas City Chiefs',
                    'San Francisco Bay Raiders': 'Oakland Raiders',
                    'Dallas–Fort Worth Cowboys': 'Dallas Cowboys',
                    'Washington, D.C. Redskins': 'Washington Redskins',
                    'Minneapolis–Saint Paul Vikings': 'Minnesota Vikings',
                    'Charlotte Panthers': 'Carolina Panthers',
                    'San Francisco Bay 49ers': 'San Francisco 49ers',
                    'Phoenix Cardinals': 'Arizona Cardinals'}
    
    NHL_cities['team'].replace(nhl_team_dict, inplace = True)
    NBA_cities['team'].replace(nba_team_dict, inplace = True)
    MLB_cities['team'].replace(mlb_team_dict, inplace = True)
    NFL_cities['team'].replace(nfl_team_dict, inplace = True)
    
    # return the four resulting dataframes
    return (NHL_cities, NBA_cities, MLB_cities, NFL_cities)

# calculate the performance probability with hyphothesis testing
def sports_team_performance():
    
    # Get win/loss ratios
    nhl = nhl_win_loss_ratio()
    nba = nba_win_loss_ratio()
    mlb = mlb_win_loss_ratio()
    nfl = nfl_win_loss_ratio()
    
    # Get areas
    (nhl_cities, nba_cities, mlb_cities, nfl_cities) = sport_cities_df()
    
    # Merge data for each sport
    nhl = pd.merge(nhl, nhl_cities[['Metropolitan area', 'team']], how = 'left', on = 'team')
    nba = pd.merge(nba, nba_cities[['Metropolitan area', 'team']], how = 'left', on = 'team')
    mlb = pd.merge(mlb, mlb_cities[['Metropolitan area', 'team']], how = 'left', on = 'team')
    nfl = pd.merge(nfl, nfl_cities[['Metropolitan area', 'team']], how = 'left', on = 'team')
    
    # Group and aggregate data
    nhl_ratio = nhl.groupby('Metropolitan area').agg({'Win/Loss Ratio' : np.mean}).reset_index()
    nba_ratio = nba.groupby('Metropolitan area').agg({'Win/Loss Ratio' : np.mean}).reset_index()
    mlb_ratio = mlb.groupby('Metropolitan area').agg({'Win/Loss Ratio' : np.mean}).reset_index()
    nfl_ratio = nfl.groupby('Metropolitan area').agg({'Win/Loss Ratio' : np.mean}).reset_index()
    
    # Rename columns
    nhl_ratio.rename(columns = {'Win/Loss Ratio': 'NHL Win/Loss Ratio'}, inplace = True)
    nba_ratio.rename(columns = {'Win/Loss Ratio': 'NBA Win/Loss Ratio'}, inplace = True)
    mlb_ratio.rename(columns = {'Win/Loss Ratio': 'MLB Win/Loss Ratio'}, inplace = True)
    nfl_ratio.rename(columns = {'Win/Loss Ratio': 'NFL Win/Loss Ratio'}, inplace = True)
    
    # Merge pairs
    nhl_nba = pd.merge(nhl_ratio, nba_ratio, how = 'inner', on = 'Metropolitan area')
    nhl_mlb = pd.merge(nhl_ratio, mlb_ratio, how = 'inner', on = 'Metropolitan area')
    nhl_nfl = pd.merge(nhl_ratio, nfl_ratio, how = 'inner', on = 'Metropolitan area')
    nba_mlb = pd.merge(nba_ratio, mlb_ratio, how = 'inner', on = 'Metropolitan area')
    nba_nfl = pd.merge(nba_ratio, nfl_ratio, how = 'inner', on = 'Metropolitan area')
    mlb_nfl = pd.merge(mlb_ratio, nfl_ratio, how = 'inner', on = 'Metropolitan area')
    
    # Calculate the hypothesis testing p-values 
    _, nhl_nba_p_value = stats.ttest_rel(nhl_nba['NHL Win/Loss Ratio'], nhl_nba['NBA Win/Loss Ratio'])
    _, nhl_mlb_p_value = stats.ttest_rel(nhl_mlb['NHL Win/Loss Ratio'], nhl_mlb['MLB Win/Loss Ratio'])
    _, nhl_nfl_p_value = stats.ttest_rel(nhl_nfl['NHL Win/Loss Ratio'], nhl_nfl['NFL Win/Loss Ratio'])
    _, nba_mlb_p_value = stats.ttest_rel(nba_mlb['NBA Win/Loss Ratio'], nba_mlb['MLB Win/Loss Ratio'])
    _, nba_nfl_p_value = stats.ttest_rel(nba_nfl['NBA Win/Loss Ratio'], nba_nfl['NFL Win/Loss Ratio'])
    _, mlb_nfl_p_value = stats.ttest_rel(mlb_nfl['MLB Win/Loss Ratio'], mlb_nfl['NFL Win/Loss Ratio'])
    
    # Create the p-values dataframe
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index = sports)
    
    # Add values to the dataframe
    p_values.loc['NHL', 'NBA'] = p_values.loc['NBA', 'NHL'] = nhl_nba_p_value
    p_values.loc['NHL', 'MLB'] = p_values.loc['MLB', 'NHL'] = nhl_mlb_p_value
    p_values.loc['NHL', 'NFL'] = p_values.loc['NFL', 'NHL'] = nhl_nfl_p_value
    p_values.loc['NBA', 'MLB'] = p_values.loc['MLB', 'NBA'] = nba_mlb_p_value
    p_values.loc['NBA', 'NFL'] = p_values.loc['NFL', 'NBA'] = nba_nfl_p_value
    p_values.loc['MLB', 'NFL'] = p_values.loc['NFL', 'MLB'] = mlb_nfl_p_value
    
    # Return the p-values dataframe
    return p_values

print(sports_team_performance())

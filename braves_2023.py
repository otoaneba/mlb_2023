import statsapi
import json
import datetime as dt
import pandas as pd
import csv


# {"id": 144, "name": "Atlanta Braves", "teamCode": "atl", "fileCode": "atl", "teamName": "Braves", "locationName": "Atlanta", "shortName": "Atlanta"}

def get_date_list(start_date, end_date):
    """
    Return the list of dates in mm/dd/YYYY format. Used to call MLB team statistic for each date.
    
    Parameters
    ----------
    start_date : str
        start date of the list of dates to return
    end_date : str
        end date of the list of dates to return

    Returns
    -------
    list
        list of dates, in mm/dd/YYYY format, starting from start_date to end_date
    """
    date_list = pd.date_range(start=start_date, end=end_date)
    result_list = []
    for date in date_list:
        result_list.append(date.strftime('%m/%d/%Y'))
    return result_list

arr = get_date_list('3/31/2023', '10/01/2023')

def get_team_hitting_stats(season, date_arr):
    """
    Return a JSON of all MLB team hitting stats for the given season
    
    Parameters
    ----------
    season : int
        integer value of the season to extract the stat from
    date_arr : str[]
        array containing date in a mm/dd/YYYY string format for a single season (i.e., ['03/31/2023', '04/01/2023'])

    Returns
    -------
    list
        list of dicts with all hitting stats for the given season (in first parameter)
    """
 
    result_arr = []

    for date in date_arr:
        params = {'season': season, 'group': 'hitting', 'stats': 'byDateRange', 'startDate': date, 'endDate': date, 'teamId':144, 'sportIds':1}
        stat = statsapi.get('teams_stats', params)
        temp = {date: stat['stats'][0]['splits']}
        for team in stat['stats'][0]['splits']:
            if team['team']['name'] == 'Atlanta Braves':
                stat = team['stat']
                stat['date'] = date
                result_arr.append(stat)
    return result_arr

def main():
    # arr = get_date_list('3/30/2023', '10/01/2023')
    # team_data = get_team_hitting_stats(2023, arr)
    # with open('daily_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(team_data, f, ensure_ascii=False, indent=4)

    with open('daily_data.json', encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile).to_csv('daily_data.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    main()

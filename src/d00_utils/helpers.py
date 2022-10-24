# Author Johannes Allgaier

# imports
import pandas as pd
from datetime import date, datetime
import numpy as np


def drop_test_users(df_name: str, df: pd.DataFrame):
    """
    Drop testusers given a list of user_ids.
    
    :param df_name: name of dataframe in helpers excel, either 'uniti' or 'tyt'
    :param df: pandas dataframe object
    :return: dataframe with no testusers
    """

    if df_name == 'tyt':
        testusers = pd.read_excel('../../data/d00_helpers/testusers.xlsx', sheet_name=df_name)
        testusers = testusers.id.to_list()
        df = df[~df['user_id'].isin(testusers)]

    if df_name == 'uniti':
        testusers_pattern = '000'
        # TODO Check pattern of user ids to drop
        pass

    return df


def find_schedule_pattern(df, form='%Y-%m-%d %H:%M:%S', date_col_name='created_at'):
    """
    Takes a dataframe df and returns a dict that describes the duration of two filled out
    assessments of one user.
    :param df: dataframe that contains assessments of all users
           form: Format of the time stamp of the date column
           date_col_name: Name of the column containing the collection time stamp
    :return: dict like {hours: , days: , weeks: }
    """
    # find all users with more than two assessments
    s = df.user_id.value_counts() > 2
    user_ids = s[s == True].index

    hours_means, days_means = list(), list()

    for user_id in user_ids:
        sub_df = df[df['user_id'] == user_id]

        # for aggregation
        hours, days = list(), list()

        for i in np.arange(0, sub_df.shape[0] - 1):
            date_start = sub_df[date_col_name].iloc[i]
            date_start = datetime.strptime(date_start, form)
            date_end = sub_df[date_col_name].iloc[i + 1]
            date_end = datetime.strptime(date_end, form)

            delta = date_end - date_start

            hours.append(delta.total_seconds() / 3600)
            days.append(delta.total_seconds() / 3600 / 24)

        hours_means.append(np.array(hours).mean())
        days_means.append(np.array(days).mean())

    return {'avg hours between two assessments': np.array(hours_means).mean(),
            # average length between two filled out assessments in hours
            'avg days between two assessments': np.array(days_means).mean(),
            # average length between two filled out assessments in days
            'std_hours': np.array(hours_means).std(),  # std of length between two filled out assessments in hours
            'std_days': np.array(days_means).std()}  # std of length between two filled out assessments in days


def main():

    """
    # test find schedule pattern
    # read in a sample dataframe, uncomment to test
    df = pd.read_csv('../../data/d01_raw/ch/22-10-05_rki_stress_followup.csv')
    # df = pd.read_csv('../../data/d01_raw/ch/22-10-05_rki_parent_followup.csv')
    # df = pd.read_csv('../../data/d01_raw/ch/22-10-05_rki_heart_followup.csv')
    res = find_schedule_pattern(df, form='%Y-%m-%d %H:%M:%S', date_col_name='created_at')
    print(res)
    """

    ### Test drop testusers
    df = pd.read_csv('../../data/d01_raw/tyt/22-10-10_standardanswers.csv', index_col='Unnamed: 0')
    df = pd.read_csv('../../data/d01_raw/uniti/uniti_dataset_22.09.28.csv')
    drop_test_users('uniti', df)


if __name__ == '__main__':
    main()

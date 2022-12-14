# Author Johannes Allgaier

# imports
import pandas as pd
import sys


def drop_ambiguous_users(df):
    """
    Takes the whole df, filters one user and drops assessments from that user, if
    - the age varies from the most common age of the users
    - the gender varies from the most common gender of the users
    - the education varies from the most common education of the users
    - the user filled out the questionnaire for others
    :param df: corona check dataframe
    :param user_id: user id of that users
    :return: reduced dataframe
    """

    pd.set_option('mode.chained_assignment', None)

    user_ids = list(df.user_id.unique())

    for user_id in user_ids:

        sub_df = df[df['user_id'] == user_id]

        # filled out for him-/herself
        sub_df = sub_df[sub_df.author == 'MYSELF']
        all_assessments = sub_df.index

        if sub_df.shape[0] > 0:

            try:
                # most common age
                mca = sub_df.age.value_counts().index[0]
                f1 = (sub_df.age == mca)
                # most common education
                mce = sub_df.education.value_counts().index[0]
                f2 = (sub_df.education == mce)
                # most common gender
                mcg = sub_df.gender.value_counts().index[0]
                f3 = (sub_df.gender == mcg)
            except:  # some users skipped those baseline questions - we drop all assessments from those
                continue

            filtered_assessments = sub_df[f1 & f2 & f3].index
            assessments_to_drop = list(set(all_assessments) - set(filtered_assessments))

            df.drop(index=assessments_to_drop, inplace=True)

    return df


def drop_one_time_users(df):
    """
    Drops users with less than 2 assessments.
    :param df:
    :return: dataframe with users that have at lest two assessments.
    """

    pd.set_option('mode.chained_assignment', None)

    s = df.user_id.value_counts() > 1
    users = s[s == True].index

    return df[df['user_id'].isin(users)]


def drop_all_but_baseline_data(df):
    """
    Drops all but the first assessment for each user_id.
    Drops all columns but user_id, locale, created_at, updated_at, person, age, gender, education, research, operating_system, country_code.

    :param df: the dataframe to be processed
    :return: dataframe containing only one entry per user_id, with reduced columns
    """

    # first we drop the columns (this is faster when first dropping the rows)
    df = df[['user_id', 'locale', 'created_at', 'updated_at', 'person', 'age', 'gender', 'education', 'research',
             'operating_system', 'country_code']]

    # next we drop the rows so that only a single user_id remains
    # we do not have to assume, that the data is sorted by date, since the user-data should not change
    # (this is garanteed by first running drop_ambiguous_users on the dataframe)
    df = df.drop_duplicates(subset=['user_id'])

    return df


def main():
    sys.path.insert(0, "../..")

    df = pd.read_csv('../../data/d01_raw/cc/22-10-27_corona-check-data.csv')

    print('shape at start', df.shape)
    df = drop_one_time_users(df)

    print('shape without one-time-users', df.shape)
    df = drop_ambiguous_users(df)

    print('final shape with distinct users', df.shape)


if __name__ == '__main__':
    main()

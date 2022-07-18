import time
import pandas as pd
import json

# time measures are rounded to ROUND_DIGITS digits after comma
ROUND_DIGITS = 3


def show_interactive_df(df):
    show = input('\nDo you want to see the raw data? Type yes. [yes]\n').lower() in ['yes', '']
    cnt = 0
    BATCH_SIZE = 5
    while cnt*BATCH_SIZE < len(df) - BATCH_SIZE and show:
        print('\t'.join([str(x) for x in list(df.columns)][1:]))
        for i in range(BATCH_SIZE):
            print('\t'.join([str(x) for x in list(df.iloc[cnt*BATCH_SIZE + i,:])][1:]))
        show = input('\nDo you want to see next 5 rows of raw data? Type yes. [yes]\n').lower() in ['yes', '']
        cnt += 1

    # show remaining rows:
    if cnt*BATCH_SIZE < len(df) and show:
        print('\t'.join([str(x) for x in list(df.columns)][1:]))
        for i in range(len(df) - cnt*BATCH_SIZE):
            print('\t'.join([str(x) for x in list(df.iloc[cnt+i,:])][1:]))


def pretty_string_from_dict(dictionary):
    """
    creates a nice looking string from dictionary (dict)

    Returns:
        (str) ret_str - string derived from dictionary
    """
    ret_str = '\n'.join(json.dumps(dictionary, indent=4).split('\n')[1:-1])
    ret_str = ret_str.replace(',', '').replace(':', ' ->').replace('"', '')
    return ret_str


def string_taken_time(t_start):
    """
    creates printable string including the seconds till t_start.
    t_start is unix timestamp (float) or (int) eg 1648208106.4388824

    Returns:
        (str) ret_str - string containing the seconds till t_start
    """
    taken_time = round(time.time() - t_start, ROUND_DIGITS)
    # check if taken_time is below resolution due to chosen ROUND_DIGITS:
    time_resolution = 10**(-1 * ROUND_DIGITS)
    if taken_time < time_resolution / 2:
        ret_str = "\nThis took < %s seconds." % (time_resolution)
    else:
        ret_str = "\nThis took %s seconds." % (taken_time)
    return ret_str


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """
    get user input for city (chicago, new york city, washington).
    HINT: Use a while loop to handle invalid inputs
    """
    city_nr = ''
    city_map = {'1': 'Chicago', '2': 'New York', '3': 'Washington'}
    print('please sepcify a city:\n', pretty_string_from_dict(city_map))
    while city_nr not in city_map.keys():
        city_nr = input('make your choice: ')
    print('you chose: {}'.format(city_map[city_nr]))

    # get user input for month (all, january, february, ... , june)
    month_map = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr',
                 '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
                 '9': 'Sep', '10': 'Oct','11': 'Nov', '12': 'Dec',
                 'all': 'all'}
    print('please sepcify a month:\n', pretty_string_from_dict(month_map))
    month_nr = ''
    while month_nr not in month_map.keys():
        month_nr = input('make your choice: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_map = {'all': 'all', '1': 'Mon', '2': 'Tue', '3': 'Wed',
               '4': 'Thu', '5': 'Fri', '6': 'Sat', '0': 'Sun'}
    print('please sepcify a day:', pretty_string_from_dict(day_map))
    day_nr = ''
    while day_nr not in day_map.keys():
        day_nr = input('make your choice: ').lower()
    print('-' * 40)
    city = city_map[city_nr]
    month = month_nr
    day = day_nr
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('loading data into data frame...')
    file_map = {"Chicago": "chicago.csv",
                "New York": "new_york_city.csv",
                "Washington": "washington.csv"}

    file = file_map[city]

    df = pd.read_csv(file)
    print('data frame has in total {} rows'.format(len(df)))

    # convert Start Time col to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')

    # add month & dow col
    df['month'] = df['Start Time'].dt.month
    df['dow'] = df['Start Time'].dt.weekday

    # apply month filter if not all is given
    if month != 'all':
        df = df[df['month'] == int(month)]
        print('data frame has {} rows after applying month filter'.format(len(df)))
    # apply day filter if not all is given
    if day != 'all':
        df = df[df['dow'] == int(day)]
        print('data frame has {} rows after applying day filter'.format(len(df)))
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].dropna().mode()[0]
    print('most common month is {}'.format(most_common_month))

    # display the most common day of week
    most_common_dow = df['dow'].dropna().mode()[0]
    print('most common day is {}'.format(most_common_dow))

    # display the most common start hour
    most_common_starthour = df['Start Time'].dropna().dt.hour.mode()[0]
    print('most common start hour is {}'.format(most_common_starthour))

    print(string_taken_time(start_time))

    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station is "{}"'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('most commonly used end station is "{}"'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['start end combination'] = df['Start Station'] + '-2-' + df['End Station']
    most_common_combi = df['start end combination'].mode()[0]
    print('most frequent combination from ' \
          '"{}" to "{}"'.format(most_common_combi.split('-2-')[0],
                                most_common_combi.split('-2-')[1]))

    print(string_taken_time(start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = sum(df['Trip Duration']) # assumption: [sec]

    print('total travel time is {} sec -> {} h ' \
          '-> {} d -> {} a'.format(round(tot_travel_time, 1),
                                   round(tot_travel_time/60/60, 1),
                                   round(tot_travel_time/60/60/24, 1),
                                   round(tot_travel_time/60/60/24/365, 3)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('average travel time is {} min'.format(round(mean_travel_time/60, 2)))

    print(string_taken_time(start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    except KeyError as exc:
        print('got exception related to access column {} of data frame'.format(exc))
    try:
        # Display earliest1, most recent, and most common year of birth
        earliest_yob = int(min(df['Birth Year'].dropna()))
        print('earliest year of birth is {}'.format(earliest_yob))
        latest_yob = int(max(df['Birth Year'].dropna()))
        print('latest year of birth is {}'.format(latest_yob))
        most_common_yob = int(df['Birth Year'].dropna().mode()[0])
        print('most common year of birth is {}'.format(most_common_yob))
    except KeyError as exc:
        print('got exception related to access column {} of data frame'.format(exc))

    print(string_taken_time(start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if len(df) > 0:
            show_interactive_df(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print('your combination has no data. Please try another one.')

        # ask for restart with yes as default
        restart = input('\nWould you like to restart? Enter yes or no. [yes]\n') or 'yes'
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

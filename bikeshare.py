import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities =  list(CITY_DATA.keys())
    message_city = '\nWould you like to see the data of:\n[1]Chicago\n[2]New York City\n[3]Washington\nInput the number of of city (1-3) and press Enter:\n'
    while True:
        try:
            city_idx = int(input(message_city))
        except ValueError:
            print('Invalid input, enter number (1-3)')
            continue

        if city_idx not in [1,2,3]:
            print('Invalid number, input number in (1-3)')
            continue
        else:
            break
    city = cities[city_idx-1]
    print('The city you have choosed is {}\n'.format(city.title()))

    # get user input for the filter's option.
    message_filter = '\nWould you like to apply filers? Enter the the number of following options:\n[1]By Month\n[2]By Day of Week\n[3]By Both\n[4]No Filters\n'
    while True:
        try:
            filter_idx = int(input(message_filter))
        except ValueError:
            print('Invalid input, enter a number (1-4)')
            continue
        if filter_idx not in [1,2,3,4]:
            print('Invalid option, input a number in (1-4)')
            continue
        else:
            break
    month = 'all'
    day = 'all'

    # get user input for month (all, january, february, ... , june)
    if filter_idx == 1 or filter_idx == 3:
        months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        message_month = '\nInput the digital of month from January to June (1-6),input 0 for all months:\n'
        while True:
            try:
                month_idx = int(input(message_month))
            except ValueError:
                print('Invalid option, enter number (0-6)')
                continue
            if month_idx not in range(7):
                print('Your input \'{}\' is invalid, try again\n'.format(month_idx))
                continue
            else:
                break
        month = months[month_idx-1]
        print('The montn you have choosed is {}\n'.format(month.title()))
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_idx == 2 or filter_idx == 3:
        weekdays = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
        message_day = '\nInput the day of week (all, monday, tuesday, ... sunday)\n'
        while True:
            try:
                day = input(message_day)
            except ValueError:
                print('Your input {} is invalid, try again\n'.format(day))
                continue
            except KeyboardInterrupt:
                break
            if day.lower() not in weekdays:
                print('Your input {} is invalid, try again\n'.format(day))
                continue
            else:
                print('The day you have choosed is {}\n'.format(day.title()))
                break
    print('-'*40)
    return city, month, day.lower()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = df.groupby(['month'])['month'].count().max()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Popular Month: {}\nCounts: {}\n'.format(months[popular_month-1].title(),popular_month_count))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    popular_dow_count = df.groupby(['day_of_week'])['day_of_week'].count().max()
    print('Popular Day of Week: {}\nCounts: {}\n'.format(popular_dow,popular_dow_count))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df.groupby(['hour'])['hour'].count().max()
    print('Popular start hour: {}\nCounts: {}\n'.format(popular_hour,popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df.groupby(['Start Station'])['Start Station'].count().max()
    print('Popular Start Station: {}\nCounts: {}\n'.format(popular_start_station,popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df.groupby(['End Station'])['End Station'].count().max()
    print('Popular End Station: {}\n Counts: {}\n'.format(popular_end_station,popular_end_station_count))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station']+ ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    popular_trip_count = df.groupby(['Trip'])['Trip'].count().max()
    print('Popular trip is from {}\nCounts: {}\n'.format(popular_trip,popular_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time: {}\n'.format(df['Trip Duration'].sum()))
    # display mean travel time
    print('The average travel time: {}\n'.format(df['Trip Duration'].mean()))
    # display longest travel time
    print('The longest travel time: {}\n'.format(df['Trip Duration'].max()))
    #display shortest travel time
    print('The shortet travel time: {}\n'.format(df['Trip Duration'].min()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCount of User Type:\n')
    user_types = dict(df['User Type'].value_counts())
    type_list = list(user_types.keys())
    for utype in type_list:
        print('{} : {} '.format(utype, user_types[utype]))

    # Display counts of gender
    print('\nCount of Gender:\n')
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('Male: {}\nFemale: {}\n'.format(genders[0],genders[1]))
    else:
        print('*** Gender is not available for selected datasets ***')

    # Display earliest, most recent, and most common year of birth
    print('\nStatistics of year of birth:\n')
    if 'Birth Year' in df.columns:
        print('Earliest: {}'.format(df['Birth Year'].min()))
        print('Most Recent: {}'.format(df['Birth Year'].max()))
        print('most Common: {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('*** Birth Year is not available for selected datasets ***')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #display next 5 lines of raw data

        for i in range(0,len(df),5):
            try:
                view_raw_data = input('\nWould you like to view 5 lines of raw data? Enter yes or no.\n')
            except KeyboardInterrupt:
                break
            if view_raw_data.lower() not in ['yes','no']:
                print('Input is not valid')
                continue
            elif view_raw_data.lower() == 'yes':
                print(df.iloc[i:i+5])
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes','no']:
            print('Input is not valid, quit running.')
            break
        elif restart.lower() != 'yes':
            break
        else:
            continue

if __name__ == "__main__":
	main()

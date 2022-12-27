import time
import pandas as pd
import numpy as np

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
    i=0
    city_list=['chicago','new york city','washington']
    month_list = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december','all']
    day_list = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

    while i==0:
        city=input('Which city would you like to explore Chicago, New York City, Washington?\n')
        if(city.lower() in city_list):
            i=1
        else:
            print('Enter a correct city name - Chicago, New York City or Washington')
            i=0

    # get user input for month (all, january, february, ... , june)
    i=0
    while i==0:
        month=input('Enter month name would you like to filter by, type all to apply no month filter?\n')
        if(month.lower() in month_list):
            i=1
        else:
            print('Enter a correct month name - all, january, february, ... , june')
            i=0    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    i=0
    while i==0:
        day=input('Which day would you like to filter by, type all to apply no day filter?\n')
        if(day.lower() in day_list):
            i=1
        else:
            print('Enter a correct wekday name - all, monday, tuesday, ... sunday')
            i=0  

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    city=city.lower()
    month=month.lower()
    day=day.lower()        
    # load data file into a dataframe
    filename=CITY_DATA[city]
    df=pd.read_csv(filename)
    #print(df.head())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d')

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    #print(df.head())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
        month = months.index(month) + 1
        #print("month " + str(month))
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #print(df.head())

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower() == day]
        #print("day " + day)
    
    return df
    
#df = load_data('chiCago', 'mARch', 'Friday')
#print(df.head())



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common travel month is ' + str(popular_month))


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common travel day is ' + popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour month is ' + str(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is ' + popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is ' + popular_end_station)


    # display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start station and end station trip is ' + str(popular_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Time Diff'] = (df['End Time'] - df['Start Time']).dt.total_seconds()

    # display total travel time
    print('Total travel time is '+ str(df['Time Diff'].sum()))

    # display mean travel time
    print('Total mean time is '+ str(df['Time Diff'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types')
    print(user_types)
    print('\n')

    # Display counts of gender
    gender_counts = df['Gender'].value_counts()
    print('Count of gender types')
    print(gender_counts)
    print('\n')

    # Display earliest, most recent, and most common year of birth
    birth_year = dict(df['Birth Year'].value_counts())
    minyear=min(birth_year, key=birth_year.get)
    maxyear=max(birth_year, key=birth_year.get)
    commonyear = df['Birth Year'].mode()[0]
    print('Earliest year of birth is ' + str(int(minyear)))
    print('Most recent year of birth is ' + str(int(maxyear)))
    print('Most common year of birth is ' + str(int(commonyear)))

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
import datetime as dt
import operator
import calendar

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
        (str) no filter - returns raw data frame
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city=input('For Which city do you want to see the bikeshare data?\n').lower()
    while city not in CITY_DATA:
        print("Sorry! we still have not got any data for {}. Please select from chicago or new york city or washington".format(city))
        city=''
        city=input('For Which city do you want to see the bikeshare data? \n').lower()

    # take the filter option in global parameter asnwer
    global answer
    answers =['monthname','both','nofilter','day']
    answer=input("Enter your filter condtion which can be on the basis of day or monthname or both or nofilter at all, if you want to see raw data\n").lower()
    while answer not in answers:
        print("Filter you have entered is out of scope! please enter from day or monthname or both or nofilter")
        answer=''
        answer=input("Enter your filter condtion which can be on the basis of day or monthname or both or nofilter at all, if you want to see raw data\n").lower()

    # get user input for month (all, january, february, ... , june) if user wants to filter by monthname
    if answer == "monthname":
        day=''
        month=input('Enter the abbreviated month name\n').lower()
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        while month not in months:
            month=''
            print("We do not have data for the entered month.Please enter a different month")
            month=input('Enter the abbreviated month name \n').lower()
        print('-'*100)
        return city, month, day,answer

    # get user input for month (all, january, february, ... , june) and day of the week, if user wants to filter by both monthname and day of the week
    elif answer == "both":
        month=input('Enter the abbreviated month name \n').lower()
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

        while month not in months:
            month=''
            print("We do not have data for the entered month.Please enter a different month")
            month=input('Enter the abbreviated month name \n').lower()


        days=[x for x in range(0,32)]
        while True:
            try:
                day=input('Enter the day number i.e if you want sunday then enter 0 \n')
                day=int(day)
                if day not in days:
                    print("Day you enetered is not a valid day number")
                    continue
                else:
                    break
            except ValueError:
                print("Not a valid integer! Please try again" )
            except NameError:
                print("Nameerror! Please try again" )

        print('-'*100)
        return city, month, day,answer

     # get user input for day of the week if user wants to filter by day of the week
    elif answer == "day":
        month=''
        days=[x for x in range(0,32)]
        while True:
            try:
                day=input('Enter the day number i.e if you want sunday then enter 0 \n')
                day=int(day)
                if day not in days:
                    print("Day you enetered is not a valid day number")
                    continue
                else:
                    break
            except ValueError:
                print("Not a valid integer! Please try again" )
            except NameError:
                print("Nameerror! Please try again" )

        print('-'*100)
        return city, month, day,answer
    # no filter taken
    elif answer == "nofilter":
        day=''
        month=''
        print('-'*100)
        return city, month, day,answer


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

    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] =df['Start Time'].dt.month
    df['day_of_week'] =df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['strt_st||end_dt']="Start Station: "+df['Start Station']+" AND "+" End Station: "+df['End Station']


    #df=df[operator.and_(df.month==month, df.day_of_week==day)]
    if answer == "monthname":
        month_conv = dt.datetime.strptime(month, "%b")
        month=month_conv.month
        df=df[df.month==month]
        return df
    elif answer == "day":
        df=df[df.day_of_week==day]
        return df
    elif answer == "both":
        month_conv = dt.datetime.strptime(month, "%b")
        month=month_conv.month
        df=df[operator.and_(df.month==month, df.day_of_week==day)]
        return df
    elif answer =="nofilter":
        return df


def time_stats(df):
    #Displays statistics on the most frequent times of travel.
    df.size

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    if answer == "monthname":
        # display the most common month
        frq_month=df['month'].value_counts().idxmax()
        frq_month_count=df['month'].value_counts().max()
        # display the most common start hour
        frq_hr=df['hour'].value_counts().idxmax()
        frq_hr_count=df['hour'].value_counts().max()
        print('*'*10,"Popular times of travel",'*'*10)
        print("Frequent Month: {} Count: {}".format(calendar.month_name[frq_month],frq_month_count))
        print("Frequent hour: {} Count: {}".format(frq_hr,frq_hr_count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*100)


    elif answer == "day":
        # display the most common day of week
        frq_dof=df['day_of_week'].value_counts().idxmax()
        frq_dof_count=df['day_of_week'].value_counts().max()

        # display the most common start hour
        frq_hr=df['hour'].value_counts().idxmax()
        frq_hr_count=df['hour'].value_counts().max()

        print('*'*10,"Popular times of travel",'*'*10)
        print("Frequent Day Of Week: {} Count: {}".format(calendar.day_name[frq_dof],frq_dof_count))
        print("Frequent hour: {} Count: {}".format(frq_hr,frq_hr_count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*100)


    elif answer == "both":
        # display the most common month
        frq_month=df['month'].value_counts().idxmax()
        frq_month_count=df['month'].value_counts().max()

        # display the most common day of week
        frq_dof=df['day_of_week'].value_counts().idxmax()
        frq_dof_count=df['day_of_week'].value_counts().max()

        # display the most common start hour
        frq_hr=df['hour'].value_counts().idxmax()
        frq_hr_count=df['hour'].value_counts().max()

        print('*'*10,"Popular times of travel",'*'*10)
        print("Frequent Month: {} Count: {}".format(calendar.month_name[frq_month],frq_month_count))
        print("Frequent Day Of Week: {} Count: {}".format(calendar.day_name[frq_dof],frq_dof_count))
        print("Frequent hour: {} Count: {}".format(frq_hr,frq_hr_count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*100)


    elif answer =="nofilter":
        # display the most common month
        frq_month=df['month'].value_counts().idxmax()
        frq_month_count=df['month'].value_counts().max()

        # display the most common day of week
        frq_dof=df['day_of_week'].value_counts().idxmax()
        frq_dof_count=df['day_of_week'].value_counts().max()

        # display the most common start hour
        frq_hr=df['hour'].value_counts().idxmax()
        frq_hr_count=df['hour'].value_counts().max()

        print('*'*10,"Popular times of travel",'*'*10)
        print("Frequent Month: {} Count: {}".format(calendar.month_name[frq_month],frq_month_count))
        print("Frequent Day Of Week: {} Count: {}".format(calendar.day_name[frq_dof],frq_dof_count))
        print("Frequent hour: {} Count: {}".format(frq_hr,frq_hr_count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*100)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frqSs=df['Start Station'].value_counts().idxmax()
    frq_ss_count=df['Start Station'].value_counts().max()

    # display most commonly used end station
    frq_es=df['End Station'].value_counts().idxmax()
    frq_es_count=df['End Station'].value_counts().max()

    # display most frequent combination of start station and end station trip
    frq_sscates=df['strt_st||end_dt'].value_counts().idxmax()
    frqSSCatES_count=df['strt_st||end_dt'].value_counts().max()


    print('*'*10,"Popular stations and trip",'*'*10)
    print("Frequent start station: {} Count: {}".format(frqSs,frq_ss_count))
    print("Frequent end station: {} Count: {}".format(frq_es,frq_es_count))
    print("Frequent combination of start station and end station trip: {} Count:{}".format(frq_sscates,frqSSCatES_count)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_timedur=df['Trip Duration'].sum()

    # display mean travel time
    AVG_timedur=df['Trip Duration'].mean()

    print('*'*10,"Trip duration",'*'*10)
    print("Total Travel Time: {}".format(tot_timedur))
    print("Average Travel Time: {}".format(AVG_timedur))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types=df['User Type'].value_counts().idxmax()
    user_count=df['User Type'].value_counts().max()

    # Display counts of gender
    gender_type=df['Gender'].value_counts().idxmax()
    gender_count=df['Gender'].value_counts().max()

    # Display earliest, most recent, and most common year of birth
    earliest_yob=int(df['Birth Year'].min())

    most_recent_yop=int(df['Birth Year'].max())

    most_common_yob= int(df['Birth Year'].value_counts().idxmax())
    most_common_yob_count=df['Birth Year'].value_counts().max()

    print('*'*10,"User info",'*'*10)
    print("Earliest year of birth: {}".format(earliest_yob))
    print("Most recent year of birth: {}".format(most_recent_yop))
    print("Most_common year of birth: {} Count:{}".format(most_common_yob,most_common_yob_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def export_to_csv(df):
    export=input("Do you want to create a csv file?").lower()
    if export == 'yes' or export =='y':
        df.to_csv('out.csv')
        print("Dataframe export success in your directory!")

def display_data(df):
    indx=5
    while True:
        response=input("Do you wish to view data?\n")
        if response == 'yes' or response == 'y':
            print(df.iloc[0:indx, 1:9])
            indx+=5
        elif response == 'no' or response == 'n' :
            break


def main():
    while True:
        city, month, day,answer = get_filters()
        df = load_data(city, month, day)
        if df.size == 0:
            print("No data found for the selection. Lets try again!")
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city =='chicago' or city =='new york city':
            user_stats(df)

        display_data(df)
        export_to_csv(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['y','yes']:
            break


if __name__ == "__main__":
	main()

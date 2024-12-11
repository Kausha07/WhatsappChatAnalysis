import re
import pandas as pd

def preprocess(data):
    # Updated pattern to capture date and time with AM/PM
    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[apAP][mM]\s-\s'

    messages = re.split(pattern, data)[1:]  # Skip the first element as it's empty
    dates = re.findall(pattern, data)

    # Debugging output
    print(f"Total messages found: {len(messages)}")
    print(f"Total dates found: {len(dates)}")
    print(f"Messages: {messages[:5]}")  # Print the first 5 messages for debugging
    print(f"Dates: {dates[:5]}")        # Print the first 5 dates for debugging

    # Create DataFrame from messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message content
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', message)
        if len(entry) > 1:  # User name exists
            users.append(entry[1].strip())
            messages.append(" ".join(entry[2:]).strip())
        else:
            users.append('group_notification')  # Default for group messages
            messages.append(entry[0].strip())

    # Add user and message columns to DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create period column
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x + 1) % 24:02d}")

    # Debugging output
    print(df.head())  # Show the first few rows of the DataFrame

    return df

# Example usage
# Assuming `data` contains your chat messages
# df = preprocess(data)

import os
import json
import mysql.connector as mysql
from git import Repo

def get_db_connection():
    return mysql.connect(host="localhost", user="root", password="Viyan@30", database="youtube", port="3306")


def create_tables(cursor):
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS aggregate_transaction (
                quarter INT,
                amount BIGINT,
                count BIGINT,
                transactionname TEXT,
                year text,
                state text
            )""")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS aggregate_user (
                quarter INT,
                count BIGINT,
                brand TEXT,
                year text,
                state text
            )""")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS map_transaction (
                    quarter INT,
                    count BIGINT,
                    amount BIGINT,
                    district TEXT,
                    year text,
                    state text
                )""")

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS map_user (
                        quarter INT,
                        registered_user INT,
                        district TEXT,
                        year text,
                        state text
                    )""")

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS top_transactions (
                        quarter INT,
                        count INT,
                        amount BIGINT,
                        district TEXT,
                        year text,
                        state text
                    )""")

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS top_users (
                        quarter INT,
                        registeredusers INT,
                        district TEXT,
                        year text,
                        state text
                    )""")


def transaction_aggregate(path):
    for state in os.listdir(path):
        state_name = state.replace("-"," ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from aggregate_transaction where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for data in df2['data']['transactionData']:
                            for rec in data['paymentInstruments']:
                                if count == 0:
                                    cursor.execute(
                                        "insert into aggregate_transaction(state,year,quarter,transactionname,amount,count)values(%s,%s,%s,%s,%s,%s)",
                                        (state_name, year, quarter_divi, data['name'], rec['amount'], rec['count']))
                                else:
                                    cursor.execute(
                                        "update aggregate_transaction set state = %s, year = %s, quarter = %s, transactionname = %s, amount = %s, count = %s",
                                        (state_name, year, quarter_divi, data['name'], rec['amount'], rec['count']))
                                conn.commit()
                    except Exception as e:
                        pass


def user_aggregate(path):
    for state in os.listdir(path):
        state_name = state.replace("-", " ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from aggregate_user where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for data in df2['data']['usersByDevice']:
                            if count == 0:
                                cursor.execute(
                                    "insert into aggregate_user(state,year,quarter,brand,count)values(%s,%s,%s,%s,%s)",
                                    (state_name, year, quarter_divi, data['brand'], data['count']))
                            else:
                                cursor.execute(
                                    "update aggregate_user set state = %s, year = %s, quarter = %s, brand = %s, count = %s",
                                    (state_name, year, quarter_divi, data['brand'], data['count']))
                            conn.commit()
                    except Exception as e:
                        pass


def map_transaction(path):
    for state in os.listdir(path):
        state_name = state.replace("-", " ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from map_transaction where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for data in df2['data']['hoverDataList']:
                            for rec in data['metric']:
                                if count == 0:
                                    cursor.execute(
                                        "insert into map_transaction(state,year,quarter,amount,count,district)values(%s,%s,%s,%s,%s,%s)",
                                        (state_name, year, quarter_divi, rec['amount'], rec['count'], data['name']))
                                else:
                                    cursor.execute(
                                        "update map_transaction set state = %s, year = %s, quarter = %s, count = %s, amount = %s, district = %s",
                                        (state_name, year, quarter_divi, rec['amount'], rec['count'], data['name']))
                                conn.commit()
                    except Exception as e:
                        pass


def map_users(path):
    for state in os.listdir(path):
        state_name = state.replace("-", " ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from map_user where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for record in df2['data']['hoverData'].items():
                            district = record[0].replace('district', '')
                            usercount = record[1]['registeredUsers']
                            if count == 0:
                                cursor.execute(
                                    "insert into map_user(state,year,quarter,registered_user,district)values(%s,%s,%s,%s,%s)",
                                    (state_name, year, quarter_divi, usercount, district))
                            else:
                                cursor.execute(
                                    "update map_user set state = %s, year = %s, quarter = %s, registered_user = %s, district = %s",
                                    (state_name, year, quarter_divi, usercount, district))
                            conn.commit()
                    except Exception as e:
                        pass


def top_transaction(path):
    for state in os.listdir(path):
        state_name = state.replace("-", " ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from top_transactions where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for record in df2['data']['districts']:
                            if count == 0:
                                cursor.execute(
                                    "insert into top_transactions(state,year,quarter,amount,count,district)values(%s,%s,%s,%s,%s,%s)",
                                    (state_name, year, quarter_divi, record['metric']['amount'], record['metric']['count'],
                                     record['entityName']))
                            else:
                                cursor.execute(
                                    "update top_transactions set state = %s, year = %s, quarter = %s, amount = %s, count=%s, district = %s",
                                    (state_name, year, quarter_divi, record['metric']['amount'], record['metric']['count'],
                                     record['entityName']))
                            conn.commit()
                    except Exception as e:
                        pass


def top_users(path):
    for state in os.listdir(path):
        state_name = state.replace("-", " ").title()
        state_path = os.path.join(path + '/' + state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path + '/' + year)
            for quarter in os.listdir(year_path):
                file_path = os.path.join(year_path + '/' + quarter)
                df = open(file_path, "r")
                df2 = json.load(df)
                quarter_divi = quarter.replace('.json', '')
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "select count(*) from top_users where state = %s and year = %s and quarter = %s",
                        (state_name, year, quarter_divi))
                    count = cursor.fetchone()[0]
                    try:
                        for record in df2['data']['districts']:
                            if count == 0:
                                cursor.execute(
                                    "insert into top_users(state,year,quarter,registeredusers,district)values(%s,%s,%s,%s,%s)",
                                    (state_name, year, quarter_divi, record['registeredUsers'], record['name']))
                            else:
                                cursor.execute(
                                    "update top_users set state = %s, year = %s, quarter = %s, registeredusers = %s, district = %s",
                                    (state_name, year, quarter_divi, record['registeredUsers'], record['name']))
                            conn.commit()
                    except Exception as e:
                        pass


def fetch_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        cursor.close()
        conn.commit()
    path = r'C:\Users\Admin\Videos\pulse_repo\data\aggregated\transaction\country\india\state'
    path1 = r'C:\Users\Admin\Videos\pulse_repo\data\aggregated\user\country\india\state'
    path2 = r'C:\Users\Admin\Videos\pulse_repo\data\map\transaction\hover\country\india\state'
    path3 = r'C:\Users\Admin\Videos\pulse_repo\data\map\user\hover\country\india\state'
    path4 = r'C:\Users\Admin\Videos\pulse_repo\data\top\transaction\country\india\state'
    path5 = r'C:\Users\Admin\Videos\pulse_repo\data\top\user\country\india\state'
    transaction_aggregate(path)
    user_aggregate(path1)
    map_transaction(path2)
    map_users(path3)
    top_transaction(path4)
    top_users(path5)


def main():
    target_directory = r"C:\Users\Admin\Videos\pulse_repo"

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    Repo.clone_from("https://github.com/PhonePe/pulse.git", target_directory)

    fetch_data()


if __name__ == "__main__":
    main()


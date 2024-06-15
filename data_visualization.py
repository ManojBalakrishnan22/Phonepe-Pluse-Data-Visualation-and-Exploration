import mysql.connector as mysql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd



def get_db_connection():
    return mysql.connect(host="localhost", user="root", password="Viyan@30", database="youtube", port="3306")


def main():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select distinct state from aggregate_transaction order by state")
        state_list = cursor.fetchall()
        state_values = [rec.replace("-"," ") for record in state_list for rec in record ]
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")
        
        with st.sidebar:
            selected = option_menu("NAVIGATION", ['Home','Explore Data','Top Charts'],
                icons=['house-fill', 'search', 'bar-chart-line-fill'], menu_icon="cast", default_index=1)
     
        if selected == 'Home':
            st.header("Phonepe Pluse Data Visualization and Exploration")
            st.write("In Current Generation, the online **Money Transfer** is used in our day-to-day Life.")
            st.write("This project explain the Phonepe payment activities in India. Here, we can explore the phoenpe data's by transaction and user. We can also explore by the "
                     "by year,quarter,state and district wise")
            
        elif selected == 'Explore Data':
            options = st.selectbox("Select the Option ",("Users", "Transactions"))
            if options == 'Users':
                year = st.selectbox("Year",("2018","2019","2020","2021","2022","2023","2024"),placeholder="Year-Wise")
                quarter = st.selectbox("Quarter",("1","2","3","4"))
                try:
                    cursor.execute("select state,sum(registered_user) from map_user where year=%s and quarter=%s group by state order by state",(year,quarter))
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Registered_Users'])
                    df2 = pd.read_csv(r'C:\Users\Admin\PycharmProjects\pythonProject\TEST\Statenames (1).csv')
                    df1.State = df2
                    df1['Registered_Users'] = pd.to_numeric(df1['Registered_Users'], errors='coerce')

                    fig = px.choropleth(
                        df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Registered_Users',
                        color_continuous_scale="emrld",#rdpu,blues,tealgrn,emrld,purp
                        range_color=(df1['Registered_Users'].min(), df1['Registered_Users'].max())
                    )
                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig, use_container_width=True)

                    state = st.selectbox("State",state_values,placeholder="State-Wise")
                    cursor.execute("select district,registered_user from map_user where year=%s and quarter=%s and state=%s order by district",(year,quarter,state))
                    df1 = pd.DataFrame(cursor.fetchall(),columns= ['District', 'Registered_Users'])
                    df1.Registered_Users = df1.Registered_Users.astype(float)
                    fig = px.bar(df1,
                                 title='District Wise Registered Users',
                                 x="District",
                                 y="Registered_Users",
                                 orientation='v',
                                 color='District',
                                 color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True)

                except Exception as e:
                    print(e)
                    pass
            
            elif options == 'Transactions':
                    year = st.selectbox("Year",("2018","2019","2020","2021","2022","2023","2024"),placeholder="Year-Wise")
                    quarter = st.selectbox("Quarter",("1","2","3","4"))
                    try:
                        cursor.execute("select state,sum(count),sum(amount) from map_transaction where year=%s and quarter=%s group by state order by state",(year,quarter))
                        df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                        df2 = pd.read_csv(r'C:\Users\Admin\PycharmProjects\pythonProject\TEST\Statenames (1).csv')

                        df1.State = df2
                        df1['Total_Transactions'] = pd.to_numeric(df1['Total_Transactions'], errors='coerce')

                        fig = px.choropleth(
                            df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Transactions',
                            color_continuous_scale="emrld",  # rdpu,blues,tealgrn,emrld,purp
                            range_color=(df1['Total_Transactions'].min(), df1['Total_Transactions'].max())
                        )

                        fig.update_geos(fitbounds="locations", visible=False)
                        st.plotly_chart(fig, use_container_width=True)

                        state = st.selectbox("State", state_values, placeholder="State-Wise")
                        cursor.execute(
                            "select district,sum(count),sum(amount) from map_transaction where year=%s and quarter=%s and state=%s group by district order by district",
                            (year, quarter,state))
                        df1 = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Transactions', 'Total_amount'])
                        df1.Total_amount = df1.Total_amount.astype(float)
                        fig = px.bar(df1,
                                     title='Top 10',
                                     x="District",
                                     y="Total_amount",
                                     orientation='v',
                                     color='District',
                                     color_continuous_scale=px.colors.sequential.Agsunset)
                        st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        print(e)
                        pass

            else:
                pass
        elif selected == 'Top Charts':
            st.header('Top Charts')

            state_name = st.selectbox("State", state_values, placeholder="State-Wise")
            year_value = st.selectbox("Year", ("2018", "2019", "2020", "2021", "2022", "2023", "2024"), placeholder="Year-Wise")
            quarter_value = st.selectbox("Quarter", ("1", "2", "3", "4"))

            if not state_name:
                cursor.execute("select state,sum(amount),sum(count) from top_transactions where year=%s and quarter=%s group by state order by sum(count) desc limit 10",(year_value,quarter_value))
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Amount', 'Total_Transactions'])
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Top 10 Transactions States**")
                    st.table(df1)
                df1.Total_Amount = df1.Total_Amount.astype(float)
                df1.Total_Transactions = df1.Total_Transactions.astype(float)
                fig = px.bar(df1,
                             title=' ',
                             x="State",
                             y="Total_Amount",
                             orientation='v',
                             color='State',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

                cursor.execute(
                    "select state,sum(registeredusers) from top_users where year=%s and quarter=%s group by state order by sum(registeredusers) desc limit 10",
                    (year_value, quarter_value))
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Registered_Users'])
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Top 10 Registered User States**")
                    st.table(df1)
                df1.Registered_Users = df1.Registered_Users.astype(float)
                fig = px.bar(df1,
                             title=' ',
                             x="State",
                             y="Registered_Users",
                             orientation='v',
                             color='State',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

            elif state_name:
                cursor.execute(
                    "select district,sum(amount),sum(count) from top_transactions where year=%s and quarter=%s and state = %s group by district order by sum(count) desc limit 10",
                    (year_value, quarter_value,state_name))
                df1 = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Amount', 'Total_Transactions'])
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Top 10 Transactions**")
                    st.table(df1)
                df1.Total_Amount = df1.Total_Amount.astype(float)
                df1.Total_Transactions = df1.Total_Transactions.astype(float)
                fig = px.bar(df1,
                             title=' ',
                             x="District",
                             y="Total_Amount",
                             orientation='v',
                             color='District',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

                cursor.execute(
                    "select district,sum(registeredusers) from top_users where year=%s and quarter=%s and state = %s group by district order by sum(registeredusers) desc limit 10",
                    (year_value, quarter_value,state_name))
                df1 = pd.DataFrame(cursor.fetchall(), columns=['District', 'Registered_Users'])
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Top 10 Registered User**")
                    st.table(df1)
                df1.Registered_Users = df1.Registered_Users.astype(float)
                fig = px.bar(df1,
                             title=' ',
                             x="District",
                             y="Registered_Users",
                             orientation='v',
                             color='District',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

                cursor.execute(
                    "select brand,sum(count) from aggregate_user where year=%s and quarter=%s and state = %s group by brand order by sum(count) desc limit 10",
                    (year_value, quarter_value, state_name))
                df3 = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Users'])
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Top 10 Mobile Brand User**")
                    st.table(df3)
                df3.Users = df3.Users.astype(float)
                fig = px.bar(df3,
                             title=' ',
                             x="Brand",
                             y="Users",
                             orientation='v',
                             color='Brand',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                with col2:
                    st.plotly_chart(fig, use_container_width=True)

            else:
                pass

if __name__ == "__main__":
    main()
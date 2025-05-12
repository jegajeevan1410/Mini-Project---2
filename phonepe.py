import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector as db
import plotly.express as px
import requests
import json
import uuid
from PIL import Image

st.set_page_config(layout="wide")


# DataFrame creation 
#sql connection 

#db_connection

user = "phonepe"
passcode = "Phonepe@1410"
host = "localhost"
db_name = "pp"

# Connect to MySQL
conn = db.connect(
    host=host,
    user=user,
    password=passcode,
    database=db_name
)
cursor = conn.cursor()
print("✅ Database connected successfully!")

#Aggregated

#Agg_insurance_df

cursor.execute("SELECT * FROM agg_insurance")
table1 = cursor.fetchall()

Agg_insurance = pd.DataFrame(table1, columns=("state", "year", "Quarter", "Transacion_type","Transacion_count","Transacion_amount"))


#Agg_Trans_df

cursor.execute("SELECT * FROM agg_trans")
table2 = cursor.fetchall()

Agg_transaction = pd.DataFrame(table2, columns=("state", "year", "Quarter", "Transacion_type","Transacion_count","Transacion_amount"))


#Agg_user_df

cursor.execute("SELECT * FROM agg_user")
table3 = cursor.fetchall()

Agg_user = pd.DataFrame(table3, columns=("state", "year", "Quarter", "Brands","Transacion_counts","Percentage"))


#Map

#Map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
table4 = cursor.fetchall()

Map_insurance = pd.DataFrame(table4, columns=("state", "year", "Quarter", "Districts","Transacion_count","Transacion_amount"))


#Map_transaction_df

cursor.execute("SELECT * FROM map_trans")
table5 = cursor.fetchall()

Map_transaction = pd.DataFrame(table5, columns=("state", "year", "Quarter", "Districts","Transacion_count","Transacion_amount"))


#Map_user_df

cursor.execute("SELECT * FROM map_user")
table6 = cursor.fetchall()

Map_user = pd.DataFrame(table6, columns=("state", "year", "Quarter", "Districts","Registered_Users","App_Opens"))


#Top

#Top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
table7 = cursor.fetchall()

Top_insurance = pd.DataFrame(table7, columns=("state", "year", "Quarter", "Pincodes","Transacion_count","Transacion_amount"))


#Top_transaction_df

cursor.execute("SELECT * FROM top_trans")
table8 = cursor.fetchall()

Top_transaction = pd.DataFrame(table8, columns=("state", "year", "Quarter", "Pincodes","Transacion_count","Transacion_amount"))


#Top_user_df

cursor.execute("SELECT * FROM top_user")
table9 = cursor.fetchall()

Top_user = pd.DataFrame(table9, columns=("state", "year", "Quarter", "Pincodes","Registered_Users"))



def Transaction_amount_count_Y(df, year):

    tacy=df[df["year"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("state")[["Transacion_count","Transacion_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    
    with col1:

        fig_amt1=px.bar(tacyg,x="state",y="Transacion_amount",title=f"{year} TRANSACTION AMOUNT",color="Transacion_amount",
                       height=650,width=600)
        st.plotly_chart(fig_amt1, key=f"fig_amt1_{year}_{uuid.uuid4()}")

    with col2:    

        fig_count1=px.bar(tacyg,x="state",y="Transacion_count",title=f"{year} TRANSACTION COUNT",color="Transacion_count",
                         height=650,width=600)
        st.plotly_chart(fig_count1, key=f"fig_count1_{year}_{uuid.uuid4()}")

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1= json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    col1, col2 = st.columns(2)

    with col1:

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations='state', featureidkey="properties.ST_NM", color="Transacion_amount", 
                                    color_continuous_scale="Rainbow", range_color=(tacyg["Transacion_amount"].min(), tacyg["Transacion_amount"].min()),
                                    hover_name= "state", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations", height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1, key=f"fig_india_1_{year}_{uuid.uuid4()}")

    with col2:    

        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations='state', featureidkey="properties.ST_NM", color="Transacion_count", 
                                    color_continuous_scale="Rainbow", range_color=(tacyg["Transacion_count"].min(), tacyg["Transacion_count"].min()),
                                    hover_name= "state", title=f"{year} TRANSACTION COUNT", fitbounds="locations", height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2, key=f"fig_india_2_{year}_{uuid.uuid4()}")  

    return tacy 

def Transaction_amount_count_Y_Q(df, quarter):

    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("state")[["Transacion_count","Transacion_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:

        fig_amt=px.bar(tacyg,x="state",y="Transacion_amount",title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",color="Transacion_amount",height=600, width=600)
        st.plotly_chart(fig_amt, key=f"fig_amt_{quarter}_{uuid.uuid4()}")

    with col2:    

        fig_count=px.bar(tacyg,x="state",y="Transacion_count",title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",color="Transacion_count",height=600, width=600)
        st.plotly_chart(fig_count, key=f"fig_count_{quarter}_{uuid.uuid4()}")

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1= json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    col1, col2 = st.columns(2)

    with col1:

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations='state', featureidkey="properties.ST_NM", color="Transacion_amount", 
                                    color_continuous_scale="Rainbow", range_color=(tacyg["Transacion_amount"].min(), tacyg["Transacion_amount"].min()),
                                    hover_name= "state", title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations", height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1, key=f"fig_india_1_{quarter}_{uuid.uuid4()}")

    with col2:    
 
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations='state', featureidkey="properties.ST_NM", color="Transacion_count", 
                                    color_continuous_scale="Rainbow", range_color=(tacyg["Transacion_count"].min(), tacyg["Transacion_count"].min()),
                                    hover_name= "state", title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations", height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2, key=f"fig_india_2_{quarter}_{uuid.uuid4()}")

    return tacy    

def Agg_Tran_Transaction_type(df, state):

    tacy=df[df["state"]== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transacion_type")[["Transacion_count","Transacion_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:

        fig_pie_1=px.pie(data_frame=tacyg, names="Transacion_type", values="Transacion_amount", 
                            width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5, )
        st.plotly_chart(fig_pie_1)

    with col2:    

        fig_pie_2=px.pie(data_frame=tacyg, names="Transacion_type", values="Transacion_count", 
                            width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5, )
        st.plotly_chart(fig_pie_2)


#Aggre user analysis 1
def Agg_user_plot_1(df,year):

    aguy = df[df["year"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transacion_counts"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transacion_counts", title=f"{year} BRAND AND TRANSACTION COUNT", width=1000, 
                       color="Transacion_counts",hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy  

#Agg_user analysis 2
def Agg_user_plot_2(df,quarter):

    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transacion_counts"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2 = px.bar(aguyqg, x="Brands", y="Transacion_counts", title =f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000, color="Transacion_counts", hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq

#Agg user analysis 3
def Agg_user_Y_plot_3(df, state):
    
    auyqs = df[df["state"] == state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transacion_counts", hover_data="Percentage",
                         title=f"{state.upper()} =BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(fig_line_1)

#Mapinsurance district
def Map_insur_District(df, state):

    tacy=df[df["state"]== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Districts")[["Transacion_count","Transacion_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_bar_1=px.bar(data_frame=tacyg, x="Transacion_amount", y="Districts", orientation="h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color="Transacion_amount")
    st.plotly_chart(fig_bar_1)

    fig_bar_2=px.bar(data_frame=tacyg, x="Transacion_count", y="Districts", orientation="h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color="Transacion_count") 
    st.plotly_chart(fig_bar_2)

#Map_user_plot1
def map_user_plot_1(df, year):

    muy = df[df["year"]== year]
    muy.reset_index(drop=True,inplace=True)

    muyg = muy.groupby("state")[["Registered_Users","App_Opens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x="state", y=["Registered_Users","App_Opens"],
                            title= f"{year} REGISTERED USER AND APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)

    return muy

#Map_user_plot_2
def map_user_plot_2(df,quarter):

    muyq = df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg =muyq.groupby("state")[["Registered_Users","App_Opens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_2 = px.line(muyqg, x="state", y=["Registered_Users","App_Opens"], title = f"{df['year'].min()} {quarter} QUARTER REGISTERED USER AND APPOPENS",
                    width=1000,height=800, markers=True, color_discrete_sequence=["blue", "orange"])
    st.plotly_chart(fig_line_2)

    return muyq

#map user_plot_3
def map_user_plot_3(df, state):
    muyqs = df[df["state"]==state]
    muyqs.reset_index(drop=True,inplace=True)

    col1, col2 = st.columns(2)
    with col1:

        fig_map_bar_1 = px.bar(muyqs, x="Registered_Users", y="Districts", orientation="h",
                                    title=f"{muyqs['state'].values[0].upper()} DISTRICT AND REGISTERED USER", width=1000, height=800, 
                                    color="Registered_Users")
        st.plotly_chart(fig_map_bar_1)

    with col2:

        fig_map_bar_2 = px.bar(muyqs, x="App_Opens", y="Districts", orientation="h",
                                    title=f"{muyqs['state'].values[0].upper()} DISTRICT AND APPOPENS", width=1000, height=800, 
                                    color="Registered_Users")
        st.plotly_chart(fig_map_bar_2)

# Top_insurance_plot_1
def Top_insurance_plot_1(df, state):
   
    tiy = df[df["state"]== state]
    tiy.reset_index(drop=True,inplace=True)

    col1, col2 = st.columns(2)
    with col1:

        fig_top_insur_bar_1=px.bar(tiy, x="Quarter", y="Transacion_amount", hover_data= "Pincodes",
                                title=f"{tiy['state'].values[0].upper()} PINCODES AND TRANSACTION AMOUNT",height=800, color="Transacion_amount")
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2=px.bar(tiy, x="Quarter", y="Transacion_count", hover_data= "Pincodes",
                                title=f"{tiy['state'].values[0].upper()} PINCODES AND TRANSACTION COUNT",height=800, color="Transacion_count")
        st.plotly_chart(fig_top_insur_bar_2) 


def Top_user_plot_1(df, year):

    tuy = df[df["year"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg = pd.DataFrame(tuy.groupby(["state","Quarter"])["Registered_Users"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_user_plot_1 = px.bar(tuyg, x="state", y="Registered_Users", color="Quarter", width=1000, height=800,
                                color_discrete_sequence=px.colors.sequential.Burg_r,hover_name="state", 
                                title=f"{year} REGISTERED USER AND QUARTER")
    st.plotly_chart(fig_top_user_plot_1)

    return tuy

#Top_user_plot_2
def Top_user_plot_2(df, state):

    tuys = df[df["state"]== state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_user_plot_2 = px.bar(tuys, x="Quarter", y="Registered_Users", color="Registered_Users", width=1000, height=800,
                                    color_continuous_scale=px.colors.sequential.Magenta,hover_data="Pincodes", 
                                    title=f"{tuys['state'].values[0].upper()} PINCODES AND REGISTERED USER")
    st.plotly_chart(fig_top_user_plot_2)

#db_connection

def top_chart_transaction_amount(table_name):

        user = "phonepe"
        passcode = "Phonepe@1410"
        host = "localhost"
        db_name = "pp"

        # Connect to MySQL
        conn = db.connect(
        host=host,
        user=user,
        password=passcode,
        database=db_name
        )
        cursor = conn.cursor()


        #Plot_1
        Query1=f"""SELECT State , SUM(Transacion_amount) as Transacion_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_amount DESC
                LIMIT 10;"""
        cursor.execute(Query1)
        table1=cursor.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table1,columns=("State","Transacion_amount"))

        col1,col2=st.columns(2)
        with col1:
    
            fig_amt1=px.bar(df_1,x="State",y="Transacion_amount",title="TOP 10 OF TRANSACTION AMOUNT",hover_name="State",
                    color="Transacion_amount",height=600, width=600)
            st.plotly_chart(fig_amt1)


        #Plot_2
        Query2=f"""SELECT State , SUM(Transacion_amount) as Transacion_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_amount
                LIMIT 10;"""
        cursor.execute(Query2)
        table2=cursor.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table2,columns=("State","Transacion_amount"))

        with col2:

            fig_amt2=px.bar(df_2,x="State",y="Transacion_amount",title="LAST 10 OF TRANSACTION AMOUNT",hover_name="State",
                    color="Transacion_amount",height=600, width=600)
            st.plotly_chart(fig_amt2)


        #Plot_3
        Query3=f"""SELECT State , AVG(Transacion_amount) as Transacion_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_amount;"""
        cursor.execute(Query3)
        table3=cursor.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table3,columns=("State","Transacion_amount"))

        fig_amt3=px.bar(df_3,x="Transacion_amount",y="State",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="State",orientation="h",
                color="Transacion_amount",height=800, width=1000)
        st.plotly_chart(fig_amt3)

#db_connection

def top_chart_transaction_count(table_name):

        user = "phonepe"
        passcode = "Phonepe@1410"
        host = "localhost"
        db_name = "pp"

        # Connect to MySQL
        conn = db.connect(
        host=host,
        user=user,
        password=passcode,
        database=db_name
        )
        cursor = conn.cursor()


        #Plot_1
        Query1=f"""SELECT State , SUM(Transacion_count) as Transacion_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_count DESC
                LIMIT 10;"""
        cursor.execute(Query1)
        table1=cursor.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table1,columns=("State","Transacion_count"))

        col1,col2=st.columns(2)
        with col1:

            fig_amt1=px.bar(df_1,x="State",y="Transacion_count",title="TRANSACTION COUNT",hover_name="State",
                    color="Transacion_count",height=600, width=600)
            st.plotly_chart(fig_amt1)


        #Plot_2
        Query2=f"""SELECT State , SUM(Transacion_count) as Transacion_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_count
                LIMIT 10;"""
        cursor.execute(Query2)
        table2=cursor.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table2,columns=("State","Transacion_count"))

        with col2:

            fig_amt2=px.bar(df_2,x="State",y="Transacion_count",title="TRANSACTION COUNT",hover_name="State",
                    color="Transacion_count",height=600, width=600)
            st.plotly_chart(fig_amt2)


        #Plot_3
        Query3=f"""SELECT State , AVG(Transacion_count) as Transacion_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transacion_count;"""
        cursor.execute(Query3)
        table3=cursor.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table3,columns=("State","Transacion_count"))

        fig_amt3=px.bar(df_3,x="Transacion_count",y="State",title="TRANSACTION COUNT",hover_name="State",orientation="h",
                color="Transacion_count",height=800, width=1000)
        st.plotly_chart(fig_amt3)

#db_connection

def top_chart_registered_user(table_name,state):

        user = "phonepe"
        passcode = "Phonepe@1410"
        host = "localhost"
        db_name = "pp"

        # Connect to MySQL
        conn = db.connect(
        host=host,
        user=user,
        password=passcode,
        database=db_name
        )
        cursor = conn.cursor()


        #Plot_1
        Query1=f"""SELECT Districts , SUM(Registered_Users) as Registered_Users
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY Registered_Users DESC
                    LIMIT 10;"""
        cursor.execute(Query1)
        table1=cursor.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table1,columns=("Districts","Registered_Users"))

        col1,col2=st.columns(2)
        with col1:

            fig_amt1=px.bar(df_1,x="Districts",y="Registered_Users",title="TOP 10 REGISTERED USER",hover_name="Districts",
                    color="Registered_Users",height=600, width=600)
            st.plotly_chart(fig_amt1)


        #Plot_2
        Query2=f"""SELECT Districts , SUM(Registered_Users) as Registered_Users
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY Registered_Users
                    LIMIT 10;"""
        cursor.execute(Query2)
        table2=cursor.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table2,columns=("Districts","Registered_Users"))

        with col2:

            fig_amt2=px.bar(df_2,x="Districts",y="Registered_Users",title="LAST 10 REGISTERED USER",hover_name="Districts",
                    color="Registered_Users",height=600, width=600)
            st.plotly_chart(fig_amt2)


        #Plot_3
        Query3=f"""SELECT Districts , AVG(Registered_Users) as Registered_Users
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY Registered_Users;"""
        cursor.execute(Query3)
        table3=cursor.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table3,columns=("Districts","Registered_Users"))

        fig_amt3=px.bar(df_3,x="Registered_Users",y="Districts",title="AVERAGE REGISTERED USER",hover_name="Districts",orientation="h",
                color="Registered_Users",height=800, width=1000)
        st.plotly_chart(fig_amt3)

#db_connection

def top_chart_app_opens(table_name,state):

        user = "phonepe"
        passcode = "Phonepe@1410"
        host = "localhost"
        db_name = "pp"

        # Connect to MySQL
        conn = db.connect(
        host=host,
        user=user,
        password=passcode,
        database=db_name
        )
        cursor = conn.cursor()


        #Plot_1
        Query1=f"""SELECT Districts , SUM(App_Opens) as App_Opens
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY App_Opens DESC
                    LIMIT 10;"""
        cursor.execute(Query1)
        table1=cursor.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table1,columns=("Districts","App_Opens"))

        col1,col2=st.columns(2)
        with col1:

            fig_amt1=px.bar(df_1,x="Districts",y="App_Opens",title="TOP 10 APP OPENS",hover_name="Districts",
                    color="App_Opens",height=600, width=600)
            st.plotly_chart(fig_amt1)


        #Plot_2
        Query2=f"""SELECT Districts , SUM(App_Opens) as App_Opens
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY App_Opens
                    LIMIT 10;"""
        cursor.execute(Query2)
        table2=cursor.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table2,columns=("Districts","App_Opens"))

        with col2:

            fig_amt2=px.bar(df_2,x="Districts",y="App_Opens",title="LAST 10 APP OPENS",hover_name="Districts",
                    color="App_Opens",height=600, width=600)
            st.plotly_chart(fig_amt2)


        #Plot_3
        Query3=f"""SELECT Districts , AVG(App_Opens) as App_Opens
                    FROM {table_name}
                    WHERE State = '{state}'
                    GROUP BY Districts
                    ORDER BY App_Opens;"""
        cursor.execute(Query3)
        table3=cursor.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table3,columns=("Districts","App_Opens"))

        fig_amt3=px.bar(df_3,x="App_Opens",y="Districts",title="AVERAGE APP OPENS",hover_name="Districts",orientation="h",
                color="App_Opens",height=800, width=1000)
        st.plotly_chart(fig_amt3)

#db_connection

def top_chart_registered_users(table_name):

        user = "phonepe"
        passcode = "Phonepe@1410"
        host = "localhost"
        db_name = "pp"

        # Connect to MySQL
        conn = db.connect(
        host=host,
        user=user,
        password=passcode,
        database=db_name
        )
        cursor = conn.cursor()


        #Plot_1
        Query1=f"""SELECT State , SUM(Registered_Users) as Registered_Users
                    FROM {table_name}
                    GROUP BY State
                    ORDER BY Registered_Users DESC
                    LIMIT 10 ;"""
        cursor.execute(Query1)
        table1=cursor.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table1,columns=("State","Registered_Users"))

        col1,col2=st.columns(2)
        with col1:

            fig_amt1=px.bar(df_1,x="State",y="Registered_Users",title="TOP 10 REGISTERED USERS",hover_name="State",
                    color="Registered_Users",height=600, width=600)
            st.plotly_chart(fig_amt1)


        #Plot_2
        Query2=f"""SELECT State , SUM(Registered_Users) as Registered_Users
                    FROM {table_name}
                    GROUP BY State
                    ORDER BY Registered_Users
                    LIMIT 10 ;"""
        cursor.execute(Query2)
        table2=cursor.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table2,columns=("State","Registered_Users"))

        with col2:

            fig_amt2=px.bar(df_2,x="State",y="Registered_Users",title="LAST 10 REGISTERED USERS",hover_name="State",
                    color="Registered_Users",height=600, width=600)
            st.plotly_chart(fig_amt2)


        #Plot_3
        Query3=f"""SELECT State , AVG(Registered_Users) as Registered_Users
                    FROM {table_name}
                    GROUP BY State
                    ORDER BY Registered_Users;"""
        cursor.execute(Query3)
        table3=cursor.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table3,columns=("State","Registered_Users"))

        fig_amt3=px.bar(df_3,x="Registered_Users",y="State",title="AVERAGE REGISTERED USERS",hover_name="State",orientation="h",
                color="Registered_Users",height=800, width=1000)
        st.plotly_chart(fig_amt3)


     
#Streamlit page 


st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video(r"E:\PHONEPE\Image\videoplayback.mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"E:\PHONEPE\Image\images.jpeg"),width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"E:\PHONEPE\Image\download.jpeg"),width= 600)

    

elif select == "Data Exploration":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the year",Agg_insurance["year"].min(),Agg_insurance["year"].max(),Agg_insurance["year"].min())
            tac_Y = Transaction_amount_count_Y(Agg_insurance, years)

            col1,col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
                           
        elif method == "Transaction Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year",Agg_transaction["year"].min(),Agg_transaction["year"].max(),Agg_transaction["year"].min())
            Agg_tran_tac_Y = Transaction_amount_count_Y(Agg_transaction, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state",Agg_tran_tac_Y["state"].unique())

            Agg_Tran_Transaction_type(Agg_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Agg_tran_tac_Y["Quarter"].min(),Agg_tran_tac_Y["Quarter"].max(),Agg_tran_tac_Y["Quarter"].min())
            Agg_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Agg_tran_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ty",Agg_tran_tac_Y_Q["state"].unique())

            Agg_Tran_Transaction_type(Agg_tran_tac_Y_Q, states)
            

        elif method == "User Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the year",Agg_user["year"].min(),Agg_user["year"].max(),Agg_user["year"].min())
            Agg_user_Y = Agg_user_plot_1(Agg_user, years)

            available_quarters = Agg_user_Y["Quarter"].unique()

            col1, col2 = st.columns(2)
            with col1:
                if len(available_quarters) == 1:
                    # Only one quarter is available, auto-select it
                    st.write(f"Only one quarter available: {available_quarters[0]}")
                    quarters = available_quarters[0]
                else:
                    # Multiple quarters, allow user to select
                    quarters = st.slider("Select the Quarter", int(available_quarters.min()), int(available_quarters.max()), int(available_quarters.min()))
            Agg_user_Y_Q = Agg_user_plot_2(Agg_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ty",Agg_user_Y_Q["state"].unique())

            Agg_user_Y_plot_3(Agg_user_Y_Q, states)

    with tab2:

        method_2 = st.radio("Select the method", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_2 == "Map Insurance Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year",Map_insurance["year"].min(),Map_insurance["year"].max(),Map_insurance["year"].min())
            Map_insur_tac_Y = Transaction_amount_count_Y(Map_insurance, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_MI",Map_insur_tac_Y["state"].unique())

            Map_insur_District(Map_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter_mi",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insur_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ty_mi",Map_insur_tac_Y_Q["state"].unique())

            Map_insur_District(Map_insur_tac_Y_Q, states)
   
        elif method_2 == "Map Transaction Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year_Tr",Map_transaction["year"].min(),Map_transaction["year"].max(),Map_transaction["year"].min())
            Map_trans_tac_Y = Transaction_amount_count_Y(Map_transaction, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Tr",Map_trans_tac_Y["state"].unique())

            Map_insur_District(Map_trans_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter_Tr",Map_trans_tac_Y["Quarter"].min(),Map_trans_tac_Y["Quarter"].max(),Map_trans_tac_Y["Quarter"].min())
            Map_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Map_trans_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ty_Tr",Map_trans_tac_Y_Q["state"].unique())

            Map_insur_District(Map_trans_tac_Y_Q, states)
            
        elif method_2 == "Map User Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the year_Mu",Map_user["year"].min(),Map_user["year"].max(),Map_user["year"].min())
            Map_user_Y = map_user_plot_1(Map_user, years)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter_Mu",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q = map_user_plot_2(Map_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ty_Mu",Map_user_Y_Q["state"].unique())

            map_user_plot_3(Map_user_Y_Q, states)
            

    with tab3:

        method_3 = st.radio("Select the method", ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_3 == "Top Insurance Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year_Ti",Top_insurance["year"].min(),Top_insurance["year"].max(),Top_insurance["year"].min())
            Top_insur_tac_Y = Transaction_amount_count_Y(Top_insurance, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Ti",Top_insur_tac_Y["state"].unique())

            Top_insurance_plot_1(Top_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter_TT",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insur_tac_Y, quarters)
      
        elif method_3 == "Top Transaction Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year_TT",Top_transaction["year"].min(),Top_transaction["year"].max(),Top_transaction["year"].min())
            Top_trans_tac_Y = Transaction_amount_count_Y(Top_transaction, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_TT",Top_trans_tac_Y["state"].unique())

            Top_insurance_plot_1(Top_trans_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter_Ti",Top_trans_tac_Y["Quarter"].min(),Top_trans_tac_Y["Quarter"].max(),Top_trans_tac_Y["Quarter"].min())
            Top_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Top_trans_tac_Y, quarters)
            
        elif method_3 == "Top User Analysis":
            col1, col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year_Tu",Top_user["year"].min(),Top_user["year"].max(),Top_user["year"].min())
            Top_user_Y = Top_user_plot_1(Top_user, years)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select the state_Tu",Top_user_Y["state"].unique())

            Top_user_plot_2(Top_user_Y, states)
            

elif select == "Top Charts":

    question=st.selectbox("Select the question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                 "2. Transaction Amount and Count of Map Insurance",
                                                 "3. Transaction Amount and Count of Top Insurance",
                                                 "4. Transaction Amount and Count of Aggregated Transaction",
                                                 "5. Transaction Amount and Count of Map Transaction",
                                                 "6. Transaction Amount and Count of Top Transaction",
                                                 "7. Transaction Count of Aggregated User",
                                                 "8. Registered users of Map User",
                                                 "9. App opens of Map User",
                                                 "10. Registered users of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("agg_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("agg_insurance")
    
    elif question == "2. Transaction Amount and Count of Map Insurance":
            
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
                
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
          
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("agg_trans")
        st.subheader("Transaction Count")
        top_chart_transaction_count("agg_trans")

    elif question == "5. Transaction Amount and Count of Map Transaction":
            
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_trans")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_trans")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_trans")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_trans")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("Transaction Count")
        top_chart_transaction_count("agg_user")

    elif question == "8. Registered users of Map User":

        states= st.selectbox("Select a state",Map_user["state"].unique())

        st.subheader("Registered users")
        top_chart_registered_user("map_user",states)

    elif question == "9. App opens of Map User":

        states= st.selectbox("Select a state",Map_user["state"].unique())

        st.subheader("App opens")
        top_chart_app_opens("map_user",states)

    elif question == "10. Registered users of Top User":

        st.subheader("Registered users")
        top_chart_registered_users("top_user")

    

    

    
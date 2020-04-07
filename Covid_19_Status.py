#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[ ]:





# In[2]:


url = 'https://www.mohfw.gov.in/' #URL to fetch the Covid-19 Data for India


# In[ ]:





# In[3]:


# Fetch the data from above URL
web_content = requests.get(url).content

# Parse the content as HTML
soup = BeautifulSoup(web_content, "html.parser")

# Remove extra spaces ,if any
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

# Iterate through the table and get the data one by one
stats = [] 
all_rows = soup.find_all('tr')
for row in all_rows:
    stat = extract_contents(row.find_all('td')) 

# Our data is now in the list of size 5
    if len(stat) == 5:
        stats.append(stat)


# In[ ]:





# In[ ]:





# In[4]:


#Create the Pandas DataFrame from above data 
new_cols = ["Sr.No", "States/UT","Confirmed","Recovered","Deceased"]
state_data = pd.DataFrame(data = stats, columns = new_cols)
state_data.head()


# In[ ]:





# In[5]:


state_data['Confirmed'] = state_data['Confirmed'].map(int)
state_data['Recovered'] = state_data['Recovered'].map(int)
state_data['Deceased'] = state_data['Deceased'].map(int)


# In[6]:


#Drop Sr.no bcoz we dont require it
state_data.drop(['Sr.No'],axis=1,inplace=True)


# In[7]:


state_data.sort_values(by='Confirmed',ascending=False,inplace=True)#Sort based on Confirmed number of cases


# In[8]:


state_data.head()


# In[9]:


state_data['Active']=state_data['Confirmed']-(state_data['Recovered']+state_data['Deceased'])
state_data


# In[ ]:





# In[10]:


#Create summary of all the indian states
total_confirmed=str(state_data['Confirmed'].sum())
#print(total_confirmed)
total_recovered=str(state_data['Recovered'].sum())
#print(total_recovered)
total_deaths=str(state_data['Deceased'].sum())
#print(total_deaths)

total_active=str(state_data['Active'].sum())
#print(total_active)




# In[11]:


#Save the above results in the list
cases_summary_numbers=[total_active,total_deaths,total_recovered]
cases_summary_labels=['Active','Deaths','Recovered']


# In[ ]:





# In[12]:


# Create list to be shown in dropdown
state_list=state_data['States/UT'].to_list()
options=[]
for state in state_list:
    options.append({'label':state ,'value':state})


# In[ ]:





# In[ ]:





# In[13]:


import plotly.graph_objs as go
import dash
import dash_core_components as dcc #High level abstract components
import dash_html_components as html #For using html tag like methods
from dash.dependencies import Input, Output, State
import dash_table


# In[ ]:





# In[ ]:





# In[14]:


#Create the Traces for Bar chart.Needed for Top 5 states Bar chart
top_traces=[]
df_top_five=state_data.head(5)
states=df_top_five['States/UT'].to_list()
recovered=df_top_five['Recovered'].to_list()
deaths=df_top_five['Deceased'].to_list()
active=df_top_five['Active'].to_list()


top_traces.append(go.Bar(x=states,y=active,name='Active'))        
top_traces.append(go.Bar(x=states,y=recovered,name='Recovered'))
top_traces.append(go.Bar(x=states,y=deaths,name='Death'))        


# In[ ]:





# In[15]:


app = dash.Dash()


# In[16]:


server=app.server


# In[ ]:





# In[17]:


#Set the title of the app
app.title='Covid-19 India'


# In[ ]:





# In[ ]:





# In[34]:


#Set the app layout
app.layout = html.Div(children=[
                
                
               html.H1(
                    children='Covid-19 Live Status Tracking',
                    style={
                            'textAlign': 'center',
                            'color': 'red',
                            'text-decoration': 'underline',
                            'margin':'8px'
                            }
                    ),#Ends Heading of the Dashboard
    
                html.Br(),
                
                html.Div([
                    
                    html.Div([html.H3('Confirmed')],style={'color':'red',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3('Active')],style={'color':'blue',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    
                     html.Div([html.H3('Recovered')],style={'color':'green',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3('Deaths')],style={'color':'gray',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'})
                    
                  
                ]),#End Div for Indian Summary headings   
    
    
            html.Div([
                    
                    html.Div([html.H3(''+total_confirmed)],style={'color':'red',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3(''+total_active)],style={'color':'blue',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    
                     html.Div([html.H3(''+total_recovered)],style={'color':'green',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3(''+total_deaths)],style={'color':'gray',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'})
                    
                    
                    
                ]),#ENd Div for Indian Summary Numbers
    

    
                html.Div([
                    dash_table.DataTable(
                    id='summary_table',
                    columns=[{"name": i, "id": i} for i in state_data.columns],
                    data=state_data.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    sort_action="native",
                    sort_mode="multi",

                    style_data={ 'border': '1px solid blue' },
                    style_header={ 'border': '1px solid red' },

                    style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }
                                            ],
                           )],style={'display':'inline-block', 'verticalAlign':'top', 'width':'40%'}
                ),#End Div for Table
                
    
    #Parent Div for state Headings      
    html.Div([
        
            html.Div([
                    
                    html.Div([html.H3('Confirmed')],style={'color':'red',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3('Active')],style={'color':'blue',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    
                     html.Div([html.H3('Recovered')],style={'color':'green',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    html.Div([html.H3('Deaths')],style={'color':'gray',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'})              
                    
                ],style={'float':'right'}),#ENd div for state headings
    
    
    
    
        html.Div(id='state_headings',style={'float':'right'}),  #This will dynamically show state numbers 
        
        
        
        html.H3('Select your state:',style={'float':'right'}),
        dcc.Dropdown(
            id='my_state',
            options=options,
            value='Delhi'
        ),#Dropdown ends
        
        dcc.Graph(id="my_graph",config={'displayModeBar':False}),#State Chart
        
         dcc.Graph(id='top_graph',
                   config={'displayModeBar':False},
                figure={
                    'data': top_traces,
                    'layout': {'title': 'Top 5 States','barmode':'stack'}
                
                }
             )#End chart for top 5 states
        
    ], style={'display':'inline-block',  'width':'50%','margin-left':'24px','float':'right','align':'right'}),#End paraent div for headings
    
   
   
    
],style={'margin':'16px'})#End container div   


# In[19]:


# Method for updating the heading of the states when user selects from the dropdown
@app.callback(
    Output('state_headings', 'children'),
    [Input('my_state', 'value')])
def update_headings(selected_state):
    #print('update ' +selected_state )
    
    # Return the list of <div>,each holds the type of cases
    return [html.Div([html.H3(state_data[state_data['States/UT']==selected_state]['Confirmed'])],style={'color':'red',
                          'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),

                    html.Div([html.H3(state_data[state_data['States/UT']==selected_state]['Active'])],style={'color':'blue',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
                    
                     html.Div([html.H3(state_data[state_data['States/UT']==selected_state]['Recovered'])],style={'color':'green',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'}),
            
                    html.Div([html.H3(state_data[state_data['States/UT']==selected_state]['Deceased'])],style={'color':'gray',
                            'margin':'4px','width':'100px','display':'inline-block','text-align':'center'})]


# In[20]:


#Method for updating the state Chart when user selects from the dropdown
@app.callback(
    Output('my_graph', 'figure'),
    [Input('my_state', 'value')])
def update_graph(value):
   # print(value)
    cases_summary_label=['Active','Deaths','Recovered']
    confirmed=int(state_data[state_data['States/UT']==value]['Confirmed'])
    recovered=int(state_data[state_data['States/UT']==value]['Recovered'])
    deaths=int(state_data[state_data['States/UT']==value]['Deceased'])
    active=int(state_data[state_data['States/UT']==value]['Active'])
    cases_summary_number=[active,deaths,recovered]
   # print(cases_summary_number)
    
    piedata=[go.Pie(labels=cases_summary_label, values=cases_summary_number,hole=0.3, pull=[0.2, 0,0])]
    return {
        'data': piedata,
        'layout': {'title':value+' Cases Summary'}
    }
    


# In[ ]:





# In[21]:


#Run the server
if __name__ == '__main__':
    app.run_server()
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import dash 
from dash import html,dcc,Input,Output,State
import pandas as pd 
import dash_daq  as daq
import dash_bootstrap_components as dbc
global data 
import json 
data=5
server = Flask(__name__)
server.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
server.config['MQTT_BROKER_PORT'] = 1883
server.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
server.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
server.config['MQTT_KEEPALIVE'] = 60  # Set KeepAlive time in seconds
server.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True

mqtt_client = Mqtt(server)
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe('sensor') # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   global data
   data=json.loads(message.payload.decode())
   
   #print('Received message on topic: {topic} with payload: {payload}'.format(**data))

@server.route('/publish', methods=['POST'])
def publish_message():
   publish_result = mqtt_client.publish('test/lights',"livingroom")
   return jsonify({'code': publish_result[0]})

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY],serve_locally=server)
app.layout=dbc.Container([
dbc.Row(dbc.Col(html.H2("Bavan Smart Home system"))),
dbc.Row([
    dbc.Col(daq.Gauge(id="temp_gauge",min=0,max=100,label="Tempreture",showCurrentValue=True,units=".C",className='dark-theme-control'),width={"size":1, "offset": 8}),
         dcc.Interval(id="temp_time",interval=2000,n_intervals=0)]),
dbc.Row([dbc.Col(
    dbc.Card(dbc.CardBody([html.H4("LivingRoom"),
    daq.PowerButton(id="livingroom_switch",on=False,className='dark-theme-control')])),width={"size":3, "offset":0}),
    html.Div(id='light_output'),
    dbc.Col(
    dbc.Card(dbc.CardBody([html.H4("Bathroom"),
    daq.PowerButton(id="bathroom_switch",on=False,className='dark-theme-control'
)])),width={"size":3, "offset":0}),
    html.Div(id='bathl_output'),
    dbc.Col(
    dbc.Card(dbc.CardBody([html.H4("Bedroom"),
    daq.PowerButton(id="bedroom_switch",on=False,className='dark-theme-control')])),width={"size":3, "offset":0}),
    html.Div(id='bedl_output'),]
),

])
@app.callback(Output('temp_gauge','value'),Input('temp_time','n_intervals'))
def update_tempreture(n):
    if data:    
    #mqtt_client.publish('test/lights',"livingroom")
        return data['tempreture']
    else:
        dash.no_update
@app.callback(Output('light_output','children'),Input('livingroom_switch','on'))
def switch_light(on):
    if on==True:
        mqtt_client.publish("test/lights","livingroom-on")
    elif on==False: 
        mqtt_client.publish("test/lights","livingroom-off")

    else:
        dash.no_update
@app.callback(Output('bathl_output','children'),Input('bathroom_switch','on'))
def switch_light(on):
    if on==True:
        mqtt_client.publish("test/lights","bathroom-on")
    elif on==False: 
        mqtt_client.publish("test/lights","bathroom-off")

    else:
        dash.no_update
@app.callback(Output('bedl_output','children'),Input('bedroom_switch','on'))
def switch_light(on):
    if on==True:
        mqtt_client.publish("test/lights","bedroom-on")
    elif on==False: 
        mqtt_client.publish("test/lights","bedroom-off")

    else:
        dash.no_update
if __name__ == '__main__':
   app.run_server(port=5000)

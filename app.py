from flask import Flask , render_template , request
import jsonify
import requests
import joblib
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

#load the model
#model = pickle.load(open('random_forest_regression_model.pkl' , 'rb'))
model = pickle.load(open('xgboost_regression_model.pkl' , 'rb'))
@app.route('/' ,methods =['GET'])
def home():
    return render_template('home.html')

@app.route('/trail',methods =['GET'])
def trial():
    return render_template('trial.html')

#initialize standard scaler
standard_to = StandardScaler()

@app.route('/predict' , methods = ['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        #Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        
        #prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        prediction = model.predict(np.array([Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]).reshape(1,-1))
        
        output = round(prediction[0],2)
        if output<0:
            return render_template('home.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('home.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('home.html')
        

if __name__=="__main__":
    app.run(debug=True)
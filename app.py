from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

#load the trained model
model = pickle.load(open('model_v01.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        #Get ssc infomration
        ssc_b = (request.form['ssc_board'])
        if (ssc_b=='Central'):
            ssc_b_Central=1
            ssc_b_Others=0
        else:
            ssc_b_Central=0
            ssc_b_Others=1
        
        ssc_p=float(request.form['ssc_percentage'])

        #Get hsc information
        hsc_b=(request.form['hsc_b'])
        if(hsc_b=='Central'):
            hsc_b_Central=1
            hsc_b_Others=0
        else:
            hsc_b_Central=0
            hsc_b_Others=1

        hsc_s=request.form['hsc_specialization']
        if (hsc_s=='Arts'):
            hsc_s_Arts=1
            hsc_s_Commerce=0
            hsc_s_Science=0
        elif (hsc_s=='Commerce'):
            hsc_s_Arts=0
            hsc_s_Commerce=1
            hsc_s_Science=0
        else:
            hsc_s_Arts=0
            hsc_s_Commerce=0
            hsc_s_Science=1

        hsc_p=float(request.form['hsc_percentage'])

        #Get Graduation Infomration
        degree_t=request.form['degree_specialization']
        if(degree_t=='Comm&Mgmt'):
            degree_t_CommMgmt=1
            degree_t_SciTech=0
            degree_t_Others=0
        elif(degree_t=='Sci&Tech'):
            degree_t_CommMgmt=0
            degree_t_SciTech=1
            degree_t_Others=0
        else:
            degree_t_CommMgmt=0
            degree_t_SciTech=0
            degree_t_Others=1
        
        degree_p=request.form['degree_percentage']

        #Get MBA Information
        mba_s=request.form['mba_specilization']
        if(mba_s=='Mkt&HR'):
            mba_MktHR=1
            mba_MktFin=0
        else:
            mba_MktHR=0
            mba_MktFin=1
        
        mba_p=float(request.form['mba_percentage'])

        #Get Employment details
        etest_p=float(request.form['employabilityTest_percentage'])
        
        workex=request.form['work_experience']
        if (workex=='Yes'):
            workex_Yes=1
            workex_No=0
        else:
            workex_Yes=0
            workex_No=1

        # Make predicitons from the model

        prediction=model.predict([['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p', 'ssc_b_Central',
       'ssc_b_Others', 'hsc_b_Central', 'hsc_b_Others', 'hsc_s_Arts',
       'hsc_s_Commerce', 'hsc_s_Science', 'degree_t_CommMgmt',
       'degree_t_Others', 'degree_t_SciTech', 'workex_No', 'workex_Yes',
       'mba_MktFin', 'mba_MktHR']])

        output=round(prediction[0],2)
        
        if output<0:
            return render_template('index.html',prediction_placement="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_placement="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
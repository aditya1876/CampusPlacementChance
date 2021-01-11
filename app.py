from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import sklearn
import pandas as pd
#from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

#load the trained model
model_salary = pickle.load(open('model_salaryPredictor_v01.pkl', 'rb'))
model_status = pickle.load(open('model_statusPredictor_v01.pkl', 'rb'))


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':

        #Get ssc infomration
        ssc_b = str(request.form['ssc_board'])
        if (ssc_b=='Central'):
            ssc_b_Central=1.0
            ssc_b_Others=0.0
        else:
            ssc_b_Central=0.0
            ssc_b_Others=1.0
        
        ssc_p=float(request.form['ssc_percentage'])

        #Get hsc information
        hsc_b=str(request.form['hsc_board'])
        if(hsc_b=='Central'):
            hsc_b_Central=1.0
            hsc_b_Others=0.0
        else:
            hsc_b_Central=0.0
            hsc_b_Others=1.0

        hsc_s=str(request.form['hsc_specialization'])
        if (hsc_s=='Arts'):
            hsc_s_Arts=1.0
            hsc_s_Commerce=0.0
            hsc_s_Science=0.0
        elif (hsc_s=='Commerce'):
            hsc_s_Arts=0.0
            hsc_s_Commerce=1.0
            hsc_s_Science=0.0
        else:
            hsc_s_Arts=0.0
            hsc_s_Commerce=0.0
            hsc_s_Science=1.0

        hsc_p=float(request.form['hsc_percentage'])

        #Get Graduation Infomration
        degree_t=str(request.form['degree_specialization'])
        if(degree_t=='Comm&Mgmt'):
            degree_t_CommMgmt=1.0
            degree_t_SciTech=0.0
            degree_t_Others=0.0
        elif(degree_t=='Sci&Tech'):
            degree_t_CommMgmt=0.0
            degree_t_SciTech=1.0
            degree_t_Others=0.0
        else:
            degree_t_CommMgmt=0.0
            degree_t_SciTech=0.0
            degree_t_Others=1.0
        
        degree_p=str(request.form['degree_percentage'])

        #Get MBA Information
        mba_s=str(request.form['mba_specilization'])
        if(mba_s=='Mkt&HR'):
            mba_MktHR=1.0
            mba_MktFin=0.0
        else:
            mba_MktHR=0.0
            mba_MktFin=1.0
        
        mba_p=float(request.form['mba_percentage'])

        #Get Employment details
        etest_p=float(request.form['employabilityTest_percentage'])
        
        workex=str(request.form['work_experience'])
        if (workex=='Yes'):
            workex_Yes=1.0
            workex_No=0.0
        else:
            workex_Yes=0.0
            workex_No=1.0

        # Make predicitons from the model
        prediction_salary=round(model_salary.predict(pd.DataFrame([[ssc_p, hsc_p, degree_p, etest_p, mba_p, ssc_b_Central,ssc_b_Others, hsc_b_Central, hsc_b_Others, hsc_s_Arts,hsc_s_Commerce, hsc_s_Science, degree_t_CommMgmt,degree_t_Others, degree_t_SciTech, workex_No, workex_Yes,mba_MktFin, mba_MktHR]]))[0],2)

        prediction_status=model_status.predict(pd.DataFrame([[ssc_p, hsc_p, degree_p, etest_p, mba_p, ssc_b_Central,ssc_b_Others, hsc_b_Central, hsc_b_Others, hsc_s_Arts,hsc_s_Commerce, hsc_s_Science, degree_t_CommMgmt,degree_t_Others, degree_t_SciTech, workex_No, workex_Yes,mba_MktFin, mba_MktHR]]))    

        #Display output
        if prediction_status<1:
            return render_template('index.html',prediction_placement="Sorry, you may not be placed based on the provided information {}".format(prediction_status))
        else:
            return render_template('index.html',prediction_placement="You can expect to get a salary of Rs. {}".format([prediction_salary]))

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
import streamlit as st
import json
import urllib.request
import os
import ssl

st.title('Creditworthiness Predictor')

st.write('This application is used to predict whether a person is creditworthy or not based on his/her age,income,debtinc and creddebt.The predictor is build using an AzrueML endpoint.')

age = st.number_input('Enter your age', min_value=10, max_value=100)
income = st.number_input('Enter your annual income', min_value=0, max_value=10000000000)
debtinc = st.number_input('Enter your debtinc ratio', min_value=0, max_value=50)
creddebt = st.number_input('Enter your creditdebt ratio', min_value=0, max_value=50)



if st.button('Click Here To Check if you are credit worthy or not'):
            def allowSelfSignedHttps(allowed):
                # bypass the server certificate verification on client side
                if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                    ssl._create_default_https_context = ssl._create_unverified_context

            allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

            # Request data goes here
            # The example below assumes JSON formatting which may be updated
            # depending on the format your endpoint expects.
            # More information can be found here:
            # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
            data =  {
            "Inputs": {
                "input1": [
                {
                    "age": age,
                    "income": income,
                    "debtinc": debtinc,
                    "creddebt": creddebt
                },
                ]
            },
            "GlobalParameters": {}
            }

            body = str.encode(json.dumps(data))

            url = 'http://ad5cc40c-9d28-4a4d-9633-d9bfe6f87863.canadacentral.azurecontainer.io/score'
            # Replace this with the primary/secondary key or AMLToken for the endpoint
            api_key = 'VgLYlVwPDqSnHfhEFwoF8HtMm9PZ6p8u'
            if not api_key:
                raise Exception("A key should be provided to invoke the endpoint")


            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

            req = urllib.request.Request(url, body, headers)
                
            try:
                response = urllib.request.urlopen(req)
                data = response.read()
                data = json.loads(data)
                predicted_class = data['Results']['WebServiceOutput0'][0]['Predicted_Class']
                print(predicted_class)
            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                print(error.info())
                print(error.read().decode("utf8", 'ignore'))

            if round(predicted_class,0)==0:
                    st.success("You are not credit worthy")
            else:
                    st.success("You are credit worthy")



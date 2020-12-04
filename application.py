from flask import Flask, render_template, url_for, request
from predictor_api import make_classification
import sqlalchemy as db
import pymysql


application = Flask(__name__)
application.debug=True

application.Secret_access_key="Pqsnm2fDrhRYHgCtoykcPGx0qABGmxCLHKlO3nm5"
application.Access_key_ID="AKIASAQV6PLTA2H7SHPD"

# An example of routing:
# If they go to the page "/" (this means a GET request
# to go to the page httP://127.0.0.1:5000/)

# GET method is the type of request your web browser will send the website
# When it accesses the URL of the web page
engine = db.create_engine('mysql+pymysql://team8user:gradhackteam8@hsbc-team8-data.ciavwhad0erl.us-east-2.rds.amazonaws.com:3306/hsbc_team8_data')
connection = engine.connect()
metadata = db.MetaData()
'''def connectioned():
    engine = db.create_engine('mysql+pymysql://team8user:gradhackteam8@hsbc-team8-data.ciavwhad0erl.us-east-2.rds.amazonaws.com:3306/hsbc_team8_data')
    connection = engine.connect()
    metadata = db.MetaData()
    ans = [engine,connection,metadata]
    return ans'''
        
        

def database_selection(x_input, category_prediction):
    global engine
    global connection
    global metadata

    print("insert into database")

    if(category_prediction=="Debt collection!"):
        data = "Debt_collection"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Loan!"):
        data = "Loan"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Credit card!"):
        data = "Credit_card"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Prepaid card!"):
        data = "Prepaid_card"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Credit reporting!"):
        data = "Credit_reporting"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Bank account or service!"):
        data = "Bank_account_service"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Mortgage!"):
        data =" Mortgage"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Checking or savings account!"):
        data = "Checking_savings_account"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    elif(category_prediction=="Money transfers!"):
        data = "Money_transfers"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)


    elif(category_prediction=="Other financial service!"):
        data = "Other_financial_service"
        temp = db.Table(data, metadata, autoload=True, autoload_with=engine)

    '''sql = "insert into "+data+" values('%s','%s')" %('hsbc100',x_input)
    cursor.execute(sql)
    db.commit()
    db.close()'''

    query = db.insert(temp).values(name="hsbc101",more_info=x_input) 
    ResultProxy = connection.execute(query)
    print("done")

@application.route("/")
def hello():
    return "It's alive!!!"


@application.route('/predict', methods=["GET", "POST"])
def predict():
    print(request.args)
    # This is a dictionary (JSON) object that contains 
    # the information submitted when someone clicks the ‘Submit’ button on our form.
    

    if (request.args):
        # request.args contains all the arguments passed by our form.
        # Comes built in with flask.
        # It is a dictionary of the form
        # "form name (as set in templatle)"
        # (key): "string in the textbox" (value)

        # by using request.args.get('chat_in'), it will take the 'name (key), "chat_in"' from the input button in the html file
        # and then it will take the associated value of "chat_in"
        x_input, category_prediction, list_of_pred_probs_dict = \
            make_classification(request.args.get('chat_in')) # if key doesn't exist, returns None

        print("a",category_prediction)
        print("b",x_input)

        database_selection(x_input,category_prediction)

        return render_template('predictor.html', x_input=x_input, 
                                                cat_prediction = category_prediction, 
                                                prediction = list_of_pred_probs_dict)
    
    else:
        # For the first load, request.args will be an 
        # empty ImmutableDict type
        # If this is the case we need to pass an empty string
        # into make_classification function so no errors are thrown.
        x_input, category_prediction, list_of_pred_probs_dict = make_classification('') 
        category_prediction = 'I think you are concerned about...'
        for dictionary in list_of_pred_probs_dict:
            for key, val in dictionary.items():
                dictionary[key] = '--'

        return render_template('predictor.html', x_input=x_input, 
                                                 cat_prediction=category_prediction, 
                                                 prediction = list_of_pred_probs_dict)


# Start the server, continuously listen to requests

if __name__ == '__main__':
    # For local development, set to True:
    application.run(host='0.0.0.0')

    # For public web serving:
    # app.run(host='0.0.0.0')
    # app.run()

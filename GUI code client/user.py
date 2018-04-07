from flask import Flask, render_template, redirect, url_for, request
import socket
import ssl
import random


ERROR = 'FAILED'
SUCCESS = 'SUCCESS'
LOGOUT = 1

host = '127.0.0.1'
port = 5500
sock = 0
usr = ''
pwd = ''

response_dict = {}
#customer_ID = 0
#----------------------------------------------------------------------------------
# Below two lines enables ssl
orig_sock = socket.socket()
# use SSL wrapped socket to connect to the server
sock = ssl.wrap_socket(orig_sock, ssl_version=ssl.PROTOCOL_TLSv1)
sock.connect((host,port))


app = Flask(__name__,template_folder="/Users/venkataponnaluri/Documents/CMPE-207/project_new/templates/")
app._static_folder = '/Users/venkataponnaluri/Documents/CMPE-207/project_new/static'
#app.debug = debug
    
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template("home.html")



 
@app.route('/login',methods=['GET','POST'])
def login():
   
    error = None
    if request.method == 'POST':
        
  
            # while True:
        if request.form['username'] != '' and request.form['password'] != '':
            usr = request.form['username']
            pwd = request.form['password']
            string_send = "LOGIN::username:"+str(usr)+"::password:"+str(pwd)
            print (string_send)

            sock.send(string_send)
            response = sock.recv(4096)
            print (response)
            res_list = response.split("::")
            
            for val in res_list[1:]:
                val_list = val.split(':')
                response_dict[val_list[0].rstrip()] = val_list[1].rstrip()
            print (response_dict)
            customer_ID = response_dict['client_id']
            if response_dict['client_type'] == 'Customer':
                return redirect(url_for('customer',customer_ID=customer_ID))
            elif response_dict['client_type'] == 'Teller':
                return redirect(url_for('teller',customer_ID=customer_ID))
            elif response_dict['client_type'] == 'Admin':
                return redirect(url_for('admin',customer_ID=customer_ID))
        else:
            error = "Invalid username or password! Please try again!"
            return render_template("login.html",error=error)
  
            
       
   
    return render_template("login.html",error=error)
        # usr = raw_input("Login Name: -> ")
        # pwd = raw_input("Password: -> ")

      
 
    #app.url_map.strict_slashes = False


@app.route('/customer',methods=['GET','POST'])
def customer():
    error=None
    customer_ID = request.args['customer_ID']

    if request.method == 'POST':
        choice = request.form['choice']
        print (request.form['choice'])
        
        
        if(request.form['choice'] == 'Logout'):
            return redirect(url_for('login'))
        else:
            return redirect(url_for("customeropt",choice=choice,customer_ID=customer_ID))
            
            #cst_user.display_customer_options(choice)
    return render_template("customer.html",error=error)

@app.route('/teller',methods=['GET','POST'])
def teller():
    error=None
    
    customer_ID = request.args['customer_ID']
    if request.method == 'POST':
        choice = request.form['choice']
        print (request.form['choice'])
        
        
        if(request.form['choice'] == 'Logout'):
            return redirect(url_for('login'))
        else:
            
            return redirect(url_for("telleropt",choice=choice,customer_ID=customer_ID))
            
            #cst_user.display_customer_options(choice)
    return render_template("teller.html",error=error)


@app.route('/admin',methods=['GET','POST'])
def admin():
    error=None
    
    customer_ID = request.args['customer_ID']
    if request.method == 'POST':
        choice = request.form['choice']
        print (request.form['choice'])
        
        
        if(request.form['choice'] == 'Logout'):
            return redirect(url_for('login'))
        else:
            
            return redirect(url_for("adminopt",choice=choice,customer_ID=customer_ID))
            
            #cst_user.display_customer_options(choice)
    return render_template("admin.html",error=error)
@app.route('/customeropt',methods=['GET','POST'])
def customeropt():
    error=None
    
    #print (request.args['messages'])
    choice = request.args['choice']
    customer_ID = request.args['customer_ID']
    #cst_user = Customer(usr,pwd,temp)
    #print (request.args['messages'])
    #if request.method == 'GET':
            #res_obj = cst_user.display_customer_options(choice)
            #print (res_obj)
    if choice == "Checking and Savings account":
    
        string_send = "GET::" +"client_type:Customer" +"::customer_id:"+ response_dict['client_id'] + "::subreq_type:CUSTOMER_ACCT"
        sock.send(string_send)
        response = sock.recv(4096)
        print (response)
        res_list = response.split("::")
    
        for val in res_list[1:]:
            val_list = val.split(':')
            response_dict[val_list[0].rstrip()] = val_list[1]
        print (response_dict)
    
        render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)

    elif choice == "Profile":
        
        string_send = "GET::" +"client_type:Customer" +"::customer_id:"+ response_dict['client_id'] + "::subreq_type:CUSTOMER_PROFILE"
        sock.send(string_send)
        response = sock.recv(4096)
        print (response)
        chk_acct_num = response_dict['chk_acct']

        res_list = response.split("::")
    
        for val in res_list[1:]:
            val_list = val.split(':')
            response_dict[val_list[0].rstrip()] = val_list[1]
        print (response_dict)
    
        render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)
    elif choice == "Transfer Funds":
        if request.method == "POST":

            if (request.form["checksave"] == "Checking"):
                acct_type = "chk_acct_num:"
                checksave = 'checking::'
            elif (request.form["checksave"] == "Saving"):
                acct_type = "sav_acct_num:"
                checksave = 'saving::'
            string_send = "SET::to_bank:" + str(request.form['bankname'])+"::subreq_type:TRANSFER_MONEY::"+acct_type+str(request.form['frombankaccountnumber'])+"::to_acct:"+str(request.form['tobankaccountnumber'])+"::client_type:Customer::op_type:SUBTRACT::acct_type:"+checksave+"customer_id:"+str(customer_ID)+"::amt:"+str(request.form['Amount'])
            sock.send(string_send)
            response = sock.recv(4096)
            print (response)
            #chk_acct_num = response_dict['chk_acct']

            res_list = response.split("::")
    
            for val in res_list[1:]:
                val_list = val.split(':')
                response_dict[val_list[0].rstrip()] = val_list[1]
            print (response_dict)
            if response_dict['status'] == 'SUCCESS':
                string_send = "GET::client_type:Customer::customer_id:"+ str(customer_ID) + "::subreq_type:CUSTOMER_ACCT"
                sock.send(string_send)
                response = sock.recv(4096)
                print (response)
            #chk_acct_num = response_dict['chk_acct']

                res_list = response.split("::")
    
                for val in res_list[1:]:
                    val_list = val.split(':')
                    response_dict[val_list[0].rstrip()] = val_list[1]
                print (response_dict)
                # render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)
    elif choice == "Monthly Statements":
                
            if (request.method == "POST"):
                customer_ID = str(request.form['Customer_ID'])
                string_send = "GET::client_type:Customer::customer_id:"+ customer_ID+ "::subreq_type:MONTHLY_STATEMENT"
                sock.send(string_send)
                response = sock.recv(4096)
                print (response)
                res_list = response.split("::")
    
                for val in res_list[1:]:
                    val_list = val.split(':')
                    response_dict[val_list[0].rstrip()] = val_list[1]
                print (response_dict)
            return render_template("customeropt.html",response_dict=response_dict,choice=choice,error=error)
    elif choice == "Withdraw":
        error = "==> Please approach the Teller for withdrawal"
        render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)
    elif choice == "Deposit":
        error = "==> Please approach the Teller for withdrawal"
        render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)
    else:
        error = "Failing in GET"


    return render_template("customeropt.html",choice=choice,response_dict=response_dict,error=error)


@app.route('/telleropt',methods=['GET','POST'])
def telleropt():
    error=None
    
    #print (request.args['messages'])
    choice = request.args['choice']
    teller_ID = request.args['customer_ID']
    transaction_dict = {}
    response_dict = {}
    #cst_user = Customer(usr,pwd,temp)
    #print (request.args['messages'])
    #if request.method == 'GET':
            #res_obj = cst_user.display_customer_options(choice)
            #print (res_obj)
    if choice == "Access Customer Account":
        if request.method == "POST":
            customer_ID = request.form['Customer_ID']
            string_send = "GET::client_type:Teller::customer_id:"+ str(customer_ID)+"::subreq_type:CUSTOMER_ACCT"
            sock.send(string_send)
            response = sock.recv(4096)
            print (response)
            res_list = response.split("::")
        
            for val in res_list[1:]:
                val_list = val.split(':')
                response_dict[val_list[0].rstrip()] = val_list[1]
            print (response_dict)
            string_send = "GET::client_type:Teller::customer_id:"+ str(customer_ID)+"::subreq_type:CUSTOMER_TRANSACTION"
            sock.send(string_send)
            response = sock.recv(4096)
            print (response)
            res_list = response.split("::")
        
            for val in res_list[1:]:
                val_list = val.split(':')
               
                    
                transaction_dict[val_list[0].rstrip()] = val_list[1]
            print (transaction_dict)
            chk_acct_num = response_dict['chk_acct']
            
            
        render_template("telleropt.html",choice=choice,response_dict=response_dict,transaction_dict=transaction_dict,error=error)
    elif choice == "Update Customer Account":
        if (request.method == "POST"):
                amount = str(request.form['Amount'])
                acct_num = request.form['tobankaccountnumber']
                customer_ID = str(request.form['Customer_ID'])
                print (request.form['withdep'])
                if request.form['withdep'] == "Withdraw":
                    op_type = "SUBTRACT"
                elif request.form['withdep'] == "Deposit":
                    op_type = "ADD"

                if (request.form["checksave"] == "Checking"):
                    acct_type = "chk_acct_num:"
                    checksave = 'checking::'
                    
                elif (request.form["checksave"] == "Saving"):
                    acct_type = "sav_acct_num:"
                    checksave = 'saving::'

                string_send = "SET::subreq_type:UPDATE_CHK_ACCT::"+acct_type+ str(acct_num)+"::client_type:Teller::op_type:"+op_type+"::customer_id:"+customer_ID+"::amt:"+amount
                sock.send(string_send)
                response = sock.recv(4096)
                print (response)
                res_list = response.split("::")
        
                for val in res_list[1:]:
                    val_list = val.split(':')
                    response_dict[val_list[0].rstrip()] = val_list[1]
                print (response_dict)
                if response_dict['status'] == "SUCCESS":
                    string_send = "GET::client_type:Teller::customer_id:"+customer_ID+"::subreq_type:CUSTOMER_ACCT"
                    sock.send(string_send)
                    response = sock.recv(4096)
                    print (response)
                    res_list = response.split("::")
        
                    for val in res_list[1:]:
                        val_list = val.split(':')
                        response_dict[val_list[0].rstrip()] = val_list[1]
                    print (response_dict)
        render_template("telleropt.html",choice=choice,response_dict=response_dict,transaction_dict=transaction_dict,error=error)
    elif choice == "Create Customer Account":
        if (request.method == "POST"):
            # for x in range(1000):
            #     cust_id = random.randint(1,1001)
            customer_ID = str(request.form['Customer_ID'])
            string_send = "INSERT::record_client_type:Customer::customer_id:"+ str(customer_ID)+"::client_type:Teller::subreq_type:INSERT_LOGIN_RECORD::password:"+request.form['password']+"::user_name:"+request.form['username']
            print (string_send)
            sock.send(string_send)
            response = sock.recv(4096)
            print (response)
            res_list = response.split("::")
        
            for val in res_list[1:]:
                val_list = val.split(':')
                response_dict[val_list[0].rstrip()] = val_list[1]
                print (response_dict)
            if response_dict['status'] == "SUCCESS":

                string_send = "INSERT::subreq_type:INSERT_ACCT_RECORD::customer_chk_bal:0::customer_sav_bal:0::customer_chk_acct:"+ request.form['checkacct']  +"::client_type:Teller::customer_sav_acct:"+request.form['savacct'] +"::customer_id:"+str(customer_ID)
                sock.send(string_send)
                response = sock.recv(4096)
                print (response)
                res_list = response.split("::")
        
                for val in res_list[1:]:
                    val_list = val.split(':')
                    response_dict[val_list[0].rstrip()] = val_list[1]
                    print (response_dict)
                    if response_dict['status'] == "SUCCESS":
                        string_send = "INSERT::city:"+request.form['City']+"::first_name:"+request.form['First_name']+"::last_name:"+request.form['Last_name']+"::DOB:"+ request.form['dob']+"::country:"+request.form['Country']+"::street_name:"+request.form['stnum']+"::zipcode:"+request.form['Zipcode']+"::phone:"+request.form['phnum']+"::state:"+request.form['State']+"::client_type:Teller::subreq_type:INSERT_PROFILE_RECORD::"+"gender:"+request.form['Gender']+"::customer_id:"+str(customer_ID)+"::email:"+request.form['Email']+"::apt_num:"+request.form['Aptnumber']
                        sock.send(string_send)
                        response = sock.recv(4096)
                        print (response)
                        res_list = response.split("::")
        
                        for val in res_list[1:]:
                            val_list = val.split(':')
                            response_dict[val_list[0].rstrip()] = val_list[1]
                        print (response_dict)
            return render_template("telleropt.html",choice=choice,error=error)
    elif choice == "Delete Customer Account":
                
                if (request.method == "POST"):
                    customer_ID = str(request.form['Customer_ID'])
                    string_send = "DELETE::client_type:Teller::customer_id:"+ customer_ID +"::subreq_type:DELETE_LOGIN_RECORD"
                    sock.send(string_send)
                    response = sock.recv(4096)
                    print (response)
                    res_list = response.split("::")
        
                    for val in res_list[1:]:
                        val_list = val.split(':')
                        response_dict[val_list[0].rstrip()] = val_list[1]
                    print (response_dict)
                return render_template("telleropt.html",choice=choice,error=error)
    else :
        error = "Failing in GET"


    return render_template("telleropt.html",choice=choice,response_dict=response_dict,transaction_dict=transaction_dict,error=error)

@app.route('/adminopt',methods=['GET','POST'])
def adminopt():
    error=None
    
    #print (request.args['messages'])
    choice = request.args['choice']
    admin_ID = request.args['customer_ID']
    transaction_dict = {}
    response_dict = {}
    #cst_user = Customer(usr,pwd,temp)
    #print (request.args['messages'])
    #if request.method == 'GET':
            #res_obj = cst_user.display_customer_options(choice)
    #         #print (res_obj)
    if choice == "View Tellers":
        string_send = "GET::client_type:Admin::subreq_type:ALL_TELLER_ID"
        sock.send(string_send)
        response = sock.recv(4096)
        print (response)
        res_list = response.split("::")
        
        for val in res_list[1:]:
            val_list = val.split(':')
            response_dict[val_list[0].rstrip()] = val_list[1]
        print (response_dict)
        return render_template("adminopt.html",choice=choice,response_dict=response_dict,error=error)
        
    # elif choice == "View Teller information":

    # elif choice == "View Transactions":
        
    # elif choice == "Delete Teller record":
                
    else :
        error = "Failing in GET"


    return render_template("adminopt.html",choice=choice,response_dict=response_dict,error=error)

######################### MAIN  #########################
def main(debug=False):

#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
    
   

  

    
  

    # send login credentials
    
    print"res_list ="
    print res_list

    sock.close()
    



if __name__ == "__main__":

    
    #app = main(debug=True)

    app.run(debug=True)
    #main(app)


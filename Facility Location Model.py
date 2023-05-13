## Facility Location Model

# Importing compress module to do some list operations from itertools package
from itertools import compress
## Importing pandas library to work with dataframes
import pandas as pd
## This particular library is use to get the geographical coordinates according to the input pincodes
import pgeocode
# Fixing the Location to India ('In') tog=fetch geographical coordinates
nomi = pgeocode.Nominatim('in')
# Using pickle to save and store the calculated distances between combinations of pincodes and hospitals locations provided
import pickle as cpickle
# To get all the combinations of any item passed in the product module
from itertools import product
# Square root function from math library
from math import sqrt
# Importing distance sub-module from geopy. distance function with in this submodule calculates the driving distances between two geographical coordinates
from geopy import distance
# For the pusrpose of solving the Mixed Integer LP problem, we import GRB module from gurobipy to check the status of the optimization run
from gurobipy import GRB
# We import gurobipy to help add LP constraints, declare the objective function and finally solve the problem
import gurobipy as gp
# We also import plt function from pyplot submodule of amtplotlib
import matplotlib.pyplot as plt

# To take the input from the suer, we use tkinter module to run desktop gui
from tkinter import *

# We also import ttk module to create buttons, windows and labels to display and capture the user input
from tkinter import ttk
# We also import filedialog module from tkinter 
from tkinter import filedialog


#Create an instance of Tkinter Frame, this is an object which will be used to call other functions to use later
win = Tk()

#Set the geometry, this denotes the size of the input window
win.geometry("700x250")

# Define a function to return the Input data. We name the function get_data, which takes no parameters as an input. We declare a global variable C which essentially save the user input.
def get_data():
    global C
    label.config(text= entry.get(), font= ('Helvetica 13'))
    C = entry.get()
    
# Create an Entry Widget, which is associated with the win object of the TK class from the tkinter library
entry = Entry(win, width= 42)
# We place/pack this entry widget at some relative x and y positions with respect to the label widget, and anchor it to the center of this label widget by passing in the needed parameters
entry.place(relx= .5, rely= .5, anchor= CENTER)

#We inititalize a Label widget, declare the font for it. And attach it to the win instance of the tkinter class TK
label= Label(win, text="", font=('Helvetica 13'))
# We then pack.place the widget on the screen in the best possible place adjudged by the tkinter module
label.pack()

#Create a Button to get the input data, with added instructions on how to input the two parameters that we have to pass in, after passing in the relative x-axis and y-axis positions 
ttk.Button(win, text= "Enter max distance and max hospitals separated by a comma", command= get_data).place(relx= .7, rely= .5, anchor= CENTER)

# We finally run the tkinter module and allied functions by calling mainloop function from the created win instance of the tkinter module.
win.mainloop()

global first_time_unoptimized
first_time_unoptimized = True

# This is where the post-processing of the user input begins. We begin by capturing the index of the "," used while inputting the input parameters.
index = C.index(",")
# Threshold will be the first input before comma, which denotes the maximum distance upto which a facility is allowed to serve radially. 
threshold = int(C[:index])
# n-hospitals is the second parameter that will be used by the function. We will use this as the budget parameter for the number of hospitals that can be made
n_hospitals = int(C[index+1:])


# We come to the main part where the implementation of the facility location model begins. We ask for the decisions to be made by the use on whether the user wants the precalculated distance matrix to run the code, or does the user want to use their own data or whether user wants to use the already populated excel sheets on the hospital locations and the customer/patient requirements assumed to be concentrated on the pincodes. 
decision = input("Enter 0 if you want to use precalculated distance matrix to run the code, Enter 1 if you wish to use the already pupulated file, enter 2 to input your own excel inputs ")

# All the imputs are string data types by default. So we will change this string data type to int datatype for further usage.
decision = int(decision)

# If the decison is 2, it means the user has decided to use their own data for the purpose of running this code. We check with the user if theu have put the data already in the input folder. If not, we prompt them to use the template as it will be generated if they choose that option. The code would stop from there and the user would have to run the code again and excercise the above steps again. They will have to follow the instructions the code would present to them again.  
if decision == 2 :

    # We check if the data is ready and is already present in the input folder to be used further by the code. 
    data_ready = input("Press 0 if the user input data is ready and present in the input folder, otherwise press 1. In the latter case you will have to rerun the code with populated files!")
    # We change the dstatype from string to int for this variable for future usage
    data_ready = int(data_ready)

    # If the data is not ready, we generate sample empty dataframes with column names listed.
    if data_ready == 1:
        # Generate pincode dataframe and export it as a csv file in the input folder. The user has to download it and use it as input when they are ready with the input data.
        sample_Pincode_csv_format = pd.DataFrame(columns = ['Pincode', 'District', 'StateName'])
        sample_Pincode_csv_format.to_csv(r"input\User_Pincode_File.csv")
        # Generate hospital dataframe and export it as an excel file and save it in the input folder. The 'Unnamed :0' column could be left empty as it will be dropped later and serves no use, but to maintain code reusability, it had to be included. The user has to download it and use it as input when they are ready with the input data.
        sample_Hospital_excel_format = pd.DataFrame(columns = ['Unnamed: 0', 'Districts', 'State', 'X1', 'X2', 'Cost'])
        sample_Hospital_excel_format.to_excel(r"input\User_Hospital_file.xlsx")
        
        print("\n\nThe excel template is ready in the input folder!")
        print("\n\nRerun the code with populated Excel and CSV files!!")
            
        # As the data is not ready in the current run of the code, the code ends here. THe user has to rerun the code again to get the solver to solve and make use of the input data they have provided. 

    elif data_ready == 0:

        # Now, in this next run, if the data is ready, we will declare the filename variables for both pincode and hospital datasets.
        filename1 = r"input\User_Pincode_File.csv"
        filename2 = r"input\User_Hospital_file.xlsx"

        # We begin by declaring the class named Facility Location for the data provided.

        class FacilityLocation:

            # We initialize the class with the parameters passed during the instance creation of this class.            
            def __init__(self, first_time_unoptimized= first_time_unoptimized, threshold = threshold, n_hospitals = n_hospitals, file_path = filename1, hospital_path = filename2 ):
                
                # And then we associate the parameters passed with the object of the class that will be created later
                self.first_time_unoptimized = first_time_unoptimized
                self.path = file_path
                self.hospital_path = hospital_path
                self.threshold = threshold
                self.n_hospitals = n_hospitals

            def algorithm(self):

                # We define the function named algorithm which will contain ways to pre-process the data for use, coordinates calculation, distance calculation between the hospitals and the pincode locations for the patients. This will also contain the methods to calculate the optimum facility location for the full coverage of the patient coordinates.
                # This will help load the passed csv file as a pandas dataframe.  
                all_codes = pd.read_csv(self.path)
                # Z will have the copy of the original dataframe in case we need it.
                z = all_codes.copy()
                # We store all the pincodes present in the user input file. We will later use it to find out the geographical coordinates as in latitudes and longitudes
                diff_pin = all_codes['Pincode']
                # We initialize empty lists as coordi, x1, and x2. x1 will store the latitude, x2 will store the longitudes and coordi will save the tuple combination of these two wihich will help in later calculations.
                coordi = []
                x1 = []
                x2 = []
                
                print("\n\n","Calculating geographical locations for the passed input file. Sit back, this may take a while!")
                # We iterate through the different pin codes, and pass the pincodes in the query_postal_code with nomi method which is fixed on India location. the 9th index value from the result will be contain the latitude and the 10th one will have the longitude for the same query 
                for pin in diff_pin:

                    x1.append(nomi.query_postal_code((pin))[9])
                    x2.append(nomi.query_postal_code((pin))[10])
                
                # We create Series datatype from the pandas library and convert the lists x1 and x2 as a list and append to the all_codes dataframe and give it the same index as the original dataframe
                all_codes['X1'] = pd.Series(x1, index = all_codes.index)
                all_codes['X2'] = pd.Series(x2, index = all_codes.index)

                print("\n\n Done appending the calculated Coordinates for the input file passed.")
                coordi = []

                # We iterate through all the rows of the all_codes dataframe to form a tuple datatype of the combination of latitudes and longitudes. We then append this tuple to the coordi list. We then save this coordi list as another column for the all_codes dataframe.
                for i in range(all_codes.shape[0]):
                    tup = (all_codes.loc[i,'X1'],all_codes.loc[i,'X2'])
                    coordi.append(tup)
                all_codes['Coordi'] = coordi
                
                # We drop all the na values from the dataframe and reset the index so that the serial number remains logical and continuous.

                all_codes.dropna(inplace=True)
                all_codes.reset_index(inplace =True)

                # We drop the 'index' column from the dataframe as it no longer serves any purpose now.
                all_codes.drop(['index'], inplace = True, axis = 1)
                 
                # we then load the hospital dataframe after reading the same from the passed hospital excel file. 
                all_district_hospitals= pd.read_excel(self.hospital_path)
                # We drop the 'unnamed: 0' column from the dataframe as this is of no use in the calculations later. We pass in the axis as 1 and replace it entirely from the dataframe.
                all_district_hospitals.drop('Unnamed: 0', axis = 1, inplace = True)
                # So that we can review the input hospital data, we print the all_district_hospitals
                print("\n\n", all_district_hospitals)

                # We create an empty customer list, it will later save the coordinates of all the district hospitals.  
                customer = []
                # We iterate through all the rows of the all_codes dataframe and append coordi column value to the customer list declared above.
                for i in range(all_codes.shape[0]):
                    customer.append(all_codes['Coordi'][i])

                # We declare the empty list as cost and the facilities that will store the cost to build the hospital.  
                cost = []
                facilities = []

                # We clean the district hospitals file and drop the na values from it and replace it entirely and then we reset the indices.
                all_district_hospitals.dropna(inplace = True)
                all_district_hospitals.reset_index(inplace=True)

                # We declare the empty list for coordinates and iterate through all the rows in the hospital dataframe to make a tuple of the coordinate locations and append it to the coordi list as shown below.
                coordis = []
                for i in range(all_district_hospitals.shape[0]):
                    tup = (all_district_hospitals.loc[i,'X1'],all_district_hospitals.loc[i,'X2'])
                    coordis.append(tup)

                # We set the cost per mile value as 5 for the problem at hand. Here it is hard coded into the model but it can later be changed to accomodate for any changes in the value later. 
                cost_per_mile = 5
                # We set the facilities value as the coordis from the previous last run lines.
                facilities = coordis
                
                # We declare the threshold value to be the maximum distance allowed between a suitable facility for each customer location.
                threshold = self.threshold
                
                # We declare a dist function to calculate the driving distance between the two passed locations. We extract the miles attribute from the returned value. This can be changed to kilometers for our purposes in the return value itself.
                def dist(loc1, loc2):
                    return distance.distance(tuple(loc1), tuple(loc2)).miles


                # We declare the empty dictionary pairings which will contain the indices of viable combinations of all hospitals and all pincodes between which the distance is lesser than the threshold distance passed as a parameter. All other combinations are discared and not stored in the dictioanry.
                pairings = {} 

                print("\n\n",f"Calculating the distance between each of the {len(facilities)*len(customer)} pairs of hospitals and patient locations")
                # We iterate through each of the customers and facilities available, find out the distance and compare the returned value with the threshold value passed as multiple key- value pair forlater use when defining the variable and constraints for our MIP problem.
                for cust in range(len(customer)):
                    for facility in range(len(facilities)) :
                        if  dist(customer[cust], facilities[facility]) < self.threshold:
                            try:
                                pairings[(facility,cust)] = dist(facilities[facility], customer[cust])
                #                 print(pairings[facility,customer])
                            except:
                                continue
                
                # We print out the number of viable pairings possible for the passed threshold value.
                print("\n\n Number of viable pairings: {0}".format(len(pairings.keys())))
            
                # We save the calculated pairing dictionary as a json readbale file for later use using the pickle module.
                with open(r"someobject1.pickle", "wb") as output_file:
                    cpickle.dump(pairings, output_file)
                
                # As the distances have already been calculated, we multiply each of these with the cost per mile as defined above. This gives the cost to transport from each of the faciliies to each of the pincodes 
                shipping_cost = {(f,c): cost_per_mile*pairings[(f,c)] for f, c in pairings.keys()}

                # We calculate the total number of the facilities and the customer locations.
                num_facilities = len(facilities)
                num_customers = len(customer)

                # We define an empty dictionary and store only those customer locations for which a viable facility is found.

                gg = []
                for f,c in pairings.keys():
                    gg.append(c)

                # In the empty list defined, we add the cost associated against each of the indices making in the pairings dictionary.
                for f,c in pairings.keys():
                    cost.append(all_district_hospitals.iloc[f,-1])
                
                # MIP  model formulation. We start with formulating the MILP model now. We add the constraints, define variables, their allowed type, upper and lower bounds and assign them a name.
                
                # We define a model m named facility_location using gurobi solver module.

                print("\n\nInitializing the facility location Gurobi model")
                m = gp.Model('facility_location')
                print("Defining model variables")
                # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')

                # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')

                print("Defining constraints for the model")
                # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                m.addConstrs((assign[facility, customer] <= select[facility]
                            for facility, customer in pairings.keys()),
                            name="Setup2ship")

                # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                m.addConstrs((assign.sum('*', customer) == 1
                            for customer in gg), name="Demand")
                
                # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                m.addConstr(select.sum() <= self.n_hospitals, name="Facility_limit1")

                # m.addConstr(select.sum() >= 10, name="Facility_limit2")
                print("\n\n Declaring the objective function for the MILP Model")
                # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                obj = gp.quicksum(cost_per_mile
                            *pairings[facility, cluster]
                            *assign[facility, cluster]
                            for facility, cluster in pairings.keys())  + select.prod(cost)
                # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                m.setObjective(obj, GRB.MINIMIZE)
                # We then make a function call to optimize the problem.
                print("\n\n Beginning optimizing the model")
                m.optimize()
            
                # Here we check the optimization status of the problem; if it's optimal for the parameters passed, it will create graphs and edges between the facilities and the customer if that particular customer serves that particular customer/patient location.
                
                global grb_status
                grb_status = m.SolCount

                print("\n\nThe number of solutions obtained: ",m.SolCount)

                if grb_status > 0:
                    
                    try:
                        assignments_file = {}
                        # We save the combination of the hospital and customer location for which the model makes an allocation.
                        assignments = [p for p in pairings if assign[p].x > 0.5]
                        # We define the parameters to plot the graph using the matplotlib module.
                        plt.figure(figsize=(8,8), dpi=150)
                        plt.scatter(*zip(*customer), c='Pink', s=0.5)
                        plt.scatter(*zip(*facilities), c='Green', s=1)
                        # assignments = [p for p in pairings if assign[p].x > 0.5]
                        
                        # We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                        for p in assignments:
                            pts = [facilities[p[0]], customer[p[1]]]
                            assignments_file[p] = (facilities[p[0]], customer[p[1]])
                            
                            plt.plot(*zip(*pts), c='Black', linewidth=0.1)
                        
                        # Save the assignments in the outputs folder as output_file.
                        assignments_file = pd.Series(assignments_file)
                        assignments_file.to_excel("output\outut_file.xlsx")
                        print("Hoorah!")
                        print("\n\n", f"The model is optimal with {n_hospitals} number of hospitals for {threshold} distance")
                
                    except:
                        print("\n\nThe solution count is 0")
                # Or else if the model is infeasible with given parameter set, we try to find the optimum number of hospitals
                
                else:
                    
                    print("\n\nThe model is infeasible with the choice of parameters.")
                    if self.first_time_unoptimized:
                        self.first_time_unoptimized = False
                        continue_optimization = input("\n\nThe model is infeasible, do you want to re-run the model with increased n_hospital parameter you provided? Enter 1 or 0 as a response. 1 indicates that you want to rerun the code")
                        print("\n\n",continue_optimization, type(continue_optimization))
                        if continue_optimization == "1":
                            self.n_hospitals += 1
                            while grb_status <= 0 and self.n_hospitals<= len(facilities):
                                
                                print(f"Trying to reoptimize again with {self.n_hospitals} number of hospitals")
                                m = gp.Model('facility_location')
                    
                                # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                                select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')
                                # assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
                                
                                # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                                assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')
                                # m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
                                
                                # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                                m.addConstrs((assign[facility, customer] <= select[facility]
                                            for facility, customer in pairings.keys()),
                                            name="Setup2ship")

                                # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                                m.addConstrs((assign.sum('*', customer) == 1
                                            for customer in gg), name="Demand")
                                # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                                m.addConstr(select.sum() <= self.n_hospitals, name="Facility_limit1")

                                # m.addConstr(select.sum() >= 10, name="Facility_limit2")

                                # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                                obj = gp.quicksum(cost_per_mile
                                            *pairings[facility, cluster]
                                            *assign[facility, cluster]
                                            for facility, cluster in pairings.keys())  + select.prod(cost)

                                # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                                m.setObjective(obj, GRB.MINIMIZE)
                                # We then make a function call to optimize the problem.
                                m.optimize()
                                self.n_hospitals += 1
                                grb_status = m.SolCount

                            if grb_status>0:
                                try:
                                    assignments_file = {}
                                    # We save the combination of the hospital and customer location for which the model makes an allocation.
                                    assignments = [p for p in pairings if assign[p].x > 0.5]
                                    # We define the parameters to plot the graph using the matplotlib module.
                                    plt.figure(figsize=(8,8), dpi=150)
                                    plt.scatter(*zip(*customer), c='Pink', s=0.5)
                                    plt.scatter(*zip(*facilities), c='Green', s=1)
                                    # assignments = [p for p in pairings if assign[p].x > 0.5]
                                    
                                    # We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                                    for p in assignments:
                                        pts = [facilities[p[0]], customer[p[1]]]
                                        assignments_file[p] = (facilities[p[0]], customer[p[1]])
                                        
                                        plt.plot(*zip(*pts), c='Black', linewidth=0.1)
                                    
                                    # Save the assignments in the outputs folder as output_file.
                                    assignments_file = pd.Series(assignments_file)
                                    assignments_file.to_excel("output\outut_file.xlsx")
                                    print("\n\n", f"The model is optimal with {self.n_hospitals} number of hospitals for {threshold} distance")
                            
                                except:
                                    print("\n\nThe solution count is 0")         

        op = FacilityLocation()
        op.algorithm()

        
        
elif decision == 1:

    # If the decision is 1, we proceed with the already populated excel file to optimize the network

    # We begin by declaring the class named Facility Location for the data provided.
    class FacilityLocation:
        def __init__(self,first_time_unoptimized = first_time_unoptimized, threshold = threshold, n_hospitals = n_hospitals):

            # We initialize the class with the parameters passed during the instance creation of this class.            
            self.path = "input\pincode-dataset.csv"
            # "C:\Users\Asus\MCLP folder\MTP Python Code\input\pincode-dataset.csv"
            self.hospital_path = "input\All District Hospitals.xlsx"
            self.threshold = threshold
            self.n_hospitals = n_hospitals
            self.first_time_unoptimized = first_time_unoptimized
        
            # We define the function named algorithm which will contain ways to pre-process the data for use, coordinates calculation, distance calculation between the hospitals and the pincode locations for the patients. This will also contain the methods to calculate the optimum facility location for the full coverage of the patient coordinates.
        
        def algorithm(self):

            # We start by defining the distinct states there are in the dataset to select for the states the user wants to run the code

            distinct_states = ['Delhi', 'Haryana', 'Sikkim', 'Punjab', 'Chandigarh',
       'Himachal Pradesh', 'Jammu and Kashmir', 'Uttar Pradesh',
       'Uttarakhand', 'Daman and Diu', 'Pondicherry', 'Rajasthan',
       'Gujarat', 'Dadra and Nagar Hav.', 'Maharashtra', 'Goa',
       'Madhya Pradesh', 'Chattisgarh', 'Telangana', 'Andhra Pradesh',
       'Karnataka', 'Tamil Nadu', 'Kerala', 'Lakshadweep', 'West Bengal',
       'Andaman and Nico.In.', 'Nagaland', 'Odisha', 'Assam',
       'Arunachal Pradesh', 'Megalaya', 'Manipur', 'Mizoram', 'Tripura',
       'Bihar', 'Jharkhand']

            # We help the user by printing the different states that are there so they can make a decision on the states to select
            print("\n\n", distinct_states)
            # We provide the instructions to the user on what to do next
            print("\n\n In the dialog box that will open now, please enter name of the states from the displayed states to be included in the model, separated by a comma (,)")
            
            # We now take the user input on the states
            states_to_be_included = input("Please enter your response!")
            # We then begin preprocessing the input received and change the datatyype from string to bool True and False
            states_to_be_included = list(states_to_be_included.split(","))
            

            # We then declare an empty list to append each of the included states in the data
            States = []
            States = states_to_be_included.copy()

            print("\n\n",f"You have selected {States} for this run")

            # This will help load the passed csv file as a pandas dataframe.  
            all_codes = pd.read_csv(self.path)
            
            # We create an empty dataframe to filter out the non selected sstates from the loaded dataframe
            all_codes_ = pd.DataFrame(columns = all_codes.columns)

            # We then append all the included states' data into this empty dataframe all_codes_
            for i in range(all_codes.shape[0]):
                if all_codes.iloc[i,-1]  in States :
                    all_codes_ = all_codes_.append(all_codes.iloc[i,:])
        
            # We then copy all of the data that is in all_codes_ to all_codes dataframe
            all_codes = all_codes_.copy()
            
            
            # z will have the copy of the original dataframe in case we need it.
            z = all_codes.copy()
            # We store all the pincodes present in the user input file. We will later use it to find out the geographical coordinates as in latitudes and longitudes
            diff_pin = all_codes['Pincode']
            
            # We initialize empty lists as coordi, x1, and x2. x1 will store the latitude, x2 will store the longitudes and coordi will save the tuple combination of these two wihich will help in later calculations.
            coordi = []
            x1 = []
            x2 = []
            
            print("\n\nCalculating the geographical locations for the states entered in the dialog box; this may take a while")
            # We iterate through the different pin codes, and pass the pincodes in the query_postal_code with nomi method which is fixed on India location. the 9th index value from the result will be contain the latitude and the 10th one will have the longitude for the same query 
            for pin in diff_pin:

                x1.append(nomi.query_postal_code((pin))[9])
                x2.append(nomi.query_postal_code((pin))[10])
            
            # We create Series datatype from the pandas library and convert the lists x1 and x2 as a list and append to the all_codes dataframe and give it the same index as the original dataframe
            all_codes['X1'] = pd.Series(x1, index = all_codes.index)
            all_codes['X2'] = pd.Series(x2, index = all_codes.index)
            coordi = []

            print("\n\nDone appending the coordinates in the dataframe!")
            print(all_codes.shape)
            all_codes.reset_index(inplace= True, drop=True)
            # We iterate through all the rows of the all_codes dataframe to form a tuple datatype of the combination of latitudes and longitudes. We then append this tuple to the coordi list. We then save this coordi list as another column for the all_codes dataframe.
            for i in range(all_codes.shape[0]):
                tup = (all_codes.loc[i,'X1'],all_codes.loc[i,'X2'])
                coordi.append(tup)
            
            print("\n\nStart appending the formed tuples to the dataframe")
            all_codes['Coordi'] = coordi
            print("\n\nDone appending the formed tuples to the dataframe")

            # We drop all the na values from the dataframe and reset the index so that the serial number remains logical and continuous.
            all_codes.dropna(inplace=True)
            all_codes.reset_index(inplace =True)

            # We drop the 'index' column from the dataframe as it no longer serves any purpose now.
            all_codes.drop(['index'], inplace = True, axis = 1)

            # we then load the hospital dataframe after reading the same from the passed hospital excel file. 
            all_district_hospitals= pd.read_excel(self.hospital_path)
            # We drop the 'index' column from the dataframe as it no longer serves any purpose now.
            all_district_hospitals.drop('Unnamed: 0', axis = 1, inplace = True)
            # So that we can review the input hospital data, we print the all_district_hospitals
            print("\n\n",all_district_hospitals)
            # We create an empty customer list, it will later save the coordinates of all the district hospitals.  
            customer = []
            for i in range(all_codes.shape[0]):
                customer.append(all_codes['Coordi'][i])
            
            # We declare the empty list as cost and the facilities that will store the cost to build the hospital.  
            cost = []
            facilities = []
            # We clean the district hospitals file and drop the na values from it and replace it entirely and then we reset the indices.
            all_district_hospitals.dropna(inplace = True)
            all_district_hospitals.reset_index(inplace=True)
            
            # We declare the empty list for coordinates and iterate through all the rows in the hospital dataframe to make a tuple of the coordinate locations and append it to the coordi list as shown below.
            coordis = []
            for i in range(all_district_hospitals.shape[0]):
                tup = (all_district_hospitals.loc[i,'X1'],all_district_hospitals.loc[i,'X2'])
                coordis.append(tup)
            # We set the cost per mile value as 5 for the problem at hand. Here it is hard coded into the model but it can later be changed to accomodate for any changes in the value later. 
            cost_per_mile = 5
            # We set the facilities value as the coordis from the previous last run lines.
            facilities = coordis
            # We declare the threshold value to be the maximum distance allowed between a suitable facility for each customer location.
            threshold = self.threshold
            

            # We declare a dist function to calculate the driving distance between the two passed locations. We extract the miles attribute from the returned value. This can be changed to kilometers for our purposes in the return value itself.
            def dist(loc1, loc2):
                return distance.distance(tuple(loc1), tuple(loc2)).miles

            # We declare the empty dictionary pairings which will contain the indices of viable combinations of all hospitals and all pincodes between which the distance is lesser than the threshold distance passed as a parameter. All other combinations are discared and not stored in the dictioanry.            
            pairings = {}

            print("\n\n",f"Calculating the distances for {len(customer)*len(facilities)} combinations of facilities and customer/patient location")
            # We iterate through each of the customers and facilities available, find out the distance and compare the returned value with the threshold value passed as multiple key- value pair forlater use when defining the variable and constraints for our MIP problem.
            for cust in range(len(customer)):
                for facility in range(len(facilities)) :
                    if  dist(customer[cust], facilities[facility]) < self.threshold:
                        try:
                            pairings[(facility,cust)] = dist(facilities[facility], customer[cust])
            #                 print(pairings[facility,customer])
                        except:
                            continue
            # We print out the number of viable pairings possible for the passed threshold value.
            print("\n\nNumber of viable pairings: {0}".format(len(pairings.keys())))
        
            # We save the calculated pairing dictionary as a json readbale file for later use using the pickle module.
            with open(r"someobject1.pickle", "wb") as output_file:
                cpickle.dump(pairings, output_file)
            
            # As the distances have already been calculated, we multiply each of these with the cost per mile as defined above. This gives the cost to transport from each of the faciliies to each of the pincodes 
            shipping_cost = {(f,c): cost_per_mile*pairings[(f,c)] for f, c in pairings.keys()}
            
            # We calculate the total number of the facilities and the customer locations.
            num_facilities = len(facilities)
            num_customers = len(customer)
            # We define an empty dictionary and store only those customer locations for which a viable facility is found.
            gg = []
            for f,c in pairings.keys():
                gg.append(c)

            # In the empty list defined, we add the cost associated against each of the indices making in the pairings dictionary.
            for f,c in pairings.keys():
                cost.append(all_district_hospitals.iloc[f,-1])
        
            
            # MIP  model formulation. We start with formulating the MILP model now. We add the constraints, define variables, their allowed type, upper and lower bounds and assign them a name.
                
            # We define a model m named facility_location using gurobi solver module.

            print("\n\nCreating the gurobi solver optimization model")
            m = gp.Model('facility_location')
            
            print("\n\nDeclaring Gurobi optimization variables")
            # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
            select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')
            # assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
            
            # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
            assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')
            # m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
            
            print("\n\n Adding Constraints")
            # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
            m.addConstrs((assign[facility, customer] <= select[facility]
                        for facility, customer in pairings.keys()),
                        name="Setup2ship")

            # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
            m.addConstrs((assign.sum('*', customer) == 1
                        for customer in gg), name="Demand")
            # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
            m.addConstr(select.sum() <= self.n_hospitals, name="Facility_limit1")

            # m.addConstr(select.sum() >= 10, name="Facility_limit2")

            # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
            
            print("\n\n Adding the objective function to the optimization model")
            obj = gp.quicksum(cost_per_mile
                        *pairings[facility, cluster]
                        *assign[facility, cluster]
                        for facility, cluster in pairings.keys())  + select.prod(cost)

            # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
            m.setObjective(obj, GRB.MINIMIZE)
            # We then make a function call to optimize the problem.
            print("Optimizing")
            m.optimize()
            
            # Here we check the optimization status of the problem; if it's optimal for the parameters passed, it will create graphs and edges between the facilities and the customer if that particular customer serves that particular customer/patient location.
            
            global grb_status
            grb_status = m.SolCount

            print("\n\nThe number of solutions obtained: ",m.SolCount)

            if grb_status > 0:
                
                try:
                    assignments_file = {}
                    # We save the combination of the hospital and customer location for which the model makes an allocation.
                    assignments = [p for p in pairings if assign[p].x > 0.5]
                    # We define the parameters to plot the graph using the matplotlib module.
                    plt.figure(figsize=(8,8), dpi=150)
                    plt.scatter(*zip(*customer), c='Pink', s=0.5)
                    plt.scatter(*zip(*facilities), c='Green', s=1)
                    # assignments = [p for p in pairings if assign[p].x > 0.5]
                    
                    # We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                    for p in assignments:
                        pts = [facilities[p[0]], customer[p[1]]]
                        assignments_file[p] = (facilities[p[0]], customer[p[1]])
                        
                        plt.plot(*zip(*pts), c='Black', linewidth=0.1)
                    
                    # Save the assignments in the outputs folder as output_file.
                    assignments_file = pd.Series(assignments_file)
                    assignments_file.to_excel("output\outut_file.xlsx")
                    print("\n\n", f"The model is optimal with {n_hospitals} number of hospitals for {threshold} distance")
            
                except:
                    print("\n\nThe solution count is 0")
            # Or else if the model is infeasible with given parameter set, we try to find the optimum number of hospitals
            
            else:
                
                print("\n\nThe model is infeasible with the choice of parameters.")
                if self.first_time_unoptimized:
                    self.first_time_unoptimized = False
                    continue_optimization = input("\n\nThe model is infeasible, do you want to re-run the model with increased n_hospital parameter you provided? Enter 1 or 0 as a response. 1 indicates that you want to rerun the code")
                    print("\n\n",continue_optimization, type(continue_optimization))
                    if continue_optimization == "1":
                        self.n_hospitals += 1
                        while grb_status <= 0 and self.n_hospitals<= len(facilities):
                            
                            print(f"Trying to reoptimize again with {self.n_hospitals} number of hospitals")
                            m = gp.Model('facility_location')
                
                            # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                            select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')
                            # assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
                            
                            # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                            assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')
                            # m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
                            
                            # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                            m.addConstrs((assign[facility, customer] <= select[facility]
                                        for facility, customer in pairings.keys()),
                                        name="Setup2ship")

                            # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                            m.addConstrs((assign.sum('*', customer) == 1
                                        for customer in gg), name="Demand")
                            # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                            m.addConstr(select.sum() <= self.n_hospitals, name="Facility_limit1")

                            # m.addConstr(select.sum() >= 10, name="Facility_limit2")

                            # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                            obj = gp.quicksum(cost_per_mile
                                        *pairings[facility, cluster]
                                        *assign[facility, cluster]
                                        for facility, cluster in pairings.keys())  + select.prod(cost)

                            # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                            m.setObjective(obj, GRB.MINIMIZE)
                            # We then make a function call to optimize the problem.
                            m.optimize()
                            self.n_hospitals += 1
                            grb_status = m.SolCount

                        if grb_status>0:
                            try:
                                assignments_file = {}
                                # We save the combination of the hospital and customer location for which the model makes an allocation.
                                assignments = [p for p in pairings if assign[p].x > 0.5]
                                # We define the parameters to plot the graph using the matplotlib module.
                                plt.figure(figsize=(8,8), dpi=150)
                                plt.scatter(*zip(*customer), c='Pink', s=0.5)
                                plt.scatter(*zip(*facilities), c='Green', s=1)
                                # assignments = [p for p in pairings if assign[p].x > 0.5]
                                
                                # We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                                for p in assignments:
                                    pts = [facilities[p[0]], customer[p[1]]]
                                    assignments_file[p] = (facilities[p[0]], customer[p[1]])
                                    
                                    plt.plot(*zip(*pts), c='Black', linewidth=0.1)
                                
                                # Save the assignments in the outputs folder as output_file.
                                assignments_file = pd.Series(assignments_file)
                                assignments_file.to_excel("output\outut_file.xlsx")
                                print("\n\n", f"The model is optimal with {self.n_hospitals} number of hospitals for {threshold} distance")
                        
                            except:
                                print("\n\nThe solution count is 0")         

    op = FacilityLocation()
    op.algorithm()
    
    


elif decision == 0:

    #We begin by reading the already populated csv file which contains the indices of the facilities and the location for which allocation has to be done. It also contains the distances as well as the cost to travel with a fixed cost of Rs 5 per mile 
    distance_matrix = pd.read_csv("input\Input__2.csv")
    # We declare the empty dictionary pairings which will contain the indices of viable combinations of all hospitals and all pincodes between which the distance is lesser than the threshold distance passed as a parameter. All other combinations are discared and not stored in the dictioanry.
    pairings = {}
    cost_per_mile = 5
    threshold = threshold
    # We filter out the rows for which the distance is larger than the passed thresholdvalue
    filtered_distance_matrix = distance_matrix[distance_matrix.loc[:,'0']<=threshold]
    # Reset the index of the input dataframe
    filtered_distance_matrix.reset_index(inplace=True, drop =True)
    
    # Create the pairings dictionaries as stated in above codes for different decisions
    for i in range(filtered_distance_matrix.shape[0]):
        pairings[(filtered_distance_matrix.loc[i,'level_0'],filtered_distance_matrix.loc[i,'level_1'])] = filtered_distance_matrix.iloc[i,-1]

    cost_per_mile = 5
    # As the distances have already been calculated, we multiply each of these with the cost per mile as defined above. This gives the cost to transport from each of the faciliies to each of the pincodes 
    shipping_cost = {(f,c): cost_per_mile*pairings[(f,c)] for f, c in pairings.keys()}
    
    # Create a list of facilities and the customers
    facilities = list(filtered_distance_matrix['level_0'].unique())
    customer = list(filtered_distance_matrix['level_1'].unique())

    # We calculate the total number of the facilities and the customer locations.
    num_facilities = (filtered_distance_matrix['level_0']).nunique()
    num_customers = (filtered_distance_matrix['level_1']).nunique()
    
    # We define an empty dictionary and store only those customer locations for which a viable facility is found.
    gg = []
    for f,c in pairings.keys():
        gg.append(c)
    

    # MIP  model formulation. We start with formulating the MILP model now. We add the constraints, define variables, their allowed type, upper and lower bounds and assign them a name.
                
    # We define a model m named facility_location using gurobi solver module.

    import gurobipy as gp
    from gurobipy import GRB
    m = gp.Model('facility_location')

    # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
    select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')

    # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
    assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')

    # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
    m.addConstrs((assign[facility, customer] <= select[facility]
                for facility, customer in pairings.keys()),
                name="Setup2ship")

    # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
    m.addConstrs((assign.sum('*', customer) == 1
                for customer in gg), name="Demand")
    # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
    m.addConstr(select.sum() <= n_hospitals, name="Facility_limit1")

    # m.addConstr(select.sum() >= 10, name="Facility_limit2")

    # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
    obj = gp.quicksum(cost_per_mile
                *pairings[facility, cluster]
                *assign[facility, cluster]
                for facility, cluster in pairings.keys())  
                # + select.prod(cost)
    # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.           
    m.setObjective(obj, GRB.MINIMIZE)
    # We then make a function call to optimize the problem.
    m.optimize()

    status = m.SolCount

    if status<=0:
        while status<=0:
            n_hospitals = n_hospitals + 1
            m = gp.Model('facility_location')

            # We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
            select = m.addVars(num_facilities, vtype=GRB.BINARY, name='select')

            # assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
            assign = m.addVars(pairings.keys(), vtype=GRB.BINARY, ub=1, name='assign')

            # We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
            m.addConstrs((assign[facility, customer] <= select[facility]
                        for facility, customer in pairings.keys()),
                        name="Setup2ship")

            # This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
            m.addConstrs((assign.sum('*', customer) == 1
                        for customer in gg), name="Demand")
            # We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
            m.addConstr(select.sum() <= n_hospitals, name="Facility_limit1")

            # m.addConstr(select.sum() >= 10, name="Facility_limit2")

            # We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
            obj = gp.quicksum(cost_per_mile
                        *pairings[facility, cluster]
                        *assign[facility, cluster]
                        for facility, cluster in pairings.keys())  
                        # + select.prod(cost)
            # Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.           
            m.setObjective(obj, GRB.MINIMIZE)
            # We then make a function call to optimize the problem.
            m.optimize()
            status = m.SolCount
        
        print("\n\n",f"The given model could be optimized with {n_hospitals} number of hospitals for {threshold} distance passed earlier!")


    
    # if GRB.OPTIMAL == 2:
                
    #     assignments = [p for p in pairings if assign[p].x > 0.5]
    #     plt.figure(figsize=(8,8), dpi=150)
    #     plt.scatter(*zip(*customer), c='Pink', s=0.5)
    #     plt.scatter(*zip(*facilities), c='Green', s=1)
    #     # assignments = [p for p in pairings if assign[p].x > 0.5]
    #     for p in assignments:
    #         pts = [facilities[p[0]], customer[p[1]]]
    #         plt.plot(*zip(*pts), c='Black', linewidth=0.1)
            
    # elif GRB.OPTIMAL == 1:
    #     print("The model is infeasible with the choice of parameters.")
    



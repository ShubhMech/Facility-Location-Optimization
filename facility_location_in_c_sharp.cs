namespace Namespace {
    
    using compress = itertools.compress;
    
    using pd = pandas;
    
    using pgeocode;
    
    using cpickle = pickle;
    
    using product = itertools.product;
    
    using sqrt = math.sqrt;
    
    using distance = geopy.distance;
    
    using GRB = gurobipy.GRB;
    
    using gp = gurobipy;
    
    using plt = matplotlib.pyplot;
    
    using ttk = tkinter.ttk;
    
    using filedialog = tkinter.filedialog;
    
    using System;
    
    using System.Collections.Generic;
    
    using System.Linq;
    
    using gp = gurobipy;
    
    using GRB = gurobipy.GRB;
    
    public static class Module {
        
        public static object nomi = pgeocode.Nominatim("in");
        
        public static object win = Tk();
        
        static Module() {
            win.geometry("700x250");
            entry.place(relx: 0.5, rely: 0.5, anchor: CENTER);
            label.pack();
            ttk.Button(win, text: "Enter max distance and max hospitals separated by a comma", command: get_data).place(relx: 0.7, rely: 0.5, anchor: CENTER);
            win.mainloop();
            sample_Pincode_csv_format.to_csv(@"input\User_Pincode_File.csv");
            sample_Hospital_excel_format.to_excel(@"input\User_Hospital_file.xlsx");
            op.algorithm();
            op.algorithm();
            filtered_distance_matrix.reset_index(inplace: true, drop: true);
            pairings[(filtered_distance_matrix.loc[i,"level_0"], filtered_distance_matrix.loc[i,"level_1"])] = filtered_distance_matrix.iloc[i,-1];
            gg.append(c);
            m.addConstrs(from _tup_5 in pairings.keys().Chop((facility,customer) => (facility, customer))
                let facility = _tup_5.Item1
                let customer = _tup_5.Item2
                select assign[facility,customer] <= select[facility], name: "Setup2ship");
            m.addConstrs(from customer in gg
                select assign.sum("*", customer) == 1, name: "Demand");
            m.addConstr(select.sum() <= n_hospitals, name: "Facility_limit1");
            m.setObjective(obj, GRB.MINIMIZE);
            m.optimize();
            m.addConstrs(from _tup_9 in pairings.keys().Chop((facility,customer) => (facility, customer))
                let facility = _tup_9.Item1
                let customer = _tup_9.Item2
                select assign[facility,customer] <= select[facility], name: "Setup2ship");
            m.addConstrs(from customer in gg
                select assign.sum("*", customer) == 1, name: "Demand");
            m.addConstr(select.sum() <= n_hospitals, name: "Facility_limit1");
            m.setObjective(obj, GRB.MINIMIZE);
            m.optimize();
        }
        
        //Set the geometry, this denotes the size of the input window
        // Define a function to return the Input data. We name the function get_data, which takes no parameters as an input. We declare a global variable C which essentially save the user input.
        public static object get_data() {
            label.config(text: entry.get(), font: "Helvetica 13");
            C = entry.get();
        }
        
        public static object entry = Entry(win, width: 42);
        
        public static object label = Label(win, text: "", font: "Helvetica 13");
        
        public static object first_time_unoptimized = true;
        
        public static object index = C.index(",");
        
        public static object threshold = Convert.ToInt32(C[::index]);
        
        public static object n_hospitals = Convert.ToInt32(C[index + 1]);
        
        public static object decision = input("Enter 0 if you want to use precalculated distance matrix to run the code, Enter 1 if you wish to use the already pupulated file, enter 2 to input your own excel inputs ");
        
        public static object decision = Convert.ToInt32(decision);
        
        public static object data_ready = input("Press 0 if the user input data is ready and present in the input folder, otherwise press 1. In the latter case you will have to rerun the code with populated files!");
        
        public static object data_ready = Convert.ToInt32(data_ready);
        
        public static object sample_Pincode_csv_format = pd.DataFrame(columns: new List<object> {
            "Pincode",
            "District",
            "StateName"
        });
        
        public static object sample_Hospital_excel_format = pd.DataFrame(columns: new List<object> {
            "Unnamed: 0",
            "Districts",
            "State",
            "X1",
            "X2",
            "Cost"
        });
        
        public static object filename1 = @"input\User_Pincode_File.csv";
        
        public static object filename2 = @"input\User_Hospital_file.xlsx";
        
        public class FacilityLocation {
            
            public FacilityLocation(
                object first_time_unoptimized = first_time_unoptimized,
                object threshold = threshold,
                object n_hospitals = n_hospitals,
                object file_path = filename1,
                object hospital_path = filename2) {
                // And then we associate the parameters passed with the object of the class that will be created later
                this.first_time_unoptimized = first_time_unoptimized;
                this.path = file_path;
                this.hospital_path = hospital_path;
                this.threshold = threshold;
                this.n_hospitals = n_hospitals;
            }
            
            public virtual object algorithm() {
                object pts;
                object assignments;
                object assignments_file;
                object c;
                object f;
                object tup;
                // We define the function named algorithm which will contain ways to pre-process the data for use, coordinates calculation, distance calculation between the hospitals and the pincode locations for the patients. This will also contain the methods to calculate the optimum facility location for the full coverage of the patient coordinates.
                // This will help load the passed csv file as a pandas dataframe.  
                var all_codes = pd.read_csv(this.path);
                // Z will have the copy of the original dataframe in case we need it.
                var z = all_codes.copy();
                // We store all the pincodes present in the user input file. We will later use it to find out the geographical coordinates as in latitudes and longitudes
                var diff_pin = all_codes["Pincode"];
                // We initialize empty lists as coordi, x1, and x2. x1 will store the latitude, x2 will store the longitudes and coordi will save the tuple combination of these two wihich will help in later calculations.
                var coordi = new List<object>();
                var x1 = new List<object>();
                var x2 = new List<object>();
                Console.WriteLine("\n\n", "Calculating geographical locations for the passed input file. Sit back, this may take a while!");
                // We iterate through the different pin codes, and pass the pincodes in the query_postal_code with nomi method which is fixed on India location. the 9th index value from the result will be contain the latitude and the 10th one will have the longitude for the same query 
                foreach (var pin in diff_pin) {
                    x1.append(nomi.query_postal_code(pin)[9]);
                    x2.append(nomi.query_postal_code(pin)[10]);
                }
                // We create Series datatype from the pandas library and convert the lists x1 and x2 as a list and append to the all_codes dataframe and give it the same index as the original dataframe
                all_codes["X1"] = pd.Series(x1, index: all_codes.index);
                all_codes["X2"] = pd.Series(x2, index: all_codes.index);
                Console.WriteLine("\n\n Done appending the calculated Coordinates for the input file passed.");
                coordi = new List<object>();
                // We iterate through all the rows of the all_codes dataframe to form a tuple datatype of the combination of latitudes and longitudes. We then append this tuple to the coordi list. We then save this coordi list as another column for the all_codes dataframe.
                foreach (var i in Enumerable.Range(0, all_codes.shape[0])) {
                    tup = (all_codes.loc[i,"X1"], all_codes.loc[i,"X2"]);
                    coordi.append(tup);
                }
                all_codes["Coordi"] = coordi;
                // We drop all the na values from the dataframe and reset the index so that the serial number remains logical and continuous.
                all_codes.dropna(inplace: true);
                all_codes.reset_index(inplace: true);
                // We drop the 'index' column from the dataframe as it no longer serves any purpose now.
                all_codes.drop(new List<object> {
                    "index"
                }, inplace: true, axis: 1);
                // we then load the hospital dataframe after reading the same from the passed hospital excel file. 
                var all_district_hospitals = pd.read_excel(this.hospital_path);
                // We drop the 'unnamed: 0' column from the dataframe as this is of no use in the calculations later. We pass in the axis as 1 and replace it entirely from the dataframe.
                all_district_hospitals.drop("Unnamed: 0", axis: 1, inplace: true);
                // So that we can review the input hospital data, we print the all_district_hospitals
                Console.WriteLine("\n\n", all_district_hospitals);
                // We create an empty customer list, it will later save the coordinates of all the district hospitals.  
                var customer = new List<object>();
                // We iterate through all the rows of the all_codes dataframe and append coordi column value to the customer list declared above.
                foreach (var i in Enumerable.Range(0, all_codes.shape[0])) {
                    customer.append(all_codes["Coordi"][i]);
                }
                // We declare the empty list as cost and the facilities that will store the cost to build the hospital.  
                var cost = new List<object>();
                var facilities = new List<object>();
                // We clean the district hospitals file and drop the na values from it and replace it entirely and then we reset the indices.
                all_district_hospitals.dropna(inplace: true);
                all_district_hospitals.reset_index(inplace: true);
                // We declare the empty list for coordinates and iterate through all the rows in the hospital dataframe to make a tuple of the coordinate locations and append it to the coordi list as shown below.
                var coordis = new List<object>();
                foreach (var i in Enumerable.Range(0, all_district_hospitals.shape[0])) {
                    tup = (all_district_hospitals.loc[i,"X1"], all_district_hospitals.loc[i,"X2"]);
                    coordis.append(tup);
                }
                // We set the cost per mile value as 5 for the problem at hand. Here it is hard coded into the model but it can later be changed to accomodate for any changes in the value later. 
                var cost_per_mile = 5;
                // We set the facilities value as the coordis from the previous last run lines.
                facilities = coordis;
                // We declare the threshold value to be the maximum distance allowed between a suitable facility for each customer location.
                var threshold = this.threshold;
                // We declare a dist function to calculate the driving distance between the two passed locations. We extract the miles attribute from the returned value. This can be changed to kilometers for our purposes in the return value itself.
                Func<object, object, object> dist = (loc1,loc2) => {
                    return distance.distance(tuple(loc1), tuple(loc2)).miles;
                };
                // We declare the empty dictionary pairings which will contain the indices of viable combinations of all hospitals and all pincodes between which the distance is lesser than the threshold distance passed as a parameter. All other combinations are discared and not stored in the dictioanry.
                var pairings = new Dictionary<object, object> {
                };
                Console.WriteLine("\n\n", "Calculating the distance between each of the {len(facilities)*len(customer)} pairs of hospitals and patient locations");
                // We iterate through each of the customers and facilities available, find out the distance and compare the returned value with the threshold value passed as multiple key- value pair forlater use when defining the variable and constraints for our MIP problem.
                foreach (var cust in Enumerable.Range(0, customer.Count)) {
                    foreach (var facility in Enumerable.Range(0, facilities.Count)) {
                        if (dist(customer[cust], facilities[facility]) < this.threshold) {
                            try {
                                pairings[(facility, cust)] = dist(facilities[facility], customer[cust]);
                                //                 print(pairings[facility,customer])
                            } catch {
                                continue;
                            }
                        }
                    }
                }
                // We print out the number of viable pairings possible for the passed threshold value.
                Console.WriteLine("\n\n Number of viable pairings: {0}".format(pairings.keys().Count));
                // We save the calculated pairing dictionary as a json readbale file for later use using the pickle module.
                using (var output_file = open(@"someobject1.pickle", "wb")) {
                    cpickle.dump(pairings, output_file);
                }
                // As the distances have already been calculated, we multiply each of these with the cost per mile as defined above. This gives the cost to transport from each of the faciliies to each of the pincodes 
                var shipping_cost = pairings.keys().ToDictionary(_tup_1 => (_tup_1.Item1, _tup_1.Item2), _tup_1 => cost_per_mile * pairings[(_tup_1.Item1, _tup_1.Item2)]);
                // We calculate the total number of the facilities and the customer locations.
                var num_facilities = facilities.Count;
                var num_customers = customer.Count;
                // We define an empty dictionary and store only those customer locations for which a viable facility is found.
                var gg = new List<object>();
                foreach (var _tup_2 in pairings.keys()) {
                    f = _tup_2.Item1;
                    c = _tup_2.Item2;
                    gg.append(c);
                }
                // In the empty list defined, we add the cost associated against each of the indices making in the pairings dictionary.
                foreach (var _tup_3 in pairings.keys()) {
                    f = _tup_3.Item1;
                    c = _tup_3.Item2;
                    cost.append(all_district_hospitals.iloc[f,-1]);
                }
                // MIP  model formulation. We start with formulating the MILP model now. We add the constraints, define variables, their allowed type, upper and lower bounds and assign them a name.
                // We define a model m named facility_location using gurobi solver module.
                Console.WriteLine("\n\nInitializing the facility location Gurobi model");
                var m = gp.Model("facility_location");
                Console.WriteLine("Defining model variables");
                // We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                var select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
                // assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                var assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
                Console.WriteLine("Defining constraints for the model");
                // We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                m.addConstrs(from _tup_4 in pairings.keys().Chop((facility,customer) => (facility, customer))
                    let facility = _tup_4.Item1
                    let customer = _tup_4.Item2
                    select assign[facility,customer] <= select[facility], name: "Setup2ship");
                // This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                m.addConstrs(from customer in gg
                    select assign.sum("*", customer) == 1, name: "Demand");
                // We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                m.addConstr(select.sum() <= this.n_hospitals, name: "Facility_limit1");
                // m.addConstr(select.sum() >= 10, name="Facility_limit2")
                Console.WriteLine("\n\n Declaring the objective function for the MILP Model");
                // We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                var obj = gp.quicksum(from _tup_5 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
                    let facility = _tup_5.Item1
                    let cluster = _tup_5.Item2
                    select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]) + select.prod(cost);
                // Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                m.setObjective(obj, GRB.MINIMIZE);
                // We then make a function call to optimize the problem.
                Console.WriteLine("\n\n Beginning optimizing the model");
                m.optimize();
                // Here we check the optimization status of the problem; if it's optimal for the parameters passed, it will create graphs and edges between the facilities and the customer if that particular customer serves that particular customer/patient location.
                grb_status = m.SolCount;
                Console.WriteLine("\n\nThe number of solutions obtained: ", m.SolCount);
                if (grb_status > 0) {
                    try {
                        assignments_file = new Dictionary<object, object> {
                        };
                        // We save the combination of the hospital and customer location for which the model makes an allocation.
                        assignments = (from p in pairings
                            where assign[p].x > 0.5
                            select p).ToList();
                        // We define the parameters to plot the graph using the matplotlib module.
                        plt.figure(figsize: (8, 8), dpi: 150);
                        plt.scatter(c: "Pink", s: 0.5, zip(customer));
                        plt.scatter(c: "Green", s: 1, zip(facilities));
                        // assignments = [p for p in pairings if assign[p].x > 0.5]
                        // We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                        foreach (var p in assignments) {
                            pts = new List<object> {
                                facilities[p[0]],
                                customer[p[1]]
                            };
                            assignments_file[p] = (facilities[p[0]], customer[p[1]]);
                            plt.plot(c: "Black", linewidth: 0.1, zip(pts));
                        }
                        // Save the assignments in the outputs folder as output_file.
                        assignments_file = pd.Series(assignments_file);
                        assignments_file.to_excel("output\outut_file.xlsx");
                        Console.WriteLine("Hoorah!");
                        Console.WriteLine("\n\n", "The model is optimal with {n_hospitals} number of hospitals for {threshold} distance");
                    } catch {
                        Console.WriteLine("\n\nThe solution count is 0");
                    }
                } else {
                    // Or else if the model is infeasible with given parameter set, we try to find the optimum number of hospitals
                    Console.WriteLine("\n\nThe model is infeasible with the choice of parameters.");
                    if (this.first_time_unoptimized) {
                        this.first_time_unoptimized = false;
                        var continue_optimization = input("\n\nThe model is infeasible, do you want to re-run the model with increased n_hospital parameter you provided? Enter 1 or 0 as a response. 1 indicates that you want to rerun the code");
                        Console.WriteLine("\n\n", continue_optimization, type(continue_optimization));
                        if (continue_optimization == "1") {
                            this.n_hospitals += 1;
                            while (grb_status <= 0 && this.n_hospitals <= facilities.Count) {
                                Console.WriteLine("Trying to reoptimize again with {self.n_hospitals} number of hospitals");
                                m = gp.Model("facility_location");
                                // We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                                select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
                                // assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
                                // assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                                assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
                                // m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
                                // We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                                m.addConstrs(from _tup_6 in pairings.keys().Chop((facility,customer) => (facility, customer))
                                    let facility = _tup_6.Item1
                                    let customer = _tup_6.Item2
                                    select assign[facility,customer] <= select[facility], name: "Setup2ship");
                                // This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                                m.addConstrs(from customer in gg
                                    select assign.sum("*", customer) == 1, name: "Demand");
                                // We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                                m.addConstr(select.sum() <= this.n_hospitals, name: "Facility_limit1");
                                // m.addConstr(select.sum() >= 10, name="Facility_limit2")
                                // We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                                obj = gp.quicksum(from _tup_7 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
                                    let facility = _tup_7.Item1
                                    let cluster = _tup_7.Item2
                                    select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]) + select.prod(cost);
                                // Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                                m.setObjective(obj, GRB.MINIMIZE);
                                // We then make a function call to optimize the problem.
                                m.optimize();
                                this.n_hospitals += 1;
                                grb_status = m.SolCount;
                            }
                            if (grb_status > 0) {
                                try {
                                    assignments_file = new Dictionary<object, object> {
                                    };
                                    // We save the combination of the hospital and customer location for which the model makes an allocation.
                                    assignments = (from p in pairings
                                        where assign[p].x > 0.5
                                        select p).ToList();
                                    // We define the parameters to plot the graph using the matplotlib module.
                                    plt.figure(figsize: (8, 8), dpi: 150);
                                    plt.scatter(c: "Pink", s: 0.5, zip(customer));
                                    plt.scatter(c: "Green", s: 1, zip(facilities));
                                    // assignments = [p for p in pairings if assign[p].x > 0.5]
                                    // We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                                    foreach (var p in assignments) {
                                        pts = new List<object> {
                                            facilities[p[0]],
                                            customer[p[1]]
                                        };
                                        assignments_file[p] = (facilities[p[0]], customer[p[1]]);
                                        plt.plot(c: "Black", linewidth: 0.1, zip(pts));
                                    }
                                    // Save the assignments in the outputs folder as output_file.
                                    assignments_file = pd.Series(assignments_file);
                                    assignments_file.to_excel("output\outut_file.xlsx");
                                    Console.WriteLine("\n\n", "The model is optimal with {self.n_hospitals} number of hospitals for {threshold} distance");
                                } catch {
                                    Console.WriteLine("\n\nThe solution count is 0");
                                }
                            }
                        }
                    }
                }
            }
        }
        
        public static object op = FacilityLocation();
        
        public class FacilityLocation {
            
            public FacilityLocation(object first_time_unoptimized = first_time_unoptimized, object threshold = threshold, object n_hospitals = n_hospitals) {
                // We initialize the class with the parameters passed during the instance creation of this class.            
                this.path = "input\pincode-dataset.csv";
                // "C:\Users\Asus\MCLP folder\MTP Python Code\input\pincode-dataset.csv"
                this.hospital_path = "input\All District Hospitals.xlsx";
                this.threshold = threshold;
                this.n_hospitals = n_hospitals;
                this.first_time_unoptimized = first_time_unoptimized;
                // We define the function named algorithm which will contain ways to pre-process the data for use, coordinates calculation, distance calculation between the hospitals and the pincode locations for the patients. This will also contain the methods to calculate the optimum facility location for the full coverage of the patient coordinates.
            }
            
            public virtual object algorithm() {
                object pts;
                object assignments;
                object assignments_file;
                object c;
                object f;
                object tup;
                // We start by defining the distinct states there are in the dataset to select for the states the user wants to run the code
                var distinct_states = new List<object> {
                    "Delhi",
                    "Haryana",
                    "Sikkim",
                    "Punjab",
                    "Chandigarh",
                    "Himachal Pradesh",
                    "Jammu and Kashmir",
                    "Uttar Pradesh",
                    "Uttarakhand",
                    "Daman and Diu",
                    "Pondicherry",
                    "Rajasthan",
                    "Gujarat",
                    "Dadra and Nagar Hav.",
                    "Maharashtra",
                    "Goa",
                    "Madhya Pradesh",
                    "Chattisgarh",
                    "Telangana",
                    "Andhra Pradesh",
                    "Karnataka",
                    "Tamil Nadu",
                    "Kerala",
                    "Lakshadweep",
                    "West Bengal",
                    "Andaman and Nico.In.",
                    "Nagaland",
                    "Odisha",
                    "Assam",
                    "Arunachal Pradesh",
                    "Megalaya",
                    "Manipur",
                    "Mizoram",
                    "Tripura",
                    "Bihar",
                    "Jharkhand"
                };
                // We help the user by printing the different states that are there so they can make a decision on the states to select
                Console.WriteLine("\n\n", distinct_states);
                // We provide the instructions to the user on what to do next
                Console.WriteLine("\n\n In the dialog box that will open now, please enter name of the states from the displayed states to be included in the model, separated by a comma (,)");
                // We now take the user input on the states
                var states_to_be_included = input("Please enter your response!");
                // We then begin preprocessing the input received and change the datatyype from string to bool True and False
                states_to_be_included = states_to_be_included.split(",").ToList();
                // We then declare an empty list to append each of the included states in the data
                var States = new List<object>();
                States = states_to_be_included.copy();
                Console.WriteLine("\n\n", "You have selected {States} for this run");
                // This will help load the passed csv file as a pandas dataframe.  
                var all_codes = pd.read_csv(this.path);
                // We create an empty dataframe to filter out the non selected sstates from the loaded dataframe
                var all_codes_ = pd.DataFrame(columns: all_codes.columns);
                // We then append all the included states' data into this empty dataframe all_codes_
                foreach (var i in Enumerable.Range(0, all_codes.shape[0])) {
                    if (States.Contains(all_codes.iloc[i,-1])) {
                        all_codes_ = all_codes_.append(all_codes.iloc[i,":"]);
                    }
                }
                // We then copy all of the data that is in all_codes_ to all_codes dataframe
                all_codes = all_codes_.copy();
                // z will have the copy of the original dataframe in case we need it.
                var z = all_codes.copy();
                // We store all the pincodes present in the user input file. We will later use it to find out the geographical coordinates as in latitudes and longitudes
                var diff_pin = all_codes["Pincode"];
                // We initialize empty lists as coordi, x1, and x2. x1 will store the latitude, x2 will store the longitudes and coordi will save the tuple combination of these two wihich will help in later calculations.
                var coordi = new List<object>();
                var x1 = new List<object>();
                var x2 = new List<object>();
                Console.WriteLine("\n\nCalculating the geographical locations for the states entered in the dialog box; this may take a while");
                // We iterate through the different pin codes, and pass the pincodes in the query_postal_code with nomi method which is fixed on India location. the 9th index value from the result will be contain the latitude and the 10th one will have the longitude for the same query 
                foreach (var pin in diff_pin) {
                    x1.append(nomi.query_postal_code(pin)[9]);
                    x2.append(nomi.query_postal_code(pin)[10]);
                }
                // We create Series datatype from the pandas library and convert the lists x1 and x2 as a list and append to the all_codes dataframe and give it the same index as the original dataframe
                all_codes["X1"] = pd.Series(x1, index: all_codes.index);
                all_codes["X2"] = pd.Series(x2, index: all_codes.index);
                coordi = new List<object>();
                Console.WriteLine("\n\nDone appending the coordinates in the dataframe!");
                Console.WriteLine(all_codes.shape);
                all_codes.reset_index(inplace: true, drop: true);
                // We iterate through all the rows of the all_codes dataframe to form a tuple datatype of the combination of latitudes and longitudes. We then append this tuple to the coordi list. We then save this coordi list as another column for the all_codes dataframe.
                foreach (var i in Enumerable.Range(0, all_codes.shape[0])) {
                    tup = (all_codes.loc[i,"X1"], all_codes.loc[i,"X2"]);
                    coordi.append(tup);
                }
                Console.WriteLine("\n\nStart appending the formed tuples to the dataframe");
                all_codes["Coordi"] = coordi;
                Console.WriteLine("\n\nDone appending the formed tuples to the dataframe");
                // We drop all the na values from the dataframe and reset the index so that the serial number remains logical and continuous.
                all_codes.dropna(inplace: true);
                all_codes.reset_index(inplace: true);
                // We drop the 'index' column from the dataframe as it no longer serves any purpose now.
                all_codes.drop(new List<object> {
                    "index"
                }, inplace: true, axis: 1);
                // we then load the hospital dataframe after reading the same from the passed hospital excel file. 
                var all_district_hospitals = pd.read_excel(this.hospital_path);
                // We drop the 'index' column from the dataframe as it no longer serves any purpose now.
                all_district_hospitals.drop("Unnamed: 0", axis: 1, inplace: true);
                // So that we can review the input hospital data, we print the all_district_hospitals
                Console.WriteLine("\n\n", all_district_hospitals);
                // We create an empty customer list, it will later save the coordinates of all the district hospitals.  
                var customer = new List<object>();
                foreach (var i in Enumerable.Range(0, all_codes.shape[0])) {
                    customer.append(all_codes["Coordi"][i]);
                }
                // We declare the empty list as cost and the facilities that will store the cost to build the hospital.  
                var cost = new List<object>();
                var facilities = new List<object>();
                // We clean the district hospitals file and drop the na values from it and replace it entirely and then we reset the indices.
                all_district_hospitals.dropna(inplace: true);
                all_district_hospitals.reset_index(inplace: true);
                // We declare the empty list for coordinates and iterate through all the rows in the hospital dataframe to make a tuple of the coordinate locations and append it to the coordi list as shown below.
                var coordis = new List<object>();
                foreach (var i in Enumerable.Range(0, all_district_hospitals.shape[0])) {
                    tup = (all_district_hospitals.loc[i,"X1"], all_district_hospitals.loc[i,"X2"]);
                    coordis.append(tup);
                }
                // We set the cost per mile value as 5 for the problem at hand. Here it is hard coded into the model but it can later be changed to accomodate for any changes in the value later. 
                var cost_per_mile = 5;
                // We set the facilities value as the coordis from the previous last run lines.
                facilities = coordis;
                // We declare the threshold value to be the maximum distance allowed between a suitable facility for each customer location.
                var threshold = this.threshold;
                // We declare a dist function to calculate the driving distance between the two passed locations. We extract the miles attribute from the returned value. This can be changed to kilometers for our purposes in the return value itself.
                Func<object, object, object> dist = (loc1,loc2) => {
                    return distance.distance(tuple(loc1), tuple(loc2)).miles;
                };
                // We declare the empty dictionary pairings which will contain the indices of viable combinations of all hospitals and all pincodes between which the distance is lesser than the threshold distance passed as a parameter. All other combinations are discared and not stored in the dictioanry.            
                var pairings = new Dictionary<object, object> {
                };
                Console.WriteLine("\n\n", "Calculating the distances for {len(customer)*len(facilities)} combinations of facilities and customer/patient location");
                // We iterate through each of the customers and facilities available, find out the distance and compare the returned value with the threshold value passed as multiple key- value pair forlater use when defining the variable and constraints for our MIP problem.
                foreach (var cust in Enumerable.Range(0, customer.Count)) {
                    foreach (var facility in Enumerable.Range(0, facilities.Count)) {
                        if (dist(customer[cust], facilities[facility]) < this.threshold) {
                            try {
                                pairings[(facility, cust)] = dist(facilities[facility], customer[cust]);
                                //                 print(pairings[facility,customer])
                            } catch {
                                continue;
                            }
                        }
                    }
                }
                // We print out the number of viable pairings possible for the passed threshold value.
                Console.WriteLine("\n\nNumber of viable pairings: {0}".format(pairings.keys().Count));
                // We save the calculated pairing dictionary as a json readbale file for later use using the pickle module.
                using (var output_file = open(@"someobject1.pickle", "wb")) {
                    cpickle.dump(pairings, output_file);
                }
                // As the distances have already been calculated, we multiply each of these with the cost per mile as defined above. This gives the cost to transport from each of the faciliies to each of the pincodes 
                var shipping_cost = pairings.keys().ToDictionary(_tup_1 => (_tup_1.Item1, _tup_1.Item2), _tup_1 => cost_per_mile * pairings[(_tup_1.Item1, _tup_1.Item2)]);
                // We calculate the total number of the facilities and the customer locations.
                var num_facilities = facilities.Count;
                var num_customers = customer.Count;
                // We define an empty dictionary and store only those customer locations for which a viable facility is found.
                var gg = new List<object>();
                foreach (var _tup_2 in pairings.keys()) {
                    f = _tup_2.Item1;
                    c = _tup_2.Item2;
                    gg.append(c);
                }
                // In the empty list defined, we add the cost associated against each of the indices making in the pairings dictionary.
                foreach (var _tup_3 in pairings.keys()) {
                    f = _tup_3.Item1;
                    c = _tup_3.Item2;
                    cost.append(all_district_hospitals.iloc[f,-1]);
                }
                // MIP  model formulation. We start with formulating the MILP model now. We add the constraints, define variables, their allowed type, upper and lower bounds and assign them a name.
                // We define a model m named facility_location using gurobi solver module.
                Console.WriteLine("\n\nCreating the gurobi solver optimization model");
                var m = gp.Model("facility_location");
                Console.WriteLine("\n\nDeclaring Gurobi optimization variables");
                // We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                var select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
                // assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
                // assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                var assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
                // m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
                Console.WriteLine("\n\n Adding Constraints");
                // We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                m.addConstrs(from _tup_4 in pairings.keys().Chop((facility,customer) => (facility, customer))
                    let facility = _tup_4.Item1
                    let customer = _tup_4.Item2
                    select assign[facility,customer] <= select[facility], name: "Setup2ship");
                // This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                m.addConstrs(from customer in gg
                    select assign.sum("*", customer) == 1, name: "Demand");
                // We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                m.addConstr(select.sum() <= this.n_hospitals, name: "Facility_limit1");
                // m.addConstr(select.sum() >= 10, name="Facility_limit2")
                // We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                Console.WriteLine("\n\n Adding the objective function to the optimization model");
                var obj = gp.quicksum(from _tup_5 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
                    let facility = _tup_5.Item1
                    let cluster = _tup_5.Item2
                    select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]) + select.prod(cost);
                // Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                m.setObjective(obj, GRB.MINIMIZE);
                // We then make a function call to optimize the problem.
                Console.WriteLine("Optimizing");
                m.optimize();
                // Here we check the optimization status of the problem; if it's optimal for the parameters passed, it will create graphs and edges between the facilities and the customer if that particular customer serves that particular customer/patient location.
                grb_status = m.SolCount;
                Console.WriteLine("\n\nThe number of solutions obtained: ", m.SolCount);
                if (grb_status > 0) {
                    try {
                        assignments_file = new Dictionary<object, object> {
                        };
                        // We save the combination of the hospital and customer location for which the model makes an allocation.
                        assignments = (from p in pairings
                            where assign[p].x > 0.5
                            select p).ToList();
                        // We define the parameters to plot the graph using the matplotlib module.
                        plt.figure(figsize: (8, 8), dpi: 150);
                        plt.scatter(c: "Pink", s: 0.5, zip(customer));
                        plt.scatter(c: "Green", s: 1, zip(facilities));
                        // assignments = [p for p in pairings if assign[p].x > 0.5]
                        // We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                        foreach (var p in assignments) {
                            pts = new List<object> {
                                facilities[p[0]],
                                customer[p[1]]
                            };
                            assignments_file[p] = (facilities[p[0]], customer[p[1]]);
                            plt.plot(c: "Black", linewidth: 0.1, zip(pts));
                        }
                        // Save the assignments in the outputs folder as output_file.
                        assignments_file = pd.Series(assignments_file);
                        assignments_file.to_excel("output\outut_file.xlsx");
                        Console.WriteLine("\n\n", "The model is optimal with {n_hospitals} number of hospitals for {threshold} distance");
                    } catch {
                        Console.WriteLine("\n\nThe solution count is 0");
                    }
                } else {
                    // Or else if the model is infeasible with given parameter set, we try to find the optimum number of hospitals
                    Console.WriteLine("\n\nThe model is infeasible with the choice of parameters.");
                    if (this.first_time_unoptimized) {
                        this.first_time_unoptimized = false;
                        var continue_optimization = input("\n\nThe model is infeasible, do you want to re-run the model with increased n_hospital parameter you provided? Enter 1 or 0 as a response. 1 indicates that you want to rerun the code");
                        Console.WriteLine("\n\n", continue_optimization, type(continue_optimization));
                        if (continue_optimization == "1") {
                            this.n_hospitals += 1;
                            while (grb_status <= 0 && this.n_hospitals <= facilities.Count) {
                                Console.WriteLine("Trying to reoptimize again with {self.n_hospitals} number of hospitals");
                                m = gp.Model("facility_location");
                                // We define a variable named select, it is a binary data type and assumes value as 1 when a fcility is selected as a potential server for a patient location l1.
                                select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
                                // assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
                                // assign is another bianry variable which bases itself on the the keys of the pairings dictionary. This takes value if and only if a facility location can serve a customer location in an optimised cost scenario, otherwise it assumes value as zero.
                                assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
                                // m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
                                // We then begin adding constraints, the Setup2ship constraint takes care of the scenario that the selected facilities are only allowed to serve a customer location.
                                m.addConstrs(from _tup_6 in pairings.keys().Chop((facility,customer) => (facility, customer))
                                    let facility = _tup_6.Item1
                                    let customer = _tup_6.Item2
                                    select assign[facility,customer] <= select[facility], name: "Setup2ship");
                                // This constraint takes care of the case that for every customer location gets only 1 optimised allocated facility to avoid multi-allocation scenario. This helps is better decision making on the part of the customer.
                                m.addConstrs(from customer in gg
                                    select assign.sum("*", customer) == 1, name: "Demand");
                                // We then add a constraint to take care of the maximum number of hospitals that can be made as the budget is always a constraint due to the limited allocation to the healthcare budget out of the allocated budget.
                                m.addConstr(select.sum() <= this.n_hospitals, name: "Facility_limit1");
                                // m.addConstr(select.sum() >= 10, name="Facility_limit2")
                                // We then define the objective function which is to minimise the overal cost of the transportation as well as the cost to make a new facility
                                obj = gp.quicksum(from _tup_7 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
                                    let facility = _tup_7.Item1
                                    let cluster = _tup_7.Item2
                                    select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]) + select.prod(cost);
                                // Here we assign the optimization direction to the problem at hand, that is to minimize the overall cost as calculated above.
                                m.setObjective(obj, GRB.MINIMIZE);
                                // We then make a function call to optimize the problem.
                                m.optimize();
                                this.n_hospitals += 1;
                                grb_status = m.SolCount;
                            }
                            if (grb_status > 0) {
                                try {
                                    assignments_file = new Dictionary<object, object> {
                                    };
                                    // We save the combination of the hospital and customer location for which the model makes an allocation.
                                    assignments = (from p in pairings
                                        where assign[p].x > 0.5
                                        select p).ToList();
                                    // We define the parameters to plot the graph using the matplotlib module.
                                    plt.figure(figsize: (8, 8), dpi: 150);
                                    plt.scatter(c: "Pink", s: 0.5, zip(customer));
                                    plt.scatter(c: "Green", s: 1, zip(facilities));
                                    // assignments = [p for p in pairings if assign[p].x > 0.5]
                                    // We iterate through each of the assignments, define pts as the coordinates of the facility and the customers, and plot them on the graph one by one. We also append the valid assignments as an excelfile and save them in the outputs folder
                                    foreach (var p in assignments) {
                                        pts = new List<object> {
                                            facilities[p[0]],
                                            customer[p[1]]
                                        };
                                        assignments_file[p] = (facilities[p[0]], customer[p[1]]);
                                        plt.plot(c: "Black", linewidth: 0.1, zip(pts));
                                    }
                                    // Save the assignments in the outputs folder as output_file.
                                    assignments_file = pd.Series(assignments_file);
                                    assignments_file.to_excel("output\outut_file.xlsx");
                                    Console.WriteLine("\n\n", "The model is optimal with {self.n_hospitals} number of hospitals for {threshold} distance");
                                } catch {
                                    Console.WriteLine("\n\nThe solution count is 0");
                                }
                            }
                        }
                    }
                }
            }
        }
        
        public static object op = FacilityLocation();
        
        public static object distance_matrix = pd.read_csv("input\Input__2.csv");
        
        public static object pairings = new Dictionary<object, object> {
        };
        
        public static object cost_per_mile = 5;
        
        public static object threshold = threshold;
        
        public static object filtered_distance_matrix = distance_matrix[distance_matrix.loc[":","0"] <= threshold];
        
        public static object cost_per_mile = 5;
        
        public static object shipping_cost = pairings.keys().ToDictionary(_tup_2 => (_tup_2.Item1, _tup_2.Item2), _tup_2 => cost_per_mile * pairings[(_tup_2.Item1, _tup_2.Item2)]);
        
        public static object facilities = filtered_distance_matrix["level_0"].unique().ToList();
        
        public static object customer = filtered_distance_matrix["level_1"].unique().ToList();
        
        public static object num_facilities = filtered_distance_matrix["level_0"].nunique();
        
        public static object num_customers = filtered_distance_matrix["level_1"].nunique();
        
        public static object gg = new List<object>();
        
        public static object m = gp.Model("facility_location");
        
        public static object select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
        
        public static object assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
        
        public static object obj = gp.quicksum(from _tup_7 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
            let facility = _tup_7.Item1
            let cluster = _tup_7.Item2
            select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]);
        
        public static object status = m.SolCount;
        
        public static object n_hospitals = n_hospitals + 1;
        
        public static object m = gp.Model("facility_location");
        
        public static object select = m.addVars(num_facilities, vtype: GRB.BINARY, name: "select");
        
        public static object assign = m.addVars(pairings.keys(), vtype: GRB.BINARY, ub: 1, name: "assign");
        
        public static object obj = gp.quicksum(from _tup_11 in pairings.keys().Chop((facility,cluster) => (facility, cluster))
            let facility = _tup_11.Item1
            let cluster = _tup_11.Item2
            select cost_per_mile * pairings[facility,cluster] * assign[facility,cluster]);
        
        public static object status = m.SolCount;
    }
}

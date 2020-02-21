class Patients():
    def __init__(self):
        self.All = {}
        self.k = 0
    
    def new(self, RBS, Hb1Ac, Cre, fundus, case_seriousness, next_visit):
        self.k+=1
        l = {}
        l["id"] = self.k        
        l["rbs"] = RBS                       # (The values of RBS, Hb1AC, Cre and fundus will be  
        l["Hb1AC"] = Hb1Ac                     # the absolute difference between the ideal value and   
        l["Cre"] = Cre                         # the reading of the patient's report) 
        l["fundus"] = fundus
        l["next_visit"] = next_visit
        l["case_sn"] = case_seriousness #(between 1 to 10)
        l["days_delayed"] = 0
        self.All[self.k] = l
        
    def whom_to_call(self, n_vacancies):
        deadlined = []
        seriousness = []
        for id_n in range(1, self.k+1):
            if self.All[id_n]["next_visit"] == 0:
                deadlined.append(id_n)
                seriousness.append([self.All[id_n]["case_sn"],
                                    self.All[id_n]["days_delayed"],                                     
                                    self.All[id_n]["rbs"],           
                                    self.All[id_n]["Hb1AC"],        
                                    self.All[id_n]["Cre"],           
                                    self.All[id_n]["fundus"], 
                                    id_n])
        
        if len(deadlined)<=n_vacancies:
            return deadlined
        
        seriousness.sort(reverse=True)     # (it will first sort based on case seriousness and if two 
                                            # patients have same seriousness then it will decide based
                                            # on days delayed to their case, then RBC, Hb1AC, Cre and fundus
                                            # will be prioritized one by one)
        today = []
        for patient in seriousness:
            n_vacancies-=1
            if n_vacancies>=0:
                today.append(patient[-1])
            else:
                self.All[patient[-1]]["days_delayed"]+=1
        return today
    
    def next_visit_minus_one(self): # This should be called everyday. Even on non-working days of doctor.
        for patient in self.All:
            self.All[patient]["next_visit"]=max(self.All[patient]["next_visit"]-1, 0)
            
    def visit(self, patient_id ,RBS, Hb1Ac, Cre, fundus, case_seriousness, next_visit):
        self.All[patient_id]["rbs"] = RBS
        self.All[patient_id]["Hb1AC"] = Hb1Ac
        self.All[patient_id]["fundus"] = fundus
        self.All[patient_id]["Cre"] = Cre
        self.All[patient_id]["next_visit"] = next_visit
        self.All[patient_id]["case_sn"] = case_seriousness
        self.All[patient_id]["days_delayed"] = 0
        
        
def test():
    patients = Patients() # day 1
    patients.new(1,2,3,4,10,1) # id = 1
    patients.new(1,2,3,4,10,2) # id = 2
    patients.new(1,2,3,4,9,1)  # id = 3
    patients.next_visit_minus_one() # day 2
    print(patients.whom_to_call(1))  # will return 1 because 1 have higher priority than 3
    print(patients.whom_to_call(2))  # will return 1 and 3 because there are only they two with next_visit = 0 
    print(patients.whom_to_call(3))  # will also return 1 and 3 because there are only they two with next_visit = 0 
    patients.visit(1, 1, 2, 3, 4, 10, 3)
    patients.next_visit_minus_one() # day 3
    print(patients.whom_to_call(1))  # will return 3 because of higher prio
    print(patients.whom_to_call(2))  # will return 2 and 3
    
test()
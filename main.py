# written and maintained by Brian David Obot
# email: brianobot9@gmail.com phone: +234 7018977031, +234 8073487154

import numpy as np
from matplotlib import pyplot as plt
from functions import ( load_data, 
                        truncate_array, 
                        generate_func_mappings,
                        rectangulize,
                        plot_graph,
                        get_multiplier,
                        get_regression, 
                        get_formatted_regression,
                        get_help as help ,
                        )

PASSWORD = "concentration"

# load the csv data into a dataframe
dataframe = load_data()

# define a array for the x-axis values (which is the pressure axis)
x = dataframe["Total conc (ppm)"].astype(float)

# process and clean x axis values to remove invalid data 
x = truncate_array(x)

# convert to np-array
x = np.array(x)

# read the function documentation for details
interpolation_functions = generate_func_mappings(x=x, df=dataframe)


def start_over(eq_conc=0, force=False):
    if force:
        main()
    start = input("""
                    TO start over           Press 0:
                    TO Do Further Analysis  Press 1:  
                    >>> """)
    if start == '0':
        main()
    elif start == "1":
        more_analysis(eq_conc)

def main():
    # the flow of actions and controls would be carried out from here
    options = ['K+', 'Na+', 'Ca2+', 'Mg2+', 'Cl-', 'CO32-', 'HCO3-', 'SO42-']
    print("##########################################################################################################")
    print("    Welcome to the Interactive Total Solid Concentration Calculator: press Enter to continue  ")
    print("##########################################################################################################")
    print('Read Help before using the application ')
    action = input(""" 
                    OPTIONS: 
                    ______________________________________________________________________________________
                    (Option One)   TO Plot graph of "multiplier" against "concentration"       | PRESS 1
                    (Option Two)   TO Find the "multiplier" for Certain Element Concentration  | PRESS 2
                    (Option Three) To Get the Regression Equation for a Certain Element        | PRESS 3
                    (Option Four)  TO See help on using the application,                       | Press Help
                    (Option Five)  To Close the Application                                    | Press Close
                    _______________________________________________________________________________________
                    Type your Option: """)
    print("_______________________________________________________________________________________")
    valid_action = False
    
    while not valid_action:
        match action:
            case '1':
                valid_action = True
                # tune = input("Do want you to customize the graph display/result. Call +243 7018977031 for Feature Update! ")
                sep = input("Do you want to plot Each Element Seperately? Y for Yes and N for No : ")
                match sep:
                    case 'y' | 'Y':
                        plot_graph(dataframe, x, functions=interpolation_functions, sep=True)
                    case 'n' | 'N':
                        plot_graph(dataframe, x, functions=interpolation_functions)
                    case _:
                        print("Invalid Option....Ploting All elements in a single figure.")
                        plot_graph(dataframe, x, functions=interpolation_functions)
                start_over(force=True)
            case '2':
                valid_action = True
                element = input(f'Which element\'s multiplier do you want to get? options are {options} use comma to seperate multiple elements == ')
                
                elements = element.split(',')
    
                while not set(elements).issubset(set(options)):
                    print(f'X! Invalid Element given ...options are {options} [HINTS: options are case sensitive]')
                    element = input(f'Which elements multiplier do you want to get? {options=} == ')

                    elements = element.split(',')

                print("Selected Elements are ", elements)

                concs = []

                for elem in elements:
                    value = float(input(f"Which value of concentration do you want to check for (Ensure it is a single value) {elem} = "))
                    result = get_multiplier(elem, value, interpolation_functions)
                    concs.append(value * float(result))
                    print(f'The Multiplier for {elem} @ {value} concentration = {result}')
                    print("_______________________________________________________________")
                
                start_over(concs)
            case '3':
                elem = input("Please Select an Element to retrieve it Regression Equation: ")
                while elem not in options:
                    print(f"{elem} is Invalid Element...Try Again options are {[options]}")
                    elem = input("Please Select an Element to retrieve it Regression Equation: ")
                degree = input("What Degree do you want the polynomial to be?(Defaults to 15 degrees) : ")
                if degree.isdigit():
                    regression = get_regression(elem, degree, interpolation_functions)    
                else:
                    regression = get_regression(elem, degree=15, function=interpolation_functions)
                    degree = 15                
                reg_str = get_formatted_regression(regression)
                len_reg = len(reg_str)
                print("---------------------------------------------------------")
                print(f"The degree {degree} Regression for {elem} is Given below: ")
                print("#"*len_reg)
                print("#"*len_reg)
                print("#"*len_reg)
                print(reg_str)
                print("#"*len_reg)
                
                start_over(force=True)
            case 'help' | 'Help':
                print(help())
                start_over(force=True)
            case 'close' | 'Close':
                exit()
            case _:
                print("__________________________________________________________________")
                print(f"{action } is an Invalid Option try again! Options are {[1, 2, 'help']}")
                print("__________________________________________________________________")
                action = input(""" 
                                OPTIONS: 
                                ______________________________________________________________________________________
                                (Option One)   TO Plot graph of "multiplier" against "concentration"       | PRESS 1
                                (Option Two)   TO Find the "multiplier" for Certain Element Concentration  | PRESS 2
                                (Option Three) To Get the Regression Equation for a Certain Element        | PRESS 3
                                (Option Four) TO See help on using the application,                        | Press Help
                                (Option Five)  To Close the Application                                    | Press Close
                                ______________________________________________________________________________________
                                TYPE your option: """)
                print("______________________________________________________________________________________")


def more_analysis(eq_conc):
    sum_of_sq_conc = sum(eq_conc)
    print("__________________________________________________")
    print(f"Total Equivalent Concentration = {sum_of_sq_conc}")
    Rw = 0.0123 + (3547.5/(sum_of_sq_conc**0.955))
    print("_____________________________________")
    print(f"THE RW of the Set of Selected = {Rw}")
    print("_____________________________________")
    print(f"The Rw@75 = {1/Rw}")
    print("_____________________________________")


def protect():
    pwd = input("Please enter password to open program: ")
    while pwd != PASSWORD:
        print("Invalid Password ...Please try again.")
        pwd = input("Please enter password to open program: ")
    print("##################################")
    print(" PASSWORD IS VALID ")
    print("##################################")


if __name__ == "__main__":
    protect()
    main()
    input("Press any Key to Close")

"""
This Module holds all the function needed to execute the interactive concentration calculator
"""
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import numpy as np

# this function was neccesitated by the fact that they are unhandle invalid values in the columns
# so to avoid the bug arising from using those invalid values for main function operation
# i trimed down the initial columns to just the right amount of none errorneous data(defaulting 38)
def truncate_array(arr, last=36):
    """takes an array and returnd a trimmed version of the array"""
    return arr[:last]


def load_data(filename='Book1.csv'):
    # load the csv file into a python object and return the object
    # the file should be in the same directroy as this script
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("The required CSV file is not Found in the current directory! (Book1.csv)")
        input("Press any key to close: ")
        exit()
    return df


def set_up_interpolator(kind='quadratic', fill_value='extrapolate'):
    # not yet functional
    return interp1d()


def generate_func_mappings(x=None, df=None, interpolator=interp1d):
    # mapping to store the ref to the interp1d generated functions
    func_mappings = {}
    for index, column in enumerate(df):
        if index == 0:
            continue
        values = truncate_array(df[column])
        func = interpolator(x, values, kind='quadratic', fill_value='extrapolate')
        func_mappings[column] = func
    return func_mappings


def rectangulize(num):
    if num % 2 == 0:
        return (2, num//2)
    else:
        return (num//2, num/2 + 1)


def plot_graph(df, x, x_start=0, x_stop=300_000, y_lims=(0, 2), points=1000, from_table=True, functions=None, values=['K+', 'Na+', 'Ca2+', 'Mg2+', 'Cl-', 'CO32-', 'HCO3-', 'SO42-'], sep=False):
    match from_table:
        case True:
            x_stop = 100_000
            plt.figure(figsize=(10, 6))
            if sep:
                row, col = rectangulize(len(values))
                for index, element in enumerate(values):
                    plt.subplot(row, col, index+1)
                    y = truncate_array(df[element])
                    plt.plot(x, y, label=element)
                    plt.title(element)
                    plt.grid(which='both')
                plt.legend()
                plt.tight_layout()
                plt.show()
                return 
            for item in values:
                y = truncate_array(df[item])
                plt.plot(x, y, label=item)
            plt.legend(loc=0)
            plt.xlim(left=x_start, right=x_stop)
            plt.ylim(y_lims[0], y_lims[1])
            plt.xlabel("Total solid concentration (ppm or mg/kg)")
            plt.ylabel("Multiplier")
            plt.grid()
            plt.axvline(x=0, color='black')
            plt.axhline(y=0, color='black')
            plt.show()

        case False:
            x_axis = np.linspace(x_start, x_stop, points)
            plt.figure(figsize=(10, 6))
            if sep:
                row, col = rectangulize(len(values))
                for index, element in enumerate(values):
                    plt.subplot(row, col, index+1)
                    y = functions[element](x_axis)
                    plt.plot(x_axis, y, label=element)
                    plt.title(element)
                    plt.grid(which='both')
                plt.legend()
                plt.tight_layout()
                plt.show()
                return 
            for item in values:
                y = functions[item](x_axis)
                plt.plot(x_axis, y, label=item)
            plt.legend(loc=0)
            plt.xlim(left=x_start, right=x_stop)
            plt.xlabel("Total solid concentration (ppm or mg/kg)")
            plt.ylabel("Multiplier")
            plt.grid()
            plt.axvline(x=0, color='black')
            plt.axhline(y=0, color='black')
            plt.show()


def get_multiplier(element, x_axis, functions):
    return functions[element](x_axis)


def get_regression(element, degree=15, function=None):
    degree = int(degree)
    #extrapolate all x values as far as 500k
    x = np.linspace(0, 500000, 1000)
    element_interpolation_funtion = function[element]
    y = element_interpolation_funtion(x)

    # get regression
    y_est = np.polyfit(x, y, degree)
    return y_est


def get_formatted_regression(y_est):
    result = ""
    index = len(y_est)
    for value in y_est:
        index -= 1
        if index == 0:
            result += f"({value})X^{index}"
            continue
        result += f"({value})X^{index} + "
    return result


def get_help():
    return """
    HELP:
    #################################################################################################################
    * TO Input Multiple Values at ant point of Values input use comma to seperate the values and do not put space between them
    * Ensure to input values as suggested by the Options array, pay keen attention to the letter's cases
    *
    *   ########## #    #  #######  #      #    #     ##    #   # ######  #    #    ##
    *       #      #    #  #     #  # #    #    #   #       #   # #    #  #    #    ##
    *       #      #    #  #     #  #   #  #    # #          # #  #    #  #    #    ##
    *       #      ######  #######  #    # #    # #           #   #    #  #    #    ##
            #      #    #  #     #  #     ##    #   #         #   #    #  #    #  
            #      #    #  #     #  #      #    #     ##      #   ######  ######    ##
    * Incase of any technical issue experienced when using the calculator, contact the developer  \nPhone one: +234 7018977031 \n Phone two: +234 8073487154 \nemail: brianobot9@gmail.com
    ##################################################################################################################
    """
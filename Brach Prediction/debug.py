import sys 

# Smith branch predictor 
def smith(b, actual_branch_status):
    """
    Implements the Smith branch predictor.

    Parameters:
    - b (int): Number of bits for the counter in the Smith predictor.
    - actual_branch_status (list): List of actual branch outcomes (taken or not taken).

    Prints:
    - Number of predictions.
    - Number of mispredictions.
    - Misprediction rate.
    - Final content of the Smith counter.
    """
    total_states = 2 ** b
    counter = 0 if b == 1 else total_states // 2
    miss_predictions = 0
    middle_state = total_states // 2 - 1
    max_state = total_states - 1

    for instance in actual_branch_status:
        # Determine the prediction based on the counter value
        prediction = 't' if counter > middle_state else 'n'
        
        # Update the counter based on the actual outcome and adjust for boundaries
        if instance.lower() == prediction:
            counter = min(max_state, counter + 1) if counter > middle_state else max(0, counter - 1)
        else:
            miss_predictions += 1
            counter = max(0, counter - 1) if prediction == 't' else min(max_state, counter + 1)
    
    # Calculate and print the results
    total_predictions = len(actual_branch_status)
    misprediction_rate = (miss_predictions/total_predictions) * 100

    # print(f"number of predictions:     {total_predictions}")
    # print(f"number of mispredictions:  {miss_predictions}")
    print(f"misprediction rate:        {misprediction_rate:.2f}%")
    # print(f"FINAL COUNTER CONTENT:     {counter}")

# Bimodal branch predictor
def bimodal(m2, address, actual_branch_status):
    """
    Implements the Bimodal branch predictor.

    Parameters:
    - m2 (int): Number of bits for the index into the prediction table.
    - address (list): List of addresses from the trace file.
    - actual_branch_status (list): List of actual branch outcomes (taken or not taken).

    Prints:
    - Number of predictions.
    - Number of mispredictions.
    - Misprediction rate.
    - Final content of the Bimodal prediction table.
    """
    total_states = 2 ** m2
    miss_predictions = 0
    prediction_table = [4] * total_states

    for i in range(len(address)):
        # Calculate the index into the prediction table based on the address
        offset_address = int(address[i], 16) >> 2
        index = int(bin(offset_address)[-m2:], 2)

         # Determine the prediction based on the prediction table entry
        prediction = 't' if prediction_table[index] > 3 else 'n'

        # Update the prediction table based on the actual outcome and adjust for boundaries
        if actual_branch_status[i].lower() == prediction:
            prediction_table[index] = min(7, prediction_table[index] + 1) if prediction_table[index] > 3 else max(0, prediction_table[index] - 1)
        else:
            miss_predictions += 1
            prediction_table[index] = max(0, prediction_table[index] - 1) if prediction == 't' else min(7, prediction_table[index] + 1)
    
    # Calculate and print the results
    total_predictions = len(actual_branch_status)
    misprediction_rate = (miss_predictions / total_predictions) * 100

    # print(f"number of predictions:       {total_predictions}")
    # print(f"number of mispredictions:    {miss_predictions}")
    print(f"misprediction rate:          {misprediction_rate:.2f}%")
    # print("FINAL BIMODAL CONTENTS")
    # for i, value in enumerate(prediction_table):
        # print(f"{i} \t {value}")

# Gshare branch predictor
def gshare(m1, n, address, actual_branch_status):
    """
    Implements the Gshare branch predictor.

    Parameters:
    - m1 (int): Number of bits for the index into the prediction table.
    - n (int): Number of bits for the global history register.
    - address (list): List of addresses from the trace file.
    - actual_branch_status (list): list of actual branch outcomes (taken or not taken).

    Prints:
    - Number of predictions.
    - Number of mispredictions.
    - Misprediction rate.
    - Final content of the Gshare prediction table.
    """
    total_states = 2 ** m1
    miss_predictions = 0
    prediction_table = [4] * total_states
    global_history = '0' * n

    for i in range(len(address)):
        # Calculate the index into the prediction table based on the address and global history
        offset_address = int(address[i], 16) >> 2
        pc_index = int(bin(offset_address)[-m1:], 2)
        gshare_index = pc_index ^ int(global_history, 2)

        # Determine the prediction based on the prediction table entry
        prediction = 't' if prediction_table[gshare_index] > 3 else 'n'

        # Update the prediction table based on the actual outcome and adjust for boundaries
        if actual_branch_status[i].lower() == prediction:
            prediction_table[gshare_index] = min(7, prediction_table[gshare_index] + 1) if prediction_table[gshare_index] > 3 else max(0, prediction_table[gshare_index] - 1)
        else:
            miss_predictions += 1
            prediction_table[gshare_index] = max(0, prediction_table[gshare_index]-1) if prediction == 't' else  min(7, prediction_table[gshare_index] + 1)
        
        # Update the global history register
        global_history = ('1' if actual_branch_status[i] == 't' else '0') + global_history[:-1]

    # Calculate and print the results
    total_predictions = len(actual_branch_status)
    misprediction_rate = (miss_predictions / total_predictions) * 100

    # print(f"number of predictions:     {total_predictions}")
    # print(f"number of mispredictions:  {miss_predictions}")
    print(f"misprediction rate:        {misprediction_rate:.2f}%")
    # print("FINAL GSHARE CONTENTS")
    # for i, value in enumerate(prediction_table):
    #     print(f"{i} \t {value}")

# Hybrid branch predictor
def hybrid(k, m1, n, m2, address, actual_branch_status):
    """
    Implements the Hybrid branch predictor.

    Parameters:
    - k (int): Number of bits for the index into the hybrid prediction table.
    - m1 (int): Number of bits for the index into the Gshare prediction table.
    - n (int): Number of bits for the global history register.
    - m2 (int): Number of bits for the index into the Bimodal prediction table.
    - address (list): List of addresses from the trace file.
    - actual_branch_status (list): list of actual branch outcomes (taken or not taken).

    Prints:
    - Number of predictions.
    - Number of mispredictions.
    - Misprediction rate.
    - Final content of the Hybrid, Gshare, and Bimodal prediction tables.
    """
    total_states = 2 ** k 
    hybrid_prediction_table = [1] * total_states
    gshare_prediction_table = [4] * 2 ** m1 
    bimodal_prediction_table = [4] * 2 ** m2
    global_history = '0' * n
    miss_predictions = 0

    for i in range(len(address)):
        # Get Gshare prediction
        offset_address = int(address[i], 16) >> 2
        gshare_pc_index = int(bin(offset_address)[-m1:], 2)
        gshare_index = gshare_pc_index ^ int(global_history, 2)

        gshare_prediction = 't' if gshare_prediction_table[gshare_index] > 3 else 'n'

        # Update the global history register
        global_history = ('1' if actual_branch_status[i] == 't' else '0') + global_history[:-1]
        
        # Get bimodal prediction
        bimodal_index = int(bin(offset_address)[-m2:], 2)

        bimodal_prediction = 't' if bimodal_prediction_table[bimodal_index] > 3 else 'n'

        # Get hybrid table values 
        hybrid_index = int(bin(offset_address)[-k:], 2)

        # Select Gshare or Bimodal based on hybrid prediction table 
        if hybrid_prediction_table[hybrid_index] > 1:   # select gshare
            # Update gshare prediction table 
            if actual_branch_status[i].lower() == gshare_prediction:
                gshare_prediction_table[gshare_index] = min(7, gshare_prediction_table[gshare_index] + 1) if gshare_prediction_table[gshare_index] > 3 else max(0, gshare_prediction_table[gshare_index] - 1)
            else:
                miss_predictions += 1
                gshare_prediction_table[gshare_index] = max(0, gshare_prediction_table[gshare_index]-1) if gshare_prediction == 't' else  min(7, gshare_prediction_table[gshare_index] + 1)
        else:   # select bimodal
            # Update bimodal prediction table 
            if actual_branch_status[i].lower() == bimodal_prediction:
                bimodal_prediction_table[bimodal_index] = min(7, bimodal_prediction_table[bimodal_index] + 1) if bimodal_prediction_table[bimodal_index] > 3 else max(0, bimodal_prediction_table[bimodal_index] - 1)
            else:
                miss_predictions += 1
                bimodal_prediction_table[bimodal_index] = max(0, bimodal_prediction_table[bimodal_index] - 1) if bimodal_prediction == 't' else min(7, bimodal_prediction_table[bimodal_index] + 1)

        # Update hybrid prediction table values 
        if actual_branch_status[i].lower() == gshare_prediction and actual_branch_status[i].lower() != bimodal_prediction:
            hybrid_prediction_table[hybrid_index] = min(3, hybrid_prediction_table[hybrid_index] + 1)
        elif actual_branch_status[i].lower() != gshare_prediction and actual_branch_status[i].lower() == bimodal_prediction:
            hybrid_prediction_table[hybrid_index] = max(0, hybrid_prediction_table[hybrid_index] - 1)
    
    # Calculate and print results
    total_predictions = len(address)
    misprediction_rate = (miss_predictions/ total_predictions) * 100

    # print(f"number of predictions:      {total_predictions}")
    # print(f"number of mispredictions:   {miss_predictions}")
    print(f"misprediction rate:         {misprediction_rate:.2f}%")
    # print("FINAL CHOOSER CONTENTS")
    # for i, value in enumerate(hybrid_prediction_table):
    #     print(f"{i} \t {value}")
    # print("FINAL GSHARE CONTENTS")
    # for i, value in enumerate(gshare_prediction_table):
    #     print(f"{i} \t {value}")
    # print("FINAL BIMODAL CONTENTS")
    # for i, value in enumerate(bimodal_prediction_table):
    #     print(f"{i} \t {value}")

# Function to read trace file 
def read_file(file_path):
    """
    Reads a file containing branch prediction data.

    Parameters:
    - file_path (str): The path to the file to be read.

    Returns:
    - Tuple of lists: Two lists, the first containing branch addresses and
      the second containing the corresponding branch status (taken or not taken).
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract address and branch status from each line using zip and list comprehension
    address, branch_status = zip(*(line.strip().split() for line in lines))

    return address, branch_status

def main(args):
    """
    Main function to execute the branch prediction based on the provided arguments.

    Parameters:
    - args (list): Command line arguments.

    Prints:
    - Command details.
    - Output based on the selected branch predictor.
    """
    # Get the predictor type from command line arguments
    predictor_type = args[1].lower()

    # Extract parameters and trace file from command line arguments
    parameters = [int(arg) for arg in args[2:-1]]  # Exclude the last element
    trace_file = args[-1]

    # Read trace file to get addresses and branch status
    address, branch_status = read_file(trace_file)

    print('COMMAND')
    print(' '.join(args))
    print('OUTPUT')

    # Choose the appropriate branch prediction function based on the predictor type
    if predictor_type == 'smith':
        smith(*parameters, branch_status)
    elif predictor_type == 'bimodal':
        bimodal(*parameters, address, branch_status)
    elif predictor_type == 'gshare':
        gshare(*parameters, address, branch_status)
    elif predictor_type == 'hybrid':
        hybrid(*parameters, address, branch_status)
    else:
        print("Invalid branch type. Use 'smith', 'bimodal', 'gshare', or 'hybrid'")
        sys.exit(1)

# Code starts here 
if __name__ == "__main__":
    main(sys.argv)
'''
Copy testing_log.txt to logs.txt
'''

def append_log(source_log, destination_log):
    # Open the source_log in read mode
    with open(source_log, 'r') as source:
        # Read the file
        log = source.read()

    # Open the destination log in append mode
    with open(destination_log, 'a') as destination:
        destination.write(log)

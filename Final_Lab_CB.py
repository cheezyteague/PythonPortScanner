#! /usr/bin/env python3

# FILE: Final_Lab_CB.py
# NAME: Final Exam Lab
# AUTHOR: Canyon Bishop
# DATE: 10/23/20
# PURPOSE: Scan ports on 127.0.0.1 to determine which are open
#          and which are closed.

import pdb
import socket
import pickle
import sys
from urllib import request

# My pickle function
def pickle_dic(tcp_ports):
    # opens data file in binary mode
    pickledtcp = open('pickledtcp','wb')
    # Saves pickled dictionary to pickledtcp
    pickle.dump(tcp_ports,pickledtcp)
    pickledtcp.close()
    return None
    
# Do not modify this function.
def get_page_contents():
    """
    Get and return the HTML contents of a specific webpage that contains
    information about TCP ports.
    """

    try:
        # Define variables needed to make the URL request.
        url = "http://www.meridianoutpost.com/resources/articles/well-known-tcpip-ports.php"
        user_agent = "Mozilla"

        # Make the URL request and get the page contents.
        req = request.Request(url, headers={"User-Agent":user_agent})
        page = request.urlopen(req)
        contents = page.read().decode("utf-8")
    except:
        print("Cannot connect to webpage!")
        sys.exit(1)

    return contents


# Do not modify this function.
def get_td_elts(row):
    """
    Returns the contents inside of the given row's first three <td> tags.
    """

    # Initialize.
    offset = 0
    td_starts = []
    td_ends = []
    td_contents = []
    
    # Find where the three <td> blocks start and stop.
    for i in range(3):
        td_starts.append(row.find("<td>", offset))
        td_ends.append(row.find("</td>", td_starts[-1]))
        offset = td_ends[-1]

    # Now extract and return the contents from the <td> blocks.
    for i in range(3):
        td_contents.append(row[td_starts[i] + 4:td_ends[i]])

    return td_contents


def parse_contents(contents):
    global port_dict
    """
    Parse the supplied contents to extract TCP port numbers and 
    descriptions.  Store the information in a dictionary and
    return the dictionary to the caller of this function.
    The keys in the dictionary are the TCP port numbers, converted
    to ints.  The corresponding values are the ports' descriptions.
    """

    # Initialize the dictionary that will contain port information.
    port_dict = {}
    
    # Find the starting point for parsing.  This was determined by
    # manually examining the website's HTML source code.
    start = contents.find("<td>Status</td>") + 15
    
    # Loop over the HTML table rows.
    # Make this a for loop just to guarantee it will stop eventually.
    # A while loop is more suitable here but there is a risk of having
    # an infinite loop in that case, so we'll stick with the for loop.
    for i in range(1000):
        # Store the HTML table row in a variable for convenience.
        row_start = contents.find("<tr>", start)
        row_end = contents.find("</tr>", start)
        the_row = contents[row_start:row_end+6].replace("\n", "")

        # Extract the first three <td> elements out of the current row.
        # If the row has valid data for us, the first <td> element will
        # be the port number.  The second element will be the protocol.
        # The third element will describe what the port is used for.
        the_port, the_protocol, the_desc = get_td_elts(the_row)

        # If the_port is "0", then set the start variable equal to
        # row_end + 5 and skip the rest of this iteration.  No special
        # processing is to be done here if the_port isn't "0".
        # (Note: we modify the start variable like this so that we can
        # successfully process the next row in the next iteration.)
        if the_port == "0":
            start = row_end + 5
        

        # Need special handling due to inconsistent webpage formatting.
        # Sometimes stuff like this is necessary when web scraping.
        if the_port == "<p>383</p>":
            the_port = "383"

        #################################################################
        # TODO1: Remove the pass keyword below and replace it with
        # code that does what this comment describes:
        # If the_port is NOT numeric, then set the start variable equal
        # to row_end + 5 and skip the rest of this iteration.  No special
        # processing is to be done here if the_port actually is numeric.
        #################################################################
        if not the_port.isnumeric():
            start = row_end + 5
            continue
        ### Your code for TODO1 should not go below this line.
        
        #################################################################
        # TODO2: Remove the pass keyword below and replace it with
        # code that does what this comment describes:
        # If the_protocol DOES NOT CONTAIN "TCP" as a substring, then set
        # the start variable equal to row_end + 5 and skip the rest of
        # this iteration.  No special processing is to be done here if
        # the_protocol actually does contain "TCP" as a substring.
        #################################################################
        if "TCP" not in the_protocol:
            start = row_end + 5
            continue
        ### Your code for TODO2 should not go below this line.

        # At this point, we know we have valid data about a TCP port
        # and its purpose, so we must put the info into the dictionary.
        
        #################################################################
        # TODO3: Remove the pass keyword below and replace it with
        # code that does what this comment describes:
        # Put a key-value pair into the dictionary as follows:
        #   The key is the_port converted to an int.
        #   The corresponding value is the_desc.
        # Reiterating for emphasis: the key MUST be converted to an int!
        #################################################################
        key = int(the_port)
        port_dict[key] = the_desc
        ### Your code for TODO3 should not go below this line.

        # Increment the start variable by 5 so that we can successfully
        # process the next row in the next iteration.
        start = row_end + 5

    # Return the dictionary back to this function's caller.
    return port_dict


def fill_in_dictionary(tcp_ports):
    """
    Fills in any "gaps" in the port information dictionary.
    """

    # Port numbers range from 1 to 65535.
    for i in range(1, 65536):
        global port_dict
        # If the current port is a key in the dictionary, then
        # go to the next iteration in the loop.
        if i in tcp_ports:
            continue

        # At this point, we know that the current value of i is not
        # one of the ports in the dictionary.  Now we put it into
        # the dictionary and classify it appropriately.
        
        #################################################################
        # TODO4: Remove the pass keyword below and replace it with
        # code that does what this comment describes:
        # Add a key-value pair to the dictionary.  They key is i.  The
        # corresponding value depends on i.  If i is less than 1024, then
        # the value is "Well-known port".  If i is at least 1024 and less
        # less than 49152, then the value is "Registered port".
        # Otherwise, the value is "Public port".
        #################################################################
        if i < 1024:
            port_dict[i] = 'Well-known port'
        elif i >= 1024 and i < 49152:
            port_dict[i] = 'Registered port'
        else:
            port_dict[i] = 'Public Port'
        ### Your code for TODO4 should not go below this line.

    # Note that because of how Python processes objects such as
    # dictionaries, we should not and will not return tcp_ports.
    # The changes we made here to tcp_ports will already be visible
    # to whatever called this function.


def scan_ports(tcp_ports):
    """
    Scans all 65535 TCP ports to determine which are open and which
    are closed.  The provided dictionary will be updated accordingly
    and returned to the caller.
    """

    #####################################################################
    # DO NOT MODIFY THE host VARIABLE!  SCANNING PORTS ON A DOMAIN THAT #
    # YOU DO NOT OWN CAN POTENTIALLY HAVE SERIOUS LEGAL CONSEQUENCES!   #
    #####################################################################
    host = "127.0.0.1"
    #####################################################################
    # Very loosely speaking, 127.0.0.1 means "this device that I'm      #
    # using right now".  127.0.0.1 is therefore safe to scan.           #
    #####################################################################

    # Initialize lists for open and closed ports.
    open_ports = []
    closed_ports = []
    
    # Looping over all 65535 ports can take some time, so if you want
    # to perform quicker tests, feel free to change the stop value to
    # something smaller, like 1000 or 2000.  Make sure to change the
    # value back to 65536 before submitting this assignment.
    for port in range(1, 65536):
        try:
            # Create a TCP socket using the TCP/IP protocol.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Try to connect the socket to the current port on the host.
            result = s.connect_ex((host, port))

            # Process the result accordingly.
            if result == 0:
                # This means the port is open.

                #################################################################
                # TODO5: Remove the pass keyword below and replace it with
                # code that does what this comment describes:
                # Append the port number to the list of open ports.
                #################################################################
                open_ports.append(port)
                ### Your code for TODO5 should not go below this line.

                #################################################################
                # TODO6: Remove the pass keyword below and replace it with
                # code that does what this comment describes:
                # Update the dictionary accordingly.  Recall that port
                # numbers are keys in the dictionary and the corresponding
                # values are the port descriptions.  Now we will update
                # this port's value to be a tuple of two elements.  The
                # first element is the port's description and the second
                # element is the string "O" since this port is open.
                # (That's a capital letter O, not the number zero.)
                ################################################################
                ## Grabs the ports description from port_dict
                the_desc = port_dict.get(port)
                ## If the port is already in tcp_ports, add this tupled information
                if port in tcp_ports:
                    tcp_ports[port] = (the_desc, 'O')
                ### Your code for TODO6 should not go below this line.
            else:
                #################################################################
                # TODO7: Remove the pass keyword below and replace it with
                # code that does what this comment describes:
                # Append the port number to the list of closed ports.
                #################################################################
                closed_ports.append(port)
                ### Your code for TODO7 should not go below this line.

                # Update the dictionary accordingly.  Recall that port
                # numbers are keys in the dictionary and the corresponding
                # values are the port descriptions.  Now we will update
                # this port's value to be a tuple of two elements.  The
                # first element is the port's description and the second
                # element is the string "C" since this port is closed.
                if port in tcp_ports:
                    tcp_ports[port] = (the_desc, "C")
                
            # Close the connection.
            s.close()
        except:
            # Any number of things could have gone wrong, but for
            # simplicity we'll assume this means the port is closed.
            
            #################################################################
            # TODO8: Remove the pass keyword below and replace it with
            # code that does what this comment describes:
            # Append the port number to the list of closed ports.
            #################################################################
            closed_ports.append(port)
            ### Your code for TODO8 should not go below this line.

            #################################################################
            # TODO9: Remove the pass keyword below and replace it with
            # code that does what this comment describes:
            # Update the dictionary accordingly.  Recall that port
            # numbers are keys in the dictionary and the corresponding
            # values are the port descriptions.  Now we will update
            # this port's value to be a tuple of two elements.  The
            # first element is the port's description and the second
            # element is the string "C" since this port is closed.
            #################################################################
            the_desc = port_dict.get(port)
            if port in tcp_ports:
                tcp_ports[port] = (the_desc, "C")
            ### Your code for TODO9 should not go below this line.
            
    # Return both lists now that the loop is done.
    return open_ports, closed_ports


def save_the_list(the_list, filename):
    """
    Save the_list to a text file whose name is the given filename.
    """

    #################################################################
    # TODO10: Remove the pass keyword below and replace it with
    # code that does what this comment describes:
    # Open a text file for writing.  The file's name is given by the
    # supplied parameter filename.  Write the contents of the_list
    # to the file.  Each entry in the_list must be on its own line.
    # (Hint: Be careful since the entries of the_list are ints and
    # not strings.)
    # If the_list is empty, just make an empty output file.  (Hint:
    # This will happen for an empty the_list if this function is
    # written properly and efficiently.)
    #################################################################
    # Opening a text file of specified filename
    ofile = open(filename, 'wt')
    for e in the_list:
        # Writes element/line in list, converts to string first
        ofile.write(str(e))
        ofile.write('\n')
    ofile.close()
    return None
    ### Your code for TODO10 should not go below this line.


def main():
    # Get webpage contents.
    contents = get_page_contents()

    # Parse the contents to build the dictionary.
    tcp_ports = parse_contents(contents)

    # Now the dictionary contains data scraped from the web.
    # Fill in the missing port information in the dictionary.
    fill_in_dictionary(tcp_ports)

    # Scan the ports and get the results.
    open_ports, closed_ports = scan_ports(tcp_ports)

    # Write the two lists to two separate plain text files.
    save_the_list(open_ports, "open_ports.txt")
    save_the_list(closed_ports, "closed_ports.txt")

    #################################################################
    # TODO11: Pickle the dictionary.
    # Define a separate function for this inside of this file.
    # Do not define the function inside of main() or inside of
    # any other function.  Do not import pickle since it has
    # already been imported at the top of this file.
    # Your function should not return anything.
    # Remove the pass keyword below and replace it with a proper
    # call to your pickling function.
    #################################################################
    pickle_dic(tcp_ports)
    ### Your function call for TODO11 should not go below this line.
    ### Note that your function definition for TODO11 will
    ### necessarily be outside of this TODO11 block.

    print("That's a wrap!")

if __name__ == '__main__':
    main()
# TODO0: Properly complete the missing mainline logic here.

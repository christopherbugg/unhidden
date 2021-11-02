from multiprocessing import Process, Queue
import logger
import visitor
import dbmanager
import stem.util.system
import os


# Safety check for multiprocessing
if __name__ == '__main__':

    class Unhidden:

        # Specify the name of the links file
        links_filename = 'links.txt'

        # Create a database handler
        db = dbmanager.DBManager()

        # Constructor
        def __init__(self):

            print("Processing links file...")

            self.import_links()

            print("Processing Complete. Main loop initiated...")

            # Main Loop
            while True:

                # Get our list of Links
                links_list = self.db.get_links(10)

                # Create container for Visitor 'threads'
                visitor_threads = []

                # Create queue for getting back IPs from the Logger
                logger_queue = Queue()

                # Define the Logger process (just need 1)
                logger_process = Process(target=logger.log, args=(logger_queue,))

                # Start up the Logger process
                logger_process.start()

                # Start up a bunch of Visitor 'threads'
                for x in range(len(links_list)):
                    visitor_threads.append(stem.util.system.DaemonTask(visitor.visit, (links_list[x],), start=True))

                # Wait for the visitor 'threads' to all return
                for visitor_thread in visitor_threads:
                    visitor_thread.join()

                # Kill the Logger process.
                # Gotta do this since we need it to run (and block) until we're done
                logger_process.terminate()
                logger_process.join()

                # A container for the IPs we get from the Logger
                ip_list = []

                # Grab all the IPs out of the Logger queue
                while not logger_queue.empty():
                    ip_list.append(logger_queue.get())

                # Clean up the Logger queue
                logger_queue.close()
                logger_queue.join_thread()

                # Create records (if needed) for the returned IPs
                self.db.insert_multiple_ips(ip_list)

                # Create/Update connections information based on what we got
                connections_list = []
                for ip in ip_list:
                    for link in links_list:
                        connections_list.append((ip, link))

                self.db.insert_multiple_connections(connections_list)

        # Import links from a file
        def import_links(self):

            # Check if the file exists first
            if os.path.exists(self.links_filename):

                # Open file file for reading
                with open(self.links_filename) as file:

                    # Setup a new list to take the stripped down lines
                    striped_lines = []

                    # Grab the file as a list of it's lines and iterate through
                    for line in file.readlines():

                        # Strip off the newline at the end
                        striped_lines.append(line.rstrip())

                    # Put the stripped lines in the db
                    self.db.insert_multiple_links(striped_lines)


    Unhidden()

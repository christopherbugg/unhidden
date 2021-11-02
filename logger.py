from stem.control import EventType, Controller
import queue


# Gets the IP address of all new non-relay connections and puts in the queue
def log(logger_queue):

    # Startup stem controller to control our Tor process
    with Controller.from_port() as controller:

        # Authenticate the controller
        controller.authenticate()

        # Create the queue for events to process in
        event_queue = queue.Queue()

        # Add the listener for events on the controller
        controller.add_event_listener(lambda thisevent: event_queue.put(thisevent), EventType.ORCONN)

        # Loop till killed, looking for events
        while True:

            # Sit here and wait for an event
            this_event = event_queue.get()

            # Only log events for new, non-relay connections
            if this_event.status == "NEW":
                logger_queue.put(this_event.endpoint_address)

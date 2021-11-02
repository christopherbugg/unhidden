from urllib3.contrib.socks import SOCKSProxyManager
import urllib3.exceptions


# Visits a given link
def visit(link):

    # Add the tld since we don't need to store it
    onion_link = link + '.onion'

    # Setup our proxy settings
    proxy = SOCKSProxyManager('socks5h://localhost:9050')

    # Send a GET request to the link. We don't need or want anything else.
    try:
        proxy.request('GET', onion_link)

    # Catch some common errors
    except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.LocationValueError):
        # print("broken link: " + onion_link)
        pass

    # Catch anything else
    except Exception as e:
        print("the below exception was encountered when attempting the following link")
        print(onion_link)
        print(e)

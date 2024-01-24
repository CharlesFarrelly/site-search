import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin

# Set arrays
searched_links = []
class_instance = []
class_instances_cleaned = []
errors = []

def getLinksFromHTML(html):
    def getLink(el):
        return el["href"]
    return list(map(getLink, BeautifulSoup(html, features="html.parser").select("a[href]")))

def find_class_instance(domainToSearch, URL, parentURL, className):
    # Makes the domain available outside of this function
    find_class_instance.domain = domainToSearch
    if (not (URL in searched_links)) and (not ("javascript:" in URL)) and (not ("facebook.com/sharer/sharer.php" in URL)) and (not ("facebook.com/sharer.php" in URL)) and (not URL.startswith("tel:")):
        try:
            requestObj = requests.get(URL)

            # Check status code is good and the domain is not wandering
            if(requestObj.status_code == 200 and domainToSearch in urlparse(URL).netloc):
                # Adds the current link to searched items
                searched_links.append(URL)

                # Print updates to terminal
                print("Searching: " + URL)

                # Grab all classes on the page
                soup = BeautifulSoup(requestObj.text, "html.parser")
                # Get all elements with classes
                for element in soup.find_all(class_=True):
                    # search through a mega list of classes
                    for value in element["class"]:
                        # Add instance if search term is found in classes
                        if(value == sys.argv[2]):
                            class_instance.append(sys.argv[2] + " found on: " + URL)
                for link in getLinksFromHTML(requestObj.text):
                    # Check not already searched
                    if link not in searched_links:
                        find_class_instance(domainToSearch, urljoin(URL, link), URL, sys.argv[2])
            else:
                # Gets the next page to search in the domain and re-runs
                if (domainToSearch in urlparse(URL).netloc):
                    for link in getLinksFromHTML(requestObj.text):
                        # Check not already searched
                        if link not in searched_links:
                            find_class_instance(domainToSearch, urljoin(URL, link), URL, sys.argv[2])
        except Exception as e:
            if (not URL.startswith("mailto:")):
                errors.append("ERROR: " + str(e) + " from " + parentURL)
                print(errors[-1])
                searched_links.append(domainToSearch)

# Call function with terminal arguments
find_class_instance(urlparse(sys.argv[1]).netloc, sys.argv[1], "", sys.argv[2])

# Remove duplicates
for item in class_instance:
    if item not in class_instances_cleaned:
        class_instances_cleaned.append(item)

# Print Results 🙂
if class_instances_cleaned:
    print("\n--- Woohoo, some instances found:")
    for item in class_instances_cleaned:
        print ("\t" + item)
elif errors:
    error_message = print("\n\nThe following errors were also found: \n\n" + '%s' % '\n'.join(map(str, errors)) + "\n\n NOTE: This script is very picky so these may not all be real errors - just give them a click to check.")
else:
    print("\n--- No instances found! ---\n")

import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/post")
    response.raise_for_status()
    data = response.json()
    print(f"Success :{len(data)} records fetched")
# except requests.exceptions.HTTPError as e:
#     print(f"HTTP error:{e}")
# except requests.exceptions.ConnectionError:
#     print("Connection failed - check your internet")
except requests.exceptions as e:
    print(f"Something went wrong {e}")

# The try block executes the code and see if that ran successfully if not it proceeds to except 
# Then the except block look for what error has happened and print it accordingly
# The raise for status is used to see if the connection was successful and its a correct status code given if not raise an error immediatly before procedding
# The multiple except blocks are used to get different exceptions errors as if we only do the simple exception it will throw another exception
# the finally blocks runs anyways whatever the try block has .

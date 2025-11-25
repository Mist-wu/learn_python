import requests

BASE_URL = "https://textdb.online"

def write_data(key, value):
    
    url = f"{BASE_URL}/update/"
    try:
        response = requests.post(f"{url}?key={key}&value={value}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error writing data: {e}")
        return None

def read_data(key):

    url = f"{BASE_URL}/{key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error reading data: {e}")
        return None

def delete_data(key):


    return write_data(key, "")


if __name__ == "__main__":
    # Use a random or unique key to avoid collisions
    my_key = "142857"
    
    print("--- Writing ---")
    write_res = write_data(my_key, "Hello, World! This is a test.")
    if write_res['status']:
        print("Data written successfully.")
    else:
        print("Failed to write data.")
    


    print("\n--- Reading ---")
    content = read_data(my_key)
    print(f"Content: \n{content}")

    print("\n--- Deleting ---")
    delete_res = delete_data(my_key)
    if delete_res['status']:
        print("Data deleted successfully.")
    else:
        print("Failed to delete data.")
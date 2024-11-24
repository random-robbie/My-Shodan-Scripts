import shodan
import requests
import json

# Replace 'YOUR_API_KEY' with your actual Shodan API key
SHODAN_API_KEY = 'YOUR_API_KEY'
OUTPUT_FILE = 'output.txt'

def main():
    # Initialize the Shodan API
    api = shodan.Shodan(SHODAN_API_KEY)

    # Search for devices
    query = 'port:11434 http.html:"Ollama is running" country:"US"'
    results = api.search(query)

    # Iterate through the results
    for result in results['matches']:
        ip = result['ip_str']
        port = result['port']
        print(f"Found IP: {ip} on port: {port}")

        # Send a request to the local Ollama API
        url = f'http://{ip}:{port}/api/generate'
        payload = {
            "model": "llama3.2",
            "prompt": "Why is the sky blue?"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                # Write the IP and port to the output file
                with open(OUTPUT_FILE, 'a') as f:
                    f.write(f"{ip}:{port}\n")
                print(f"Response received from {ip}:{port}, logged to {OUTPUT_FILE}")
            else:
                print(f"Failed to get a valid response from {ip}:{port}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {ip}:{port} - {e}")

if __name__ == "__main__":
    main()

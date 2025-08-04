import urllib.request
import json

try:
    print("Probando endpoint /public/products...")
    req = urllib.request.Request("http://127.0.0.1:8000/public/products")
    req.add_header('accept', 'application/json')
    
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Headers: {dict(response.headers)}")
        response_text = response.read().decode()
        print(f"Response: {response_text}")
        
        # Intentar parsear JSON si es posible
        try:
            data = json.loads(response_text)
            print(f"JSON parsed successfully. Number of products: {len(data) if isinstance(data, list) else 'N/A'}")
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(f"Error response: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 

input("Press Enter to exit...")
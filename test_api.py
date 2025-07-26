import requests
import json

# Test script for HackRx 6.0 API
def test_hackrx_api():
    # API endpoint
    url = "http://localhost:8000/hackrx/run"
    
    # Sample request data
    test_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer d4877d9d88d610aa37e94d3f33b9257a5ccd6f36da70ee08a44dba7b3d684e9d"
    }
    
    try:
        print("🔄 Sending request to HackRx API...")
        print(f"URL: {url}")
        print(f"Questions: {len(test_data['questions'])}")
        
        # Send POST request
        response = requests.post(url, json=test_data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Request successful!")
            result = response.json()
            
            print("\n📊 Results:")
            print("-" * 50)
            
            for i, answer in enumerate(result['answers'], 1):
                print(f"\n{i}. Question: {answer['question']}")
                print(f"   Answer: {answer['answer']}")
                print(f"   Confidence: {answer['rationale'].get('confidence_factors', 'N/A')}")
                print(f"   Evidence Sources: {len(answer['rationale'].get('key_evidence', []))}")
                
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on localhost:8000")
        print("Run: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_hackrx_api()
import requests
import hashlib

def verify_and_store(url):
        headers = {'User-Agent': 'CivicAdvocate-OS-Agent'}
            response = requests.get(url, headers=headers)
                
                    if response.status_code == 200:
                                content_hash = hashlib.sha512(response.content).hexdigest()
                                        print(f"Record Verified: {url}")
                                                print(f"SHA-512 Ledger Hash: {content_hash}")
                                                        return content_hash
                                                        else:
                                                                    print(f"Audit Exception: Status {response.status_code}")
                                                                            return None

                                                                        target = "https://www.glo.texas.gov/archives-heritage/search-our-collections/land-grant-search/land-grant/167688-1987"
                                                                        verify_and_store(target)

import requests
import csv

def get_company_info(company_name):
    api_key = "YOUR_API_KEY"  # Replace this with your Google Maps API key
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={company_name}&inputtype=textquery&fields=formatted_address,name,geometry,place_id&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        place_id = data['candidates'][0]['place_id']
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={api_key}"
        details_response = requests.get(details_url)
        details_data = details_response.json()
        
        if details_data['status'] == 'OK':
            result = data['candidates'][0]  # Taking the first candidate
            address = result.get('formatted_address', 'Not available')
            # Parsing address components
            address_components = address.split(', ')
            address_1 = address_components[0]
            address_2 = address_components[1] if len(address_components) > 1 else 'Not available'
            city = address_components[-3] if len(address_components) >= 3 else 'Not available'
            state_zip = address_components[-2] if len(address_components) >= 2 else 'Not available'
            state, zip_code = state_zip.split(' ') if len(state_zip.split(' ')) == 2 else ('Not available', 'Not available')
            phone = details_data['result'].get('formatted_phone_number', 'Not available')
            
            return {
                'Company Name': company_name,
                'Address 1': address_1,
                'Address 2': address_2,
                'City': city,
                'State': state,
                'Zip': zip_code,
                'Phone': phone
            }
        else:
            print("Error:", details_data['status'])
            return None
    else:
        print("Error:", data['status'])
        return None

def main():
    with open('company_names.txt', 'r') as file:
        company_names = file.read().splitlines()

    with open('company_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Address 1', 'Address 2', 'City', 'State', 'Zip', 'Phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for company_name in company_names:
            company_info = get_company_info(company_name)
            if company_info:
                writer.writerow(company_info)

    print("Company information saved to company_info.csv")

if __name__ == "__main__":
    main()

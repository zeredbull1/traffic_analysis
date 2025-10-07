import requests
import json
import os 
from datetime import datetime
import schedule
import time

API_KEY = "_YRMvppSdybjNM5cvha6KPkcGS5YS_TOgHLlZr84rNA"
def collect_traffic_data():
     
    def get_route_with_traffic(origin, destination):
        """
        Get route from origin to destination with current traffic
        
        Args:
            origin: tuple (lat, lon) - Paris
            destination: tuple (lat, lon) - Palaiseau
        """
        
        url = "https://router.hereapi.com/v8/routes"
        
        params = {
            'transportMode': 'car',
            'origin': f'{origin[0]},{origin[1]}',
            'destination': f'{destination[0]},{destination[1]}',
            'return': 'summary,polyline,turnByTurnActions,travelSummary',
            'departureTime': datetime.now().replace(microsecond=0).isoformat(),
            'apiKey': API_KEY
        }
        
        response = requests.get(url, params=params)
        data = response.json()

        
        #Extract useful information
        route = data['routes'][0]
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': route['sections'][0]['travelSummary']['duration'],
            'duration_minutes': route['sections'][0]['travelSummary']['duration'] / 60,
            'distance_meters': route['sections'][0]['travelSummary']['length'],
            'distance_km': route['sections'][0]['travelSummary']['length'] / 1000,
            'base_duration': route['sections'][0]['travelSummary'].get('baseDuration', None),
            'traffic_delay': None
        }
        
        # Calculate traffic delay if base duration available
        if result['base_duration']:
            result['traffic_delay'] = result['duration_seconds'] - result['base_duration']
        
        return result

    # Example usage
    paris = (48.858694, 2.324993)  # Paris center
    palaiseau = (48.713830, 2.214260)  # Palaiseau

    traffic_data_solfe_X = get_route_with_traffic(paris, palaiseau)
    print(json.dumps(traffic_data_solfe_X, indent=2))

    with open("data_solfe_X.json", "r") as f:
            data = json.load(f)

    data.append(traffic_data_solfe_X)

    # Write back
    with open("data_solfe_X.json", "w") as f:
        json.dump(data, f, indent=2)

    #####Other way
    traffic_data_X_solfe = get_route_with_traffic(palaiseau, paris)
    print(json.dumps(traffic_data_X_solfe, indent=2))

    with open("data_X_solfe.json", "r") as f:
            data = json.load(f)

    data.append(traffic_data_X_solfe)

    # Write back
    with open("data_X_solfe.json", "w") as f:
        json.dump(data, f, indent=2)

    return True

collect_traffic_data()

schedule.every(10).minutes.do(collect_traffic_data)

print("Starting traffic data collection (every 10 minutes)...")
while True:
    schedule.run_pending()
    time.sleep(60) 

import requests
import time  # Added for delay in get_game_name

def get_owned_games(api_key, steam_id):
    """
    Fetches the list of owned games and playtime information from Steam's Web API.
    
    Parameters:
    - api_key: Your Steam Web API key.
    - steam_id: Your 64-bit Steam ID.
    
    Returns:
    - JSON response from the API or None if the request fails.
    """
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_played_free_games": True,  # Includes free games you've played
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def get_game_name(appid):
    """
    Fetches the game name for a given appid using the Steam API.
    
    Parameters:
    - appid: The appid of the game.
    
    Returns:
    - Game name as a string, or None if the request fails.
    """
    time.sleep(1)  # Add a 1-second delay between requests
    url = "https://store.steampowered.com/api/appdetails"
    params = {"appids": appid}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if str(appid) in data and data[str(appid)]["success"]:
            return data[str(appid)]["data"]["name"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game name for appid {appid}: {e}")
        return None

def main():
    print("This script retrieves your total playtime across all Steam games and lists each game with its playtime.")
    api_key = input("Enter your Steam API key: ")
    steam_id = input("Enter your 64-bit Steam ID: ")
    data = get_owned_games(api_key, steam_id)
    
    if data:
        if "response" in data and "games" in data["response"]:
            games = data["response"]["games"]
            
            # Calculate total playtime
            total_minutes = sum(game.get("playtime_forever", 0) for game in games)
            total_hours = total_minutes / 60  # Convert minutes to hours
            
            # Print list of games and their playtime
            print("\nList of Games and Playtime:")
            print("-" * 30)
            for game in games:
                appid = game.get("appid")
                playtime_minutes = game.get("playtime_forever", 0)
                playtime_hours = playtime_minutes / 60  # Convert minutes to hours
                
                # Skip games with 0 playtime (optional, remove if you want to see all games)
                if playtime_minutes == 0:
                    continue
                
                # Get the game name
                game_name = get_game_name(appid)
                if game_name:
                    print(f"{game_name}: {playtime_hours:.2f} hours")
                else:
                    print(f"AppID {appid} (Unknown Name): {playtime_hours:.2f} hours")
            
            # Print total playtime
            print("-" * 30)
            print(f"Total playtime: {total_hours:.2f} hours")
        else:
            print("No game data found. Ensure you are using your own API key and Steam ID.")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()
import requests

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
        response.raise_for_status()  # Raises an exception for HTTP errors (e.g., 403, 404)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def main():
    print("This script retrieves your total playtime across all Steam games.")
    api_key = input("Enter your Steam API key: ")
    steam_id = input("Enter your 64-bit Steam ID: ")
    data = get_owned_games(api_key, steam_id)
    if data:
        if "response" in data and "games" in data["response"]:
            games = data["response"]["games"]
            total_minutes = sum(game.get("playtime_forever", 0) for game in games)
            total_hours = total_minutes / 60  # Convert minutes to hours
            print(f"Total playtime: {total_hours:.2f} hours")
        else:
            print("No game data found. Ensure you are using your own API key and Steam ID.")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()
import requests  # Importerar request library
import random  # Importerar random modul
import redis  # Importerar redis modul

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)  # ansluter till redis databas


def random_quote_from_redis():  # fetchar random quote från db
    quote_id = random.choice(redis_client.keys())  # random key
    return redis_client.get(quote_id).decode()  # decode


def quotes_from_url(url):  # quote från url
    try:
        response = requests.get(url)  # get request
        if response.status_code == 200:  # if response 200
            quotes_data = response.json()  # parse JSON
            quotes = quotes_data.get("quotes", [])  # extract quote lista
            if quotes:
                for quote in quotes:  # loopar in alla quotes
                    redis_client.set(quote['id'], quote['quote'])
                print("Quotes har sparats i Redis databas")
            else:
                print("Inga quotes funna.")
        else:
            print("Misslyckad laddning av quotes från URL.")
    except Exception as e:
        print(f"Error uppstått: {e}")


def meny():  # func för meny
    while True:
        # Displayar meny options
        print("\nMeny:")
        print("1. Få Random Quote (Måste först köra 2. eller 3.)")
        print("2. Ladda ner quotes från dummyjson")
        print("3. Skriv in ett URL för att ladda ner quotes (JSON)")
        print("4. Avsluta program")

        choice = input("Välj ett alternativ: ")  # user väljer choice

        if choice == '1':  # om user väljer 1
            # Fetch and display a random quote from Redis
            print("Laddar random quote från databas...")
            quote = random_quote_from_redis()
            if quote:
                print("Random Quote:")
                print(quote)
        elif choice == '2':  # om user väljer 2
            print("Laddar ner quotes från dummyjson och sparar i Redis...")
            quotes_from_url('https://dummyjson.com/quotes')
        elif choice == '3':  # om user väljer 3
            url = input("Skriv URL till JSON fil som innehåller quotes: ")
            print(f"Laddar ner quotes från {url} och sparar i Redis...")
            quotes_from_url(url)
        elif choice == '4':  # exit
            print("Avslutar programmet...")
            break
        else:
            print("Felaktigt val. Försök igen.")


if __name__ == "__main__":  # Om filen körs direkt
    meny()

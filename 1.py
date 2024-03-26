import webbrowser
from weibo import APIClient
def main():
    try:
        APP_KEY ='3830241562'
        APP_SECRET ='fb519533e83c9a5cc4b49e33ac4ba81b'
        REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
        client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=REDIRECT_URL)
        url = client.get_authorize_url()
        # print(urz)
        webbrowser.open_new(url)
        result = client.request_access_token(
            input("please input code ： ")) 
        print(result)

    except Exception as e:
        print(e) 

if __name__ == "__main__":
    main()
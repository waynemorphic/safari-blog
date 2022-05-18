import urllib.request, json

quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def random_quotes():
    '''
    method gets the json url request from the  quote API
    '''
    
    with urllib.request.urlopen(quote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)
        quote_result = {}
        
        if get_quote_response['quote']:
            quote_result['id'] = get_quote_response['id']
            quote_result['author'] = get_quote_response['author']
            quote_result['quote'] = get_quote_response['quote']
            
        return quote_result
    
def generate_quote(times, random_quotes):
    quotes = []
    for i in range(times):
        quote = random_quotes()
        quotes.append(quote)
        
    return quotes
        
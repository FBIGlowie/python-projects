import asyncio
import aiohttp
import json
import uuid
from concurrent.futures import ThreadPoolExecutor




# this little script just spams the discord server that generates the promo urls for the opera gx partnership or whatever, gets rate limited a lot but i got 200k already made
# here is a little bash script to automate it forever, so you can leave it overnight lol


#source /home/path_to_python_env/bin/activate

#while true
#do
#python3 /path_to_file/nitrogenerator.py
#sleep 300
#done

#have fun


# Headers for the POST request
headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium"; v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
}
count = 0

# The number of threads to use
num_threads = 200 # Change this to the number of threads you want to use

# The dictionary to store the promotions
promotions = []

count_lock = asyncio.Lock()
async def get_promotion(session, i):
    global count
    partner_user_id = str(uuid.uuid4())
    data = json.dumps({"partnerUserId": partner_user_id})
    count += 1

    try:
        async with session.post('https://api.discord.gx.games/v1/direct-fulfillment', headers=headers, data=data) as response:
            print('HTTP status code: ' + str(response.status) + "  count: " + str(count))

            if response.status == 200:
                response_json = await response.text()
                response_json = json.loads(response_json)
                token = response_json['token']
                url = 'https://discord.com/billing/partner-promotions/1180231712274387115/' + token
                promotions.append(url)
            else:
                exit()
    except aiohttp.ClientOSError as e:
        print(f"Caught ClientOSError: {e}")
        return  # Skip the error and continue with the next iteration


async def main():
    while True:
       async with aiohttp.ClientSession() as session:
           tasks = []
           with ThreadPoolExecutor(max_workers=num_threads) as executor:
               for i in range(num_threads):
                  task = asyncio.ensure_future(get_promotion(session, i))
                  tasks.append(task)
               await asyncio.gather(*tasks)

           # Save the promotions to a JSON file
           with open('promotions.json', 'a') as f:
               for url in promotions:
                  f.write(f'{url}\n')

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

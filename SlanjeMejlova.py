from mailjet_rest import Client

def posalji_mejl(za, zanrovi, filmovi):
    api_key = '7b134c27df44cf44fdcffcbfbc423b83'
    api_secret = 'ca95d3df05dc7979173faa8f1d604fda'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "publisher123@tutanota.com",
            "Name": "Publisher"
        },
        "To": [
            {
            "Email": za[1],
            "Name": za[0]
            }
        ],
        "Subject": "NEW MOVIES",
        "TextPart": f"You are subscribed for genres: {zanrovi}\n New movies are : f{filmovi}\n",
        #"HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json())



import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    end_time = event['time']
    db_event = event['dbResults']
    order_id = event['detail']['orderId']
    file_name = '11111.html'

    # HTML template
    html = [
        "<head><link rel='stylesheet' type='text/css' href='https://serverlesspresso-order-journey-journeybucket-1lc9wg7eac1f4.s3.us-west-2.amazonaws.com/assets/css/style.css'>",
        "<link rel='stylesheet' type='text/css' href='https://serverlesspresso-order-journey-journeybucket-1lc9wg7eac1f4.s3.us-west-2.amazonaws.com/assets/css/fa.css'>",
        "<style>p{font-size:20px !important;} img{width:100%:} </style></head>",
        "<body>",
        "<div style='text-align:center'>",
        "<a href='https://order.serverlesscoffee.com'><img src='https://da-public-assets.s3.amazonaws.com/serverlesspresso/images/serverlesspresso-large.png'></a>",
        "</div>",
        "<section style='padding:20px;'><p style=''>Your order was orchestrated by this AWS Step Functions workflow:<br><img src='https://da-public-assets.s3.amazonaws.com/serverlesspresso/images/"+choose_graph(db_event['Items'])+"'><p></section>",
        "<section style='padding:20px;'><h2 style=''>Events:</h2><p style=''>These are the events that choreographed the order:</p></section>",
        "<section class='cd-timeline js-cd-timeline'>",
        "<div class='container max-width-lg cd-timeline__container'>"
    ]

    # HTML timeline block
    for item in db_event['Items']:
        event_details = json.loads(item['orderDetails']['S'])
        print(event_details)
        html.append(''.join([
            "<div class='cd-timeline__block'>",
            "<div class='cd-timeline__img cd-timeline__img--picture'>",
            "<img src='https://serverlesspresso-order-journey-journeybucket-1lc9wg7eac1f4.s3.us-west-2.amazonaws.com/assets/img/cd-icon-picture.svg' alt='Picture'>",
            "</div> <!-- cd-timeline__img -->",
            "<div class='cd-timeline__content text-component'>",
            "<h2 style=''>" + parse_detail(item['detailType']['S']) + "</h2>",
            "<p style='' class='color-contrast-medium'>" + parse_message(event_details['Message']) + "</p>",
            "<p><img style='width:100%;' src='https://da-public-assets.s3.amazonaws.com/serverlesspresso/images/" + item['detailType']['S'].replace('.', '') + ".png'></p>",
            "<div class='flex justify-between items-center'>",
            "<span class='cd-timeline__date'><h2 style=''>" + parse_time(item['SK']['S']) + "</h2></span>",
            "</div>",
            "</div> <!-- cd-timeline__content -->",
            "</div> <!-- cd-timeline__block -->"
        ]))
    # HTML template 2
    html2 = [
                "<div class='cd-timeline__block'>",
                "<!-- ... -->",
                "</div> <!-- cd-timeline__block -->",
                "</div>",
                "<div style='text-align:center'>",
                "<a style='width:50% !important; padding:10px; font-size:30px;' data-size='large' href='https://twitter.com/intent/tweet?text=I%20Just%20ordered%20a%20coffee%20using sererlesspresso!%20&url=https://serverlessland.com/sls-order-journey?orderId="+order_id+"&hashtags=serverlesspresso' class='twitter-share-button btn btn--subtle'> Share </a>",
                "</div>",
                "</section> <!-- cd-timeline -->",                
                "<script src='https://serverlesspresso-order-journey-journeybucket-1lc9wg7eac1f4.s3.us-west-2.amazonaws.com/assets/js/main.js'></script></body>"
            ]
    final_html = html + html2
    result = {'html': ''.join(final_html), 'fileName': db_event['Items'][0]['PK']['S'] + '.html'}
    
  
    print(result)
    return result

def parse_message(message):
    return message

def parse_detail(detail):
    friendly_detail = ''
    friendly_detail_array = detail.split('.')
    friendly_detail = friendly_detail_array[1]
    return friendly_detail

def parse_time(time):
    friendly_time = ''
    friendly_time_array = time.split('T')
    friendly_time = friendly_time_array[1].replace('Z\"', '')
    return friendly_time

def choose_graph(items):
    if items[-1]['detailType']['S'] == 'OrderManager.OrderCancelled':
        return 'order_processor_cancellation.png'
    return 'stepfunctions_graph_success.png'

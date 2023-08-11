from flask import Flask, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Load XML data
tree = ET.parse('Response.xml')
root = tree.getroot()
# Define namespaces
namespaces = {'ns': 'http://TekTravel/HotelBookingApi'}

ITEMS_PER_PAGE = 10

# @app.route('/')
# def index():
#     search_query = request.args.get('search', '').lower()
#     sort_key = request.args.get('sort', '')
#     page = int(request.args.get('page', 1))

#     filtered_data = []

#     for hotel_result in root.findall('.//{http://TekTravel/HotelBookingApi}HotelResult'):
#         hotel_info = hotel_result.find('{http://TekTravel/HotelBookingApi}HotelInfo')
#         hotel_name = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelName').text.lower()
#         hotel_description = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelDescription').text.lower()

#         if search_query in hotel_name or search_query in hotel_description:
#             filtered_data.append(hotel_result)

#     total_items = len(filtered_data)
#     total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

#     start_index = (page - 1) * ITEMS_PER_PAGE
#     end_index = start_index + ITEMS_PER_PAGE

#     paginated_data = filtered_data[start_index:end_index]

#     return render_template('/templates/index.html', data=paginated_data, search=search_query, current_page=page,
#                            total_pages=total_pages, prev_page=page - 1, next_page=page + 1)

def convert_rating(rating_string):
    if rating_string == 'OneStar':
        return 1
    elif rating_string == 'TwoStar':
        return 2
    elif rating_string == 'ThreeStar':
        return 3
    # Add more ratings as needed
    else:
        return 0  # Default value for unknown ratings

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    sort_key = request.args.get('sort', '')
    page = int(request.args.get('page', 1))

    filtered_data = []

    for hotel_result in root.findall('.//{http://TekTravel/HotelBookingApi}HotelResult'):
        hotel_info = hotel_result.find('{http://TekTravel/HotelBookingApi}HotelInfo')
        hotel_name = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelName').text.lower()
        hotel_description_element = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelDescription')
        hotel_description = hotel_description_element.text if hotel_description_element is not None else ""

        if search_query in hotel_name or search_query in hotel_description:
            filtered_data.append(hotel_result)

    if sort_key == 'name':
        filtered_data.sort(key=lambda hotel: hotel.find('{http://TekTravel/HotelBookingApi}HotelInfo/{http://TekTravel/HotelBookingApi}HotelName').text)
    elif sort_key == 'price':
        filtered_data.sort(key=lambda hotel: float(hotel.find('{http://TekTravel/HotelBookingApi}MinHotelPrice').get('PrefPrice')))
    elif sort_key == 'rating':
        filtered_data.sort(key=lambda hotel: convert_rating(hotel.find('{http://TekTravel/HotelBookingApi}HotelInfo/{http://TekTravel/HotelBookingApi}Rating').text))
        # filtered_data.sort(key=lambda hotel: float(hotel.find('{http://TekTravel/HotelBookingApi}HotelInfo/{http://TekTravel/HotelBookingApi}Rating').text))
        # filtered_data.sort(key=lambda hotel: float(hotel.find('ns:HotelInfo/ns:Rating', namespaces).text))
        
    total_items = len(filtered_data)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    paginated_data = filtered_data[start_index:end_index]

    return render_template('index.html', data=paginated_data, search=search_query, current_page=page,
                           total_pages=total_pages, prev_page=page - 1, next_page=page + 1)

if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/')
# def index():
#     search_query = request.args.get('search', '').lower()
#     sort_key = request.args.get('sort', '')
#     page = int(request.args.get('page', 1))

#     filtered_data = []

#     for hotel_info in root.findall('.//HotelInfo'):
#         hotel_name = hotel_info.find('HotelName').text.lower()
#         hotel_description = hotel_info.find('HotelDescription').text.lower()

#         if search_query in hotel_name or search_query in hotel_description:
#             filtered_data.append(hotel_info)

#     if sort_key == 'name':
#         filtered_data.sort(key=lambda hotel: hotel.find('HotelName').text)
#     elif sort_key == 'rating':
#         filtered_data.sort(key=lambda hotel: hotel.find('Rating').text)

#     total_items = len(filtered_data)
#     total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

#     start_index = (page - 1) * ITEMS_PER_PAGE
#     end_index = start_index + ITEMS_PER_PAGE

#     paginated_data = filtered_data[start_index:end_index]

#     return render_template('index.html', data=paginated_data, search=search_query, sort=sort_key,
#                            current_page=page, total_pages=total_pages,
#                            prev_page=page - 1 if page > 1 else None,
#                            next_page=page + 1 if page < total_pages else None)





# from flask import Flask, render_template, request
# import xml.etree.ElementTree as ET

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Read the XML data from the file
#     tree = ET.parse('Response.xml')
#     root = tree.getroot()

#     # Extract relevant data from the XML
#     hotel_results = []
#     for hotel_result in root.findall('.//{http://TekTravel/HotelBookingApi}HotelResult'):
#         hotel_info = hotel_result.find('{http://TekTravel/HotelBookingApi}HotelInfo')
#         hotel_name = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelName').text
#         hotel_description = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelDescription').text
#         hotel_picture = hotel_info.find('{http://TekTravel/HotelBookingApi}HotelPicture').text
#         # Extract other relevant data here

#         hotel_results.append({
#             'name': hotel_name,
#             'description': hotel_description,
#             'picture': hotel_picture,
#             # Add other data to the dictionary
#         })

#     return render_template('./templates/index.html', hotel_results=hotel_results)

# if __name__ == '__main__':
#     app.run(debug=True)

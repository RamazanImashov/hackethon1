
from bs4 import BeautifulSoup as bs
import requests
import csv


def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['price_dollar'], data['price_som'], data['image'], data['description']])

def get_html(url):
    response = requests.get(url)
    return response.text
    # print(response)

# def get_total_pages(html):
#     soup = bs(html, 'lxml')
#     page_list = soup.find('ul', class_="pagination").find_all('a')[-1].attrs.get('data-page')
#     print(page_list)
#     # return int(last_page)

def get_total_pages(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('ul', class_="pagination").find_all('a')[-1].attrs.get('data-page')
    if page_list is not None:
        return int(page_list)
    else:
        return 0



def get_data(html):
    soup = bs(html, 'lxml')
    cars_list = soup.find('div', class_ = 'table-view-list').find_all('div', class_ = 'list-item list-label')
    # print(cars_list)
    
    for car in cars_list:
        try:
            title = car.find('div', class_='title').find('h2').text.strip()
        except AttributeError:
            title = 'none '
        # try:
        #     price_som = car.find('div', class_='price').find('p').text.split().replace(price_dollar, '')
        #     price_som = ' '.join(price_som)
        #     # price_som.replace(price_dollar, '')
        # except AttributeError:
        #     price_som = 'none '
        try:
            price_dollar = car.find('div', class_='price').find('p').find('strong').text.split()
            price_dollar = ' '.join(price_dollar)
        except AttributeError:
            price_dollar = 'none '
        try:
            price_som = car.find('div', class_='price').find('p').text.split()#.replace(price_dollar, '')
            price_som = ' '.join(price_som)
            # price_som.replace(price_dollar, '')
            # print(price_som)
        except AttributeError:
            price_som = 'none '
        try:
            image = car.find('div', class_='thumb-item-carousel').find('img').attrs.get('data-src')
            # image = car.find('img').get('src')[0]
        except:
            image = 'none '
        try:
            desc = car.find('div', class_='block info-wrapper item-info-wrapper').text.split()
            desc = ''.join(desc)
        except AttributeError:
            desc = 'none '
            
        product_dict = {
            'title': title, 
            'price_dollar': price_dollar,
            'price_som': price_som.replace(price_dollar, ''),
            'image': image, 
            'description': desc
            
        }
        write_to_csv(product_dict)
            
            
            
        # print(title)
        # print(price_som.replace(price_dollar, ''))
        # print(price_dollar)
        # print(image)
        # print(desc)


# def main():
#     url = 'https://www.mashina.kg/search//?currency=2&price_from=&price_to='
#     html = get_html(url)
#     get_data(html)
#     # html = get_data(get_html(url))
#     get_total_pages(html)
#     number = get_total_pages(html)
#     for i in range(1, number + 1):
#         global page_list
#         if i != print(page_list):
#             url_with_page = url + '&page=' +  str(i)
#             html = get_html(url_with_page)
#             get_data(html)
#         else:
#             break

# main()


def main():
    url = 'https://www.mashina.kg/search//?currency=2&price_from=&price_to='
    html = get_html(url)
    get_data(html)
    number = get_total_pages(html)
    for i in range(1, number + 1):
        url_with_page = url + '&page=' + str(i)
        html = get_html(url_with_page)
        get_data(html)
        
        
with open('data.csv', 'w') as file:
    write_ = csv.writer(file)
    write_.writerow(['title             ','price dollar          ','price som          ', 'image            ', 'description           '])

main()
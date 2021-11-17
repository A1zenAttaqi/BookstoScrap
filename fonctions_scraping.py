import requests
from bs4 import BeautifulSoup
import csv
import os

#Fonction qui retourne les URLs de chaque categorie
def get_url_category(url):

    reponse = requests.get(url)
    links= []
    if reponse.ok:
        soup = BeautifulSoup(reponse.content,'html.parser')
        categories = soup.find_all('ul',class_='nav nav-list')
    
        for category in categories:
            for link in category.find_all('a',href=True):
                links.append('http://books.toscrape.com/'+ link ['href'])
    
    return links



#Fonction qui retourne les URLs des Livres de chaque page 
def get_url_Books(url_category):
    reponse = requests.get(url_category)
    bookslinks=[]
    if reponse.ok:
        soup=BeautifulSoup(reponse.content,'html.parser')
        article_N=soup.find_all('strong')[1]  
        nbr= int(article_N.text)
        '''print('le nombres de livres: ', nbr)'''
        nombres_pages=nbr//20 +1
        for i in range(1,nombres_pages+1):
            new_url_category=''
            if nbr>20:
                new_url_category=url_category.replace('index.html',f'page-{i}.html')
            else:
                new_url_category=url_category
            '''print (new_url_category) '''   
            new_reponse = requests.get(new_url_category)
            if new_reponse.ok:
                soup=BeautifulSoup(new_reponse.content,'html.parser')                  
                bookslist=soup.find_all('article',class_='product_pod')
                for item in bookslist:
                    link=item.find('a',href=True)
                    link=link['href'].replace('../../../','')
                    bookslinks.append('https://books.toscrape.com/catalogue/' + link)    
    return bookslinks   



#Fonction qui retourne un dictionnaire de détails de chaque livre
def get_books_info(url_books):
    response = requests.get(url_books)
    book={}
    if response.ok:
        soup=BeautifulSoup(response.content,'html.parser')
        product_page_url=url_books
        title=soup.find('div',class_='col-sm-6 product_main').find('h1').text
        category_1= soup.find_all('li')[2].text
        category=category_1[1:len(category_1)-1]
        universal_product_code=soup.find_all('td')[0].text
        price_including_tax=soup.find_all('td')[3].text
        price_excluding_tax=soup.find_all('td')[2].text
        number_available=soup.find_all('td')[5].text
        product_description=soup.find_all('p')[3].text
        product_description=product_description.replace(',' , '')
        image_url='http://books.toscrape.com/'+ soup.find_all('img')[0] ['src']
        product_main= soup.find('div',class_='col-sm-6 product_main')
        rating = product_main.find('p',class_='star-rating')['class'][1]
        rating_value = ''
        if rating == 'One':
            rating_value = '1/5'
        elif rating == 'Two':
            rating_value ='2/5'
        elif rating =='Three':
            rating_value ='3/5'
        elif rating =='Four':
            rating_value ='4/5'
        elif rating == 'Five':
            rating_value ='5/5'
        else:
            rating_value ='no rating available'
        book = {
            'product_page_url': product_page_url, 
            'universal_ product_code (upc)':universal_product_code,
            'title':clean_file_name(title),
            'price_including_tax':price_including_tax,
            'price_excluding_tax':price_excluding_tax,
            'number_available':number_available,
            'product_description':product_description,
            'category': category,
            'image': image_url,
            'rating': rating_value,
        }    
    return book    

                            
#Fonction qui crée les fichier csv de chaque categorie et les remplie par les info de chaque livres dans cette categorie
def creation_fichier_csv(url_category):
    reponse=requests.get(url_category)
    if reponse.ok:
        soup=BeautifulSoup(reponse.content,'html.parser')
        nom_category=soup.find('div',class_='page-header action').text 
        nom_category_csv=nom_category[1:len(nom_category)-1] +'.csv'
        save_path = './Csv_files'
        file_name= nom_category_csv
        completeName = os.path.join(save_path, file_name)
        with open(completeName, 'w',encoding='utf-8-sig') as csvfile:
            fieldnames = ['product_page_url', 'universal_ product_code (upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','image', 'rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,dialect='excel')
            writer.writeheader()
            books_url= get_url_Books(url_category)

            for book_url in books_url:
                book_info=get_books_info(book_url)
                writer.writerow(book_info)


# fonction qui télécharge et enregistre le fichier image de chaque Livre
def download_image(image_url,title_image):
    response = requests.get(image_url)
    title_image=clean_file_name(title_image)
    save_path = './Images'
    file_name= title_image + '.jpg'
    
    completeName = os.path.join(save_path, file_name)
    file = open(completeName, "wb")
    file.write(response.content)
    file.close()

# fonction qui retire les caractères interdits dans les noms de fichiers
def clean_file_name(text):
    text=text.replace(':', '_').replace('?', '_').replace(',', '_').replace('"', '_').replace(' ', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('| ', '_')
    return text












      

        




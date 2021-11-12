
from fonctions_scraping import get_url_category,get_url_Books,get_books_info,download_image,creation_fichier_csv
import os
print('start...')


baseurl= 'https://books.toscrape.com/'
if not os.path.exists('./Images'):
    os.makedirs('./Images')
if not os.path.exists('./Csv_files'):
    os.makedirs('./Csv_files')    



categories_links=get_url_category(baseurl)
for category_link in categories_links[1:]:
    print('scrap category: ',category_link)
    category_csv=creation_fichier_csv(category_link)
    books_url= get_url_Books(category_link)
    for book_url in books_url:
        print('scrap category: ',category_link,'book: ',book_url)
        book_info=get_books_info(book_url)
        url_image=book_info['image']
        title_image=book_info['title']
        download_image(url_image,title_image)
print('end')          
        
    

        






    
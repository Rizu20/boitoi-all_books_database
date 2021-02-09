import os
import json
import csv
import urllib.request
from datetime import datetime


def total_book_count():
    success=0
    fail=10000
    book_id=fail
    while fail-success!=1:
        url_string='https://boitoi.com.bd/api/books/v1/books/'+str(book_id)+'/details/'
        try:
            response=urllib.request.urlopen(url_string)
            if response.status==200:
                success=book_id
        except urllib.error.HTTPError:
            fail=book_id
        book_id=int(success+((fail-success)/2))

    return book_id


def boitoi_request(book_id):
    url_string='https://boitoi.com.bd/api/books/v1/books/'+str(book_id)+'/details/'
    try:
        response=urllib.request.urlopen(url_string)
        if response.status==200:
            response_data=response.read().decode('utf-8')
            response_dict=json.loads(response_data)

            book_title=response_dict['title']
            authors_count=len(response_dict['authors'])
            authors=[]
            for author in response_dict['authors']:
                authors.append(str(author['id'])+' : '+author['name'])
            publisher=response_dict['publisher']
            if publisher!=None:
                publisher=str(publisher['id'])+" : "+publisher['name']
            categories=[]
            for category in response_dict['categories']:
                categories.append(category['name'])
            isbn=response_dict['isbn']
            language=response_dict['language']
            price=response_dict['price']
            android_price=response_dict['price_android']
            ios_price=response_dict['price_ios']
            discount=response_dict['discount']
            rating=response_dict['rating']
            reviews_count=response_dict['reviews']
            text_reviews_count=response_dict['text_reviews']
            pages_count=response_dict['pages']

            return [book_id,book_title,authors_count,authors,publisher,categories,isbn,language,price,android_price,ios_price,discount,rating,reviews_count,text_reviews_count,pages_count]
    
    except urllib.error.HTTPError:
        print("HTTP Error occured for Book ID {}".format(book_id))
        pass



def csv_file_write(response_dict_list,csv_headers):
    with open(os.path.join(os.getcwd(),'boitoi_output.csv'),'w',newline='',encoding="utf-8") as f_out:
        csv_writer=csv.DictWriter(f_out,fieldnames=csv_headers)
        csv_writer.writeheader()

        for row_dict in response_dict_list:
            csv_writer.writerow(row_dict)



# def main():
start_time=datetime.now()

max_book_count=total_book_count()
print("Total count of books found in boitoi.com : {}. Time taken {} seconds.".format(max_book_count,(datetime.now()-start_time).seconds))

print("Starting individual book info request")
response_dict_list=[]
csv_headers=['Book ID','Book Title','Authors Count','Authors','Publisher','Categories','ISBN','Language','Price','Android Price','IOS Price','Discount','Rating','Review Count','Text Review Count','Page Count']
for book_id in range(1,max_book_count+1):
    boitoi_response=boitoi_request(book_id)
    if boitoi_response != None:
        response_dict={}
        for i,j in zip(csv_headers,boitoi_response):
            response_dict[i]=j
        response_dict_list.append(response_dict)
print("Total {} books information fetched. Time taken {} seconds.".format(len(response_dict_list),(datetime.now()-start_time).seconds))

csv_file_write(response_dict_list,csv_headers)
print("Response data from API call successfully written to CSV file. Time taken {} seconds.".format((datetime.now()-start_time).seconds))

print("Program complete")


# try:
#     main()
# except Exception as e:
#     print(str(e))

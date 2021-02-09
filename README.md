# boitoi-all_books_database
This script places repeated API calls to boitoi.com.bd to create a complete current books database.

At first, with a binary search, this script finds out the total number of books currently at boitoi.com.bd
Afterwards, this script places API calls to the website with incrementing book id to fetch all information (eg. author, publisher, price, discount etc.) and creates a output CSV file, containing information for all books.

This script takes around half an hour or more for about 2000 books without threading. With threading, it should take less time.

API related to books only was used. Other APIs (eg. authors or publishers ) didn't provide complete books information.

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    l = []
    with open(filename, 'r') as resFile:
        soup = BeautifulSoup(resFile, 'html.parser')
        for row in soup.find("tbody").find_all('td'):
            if row.find('a', class_='bookTitle'):
                l.append(
                    (row.find('a', class_='bookTitle').text.strip(), row.find('a', class_='authorName').text.strip()))

    return l


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    l = []
    cnt = 0
    try:
        soup = BeautifulSoup(requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc").text,
                             "html.parser")
    except:
        print("Error while creating Soup object")
        return l

    for row in soup.find("table").find_all('td'):
        if row.find('a', class_='bookTitle'):
            l.append("https://www.goodreads.com" + row.find('a', class_='bookTitle')['href'])  # Ask Michael
            cnt += 1
            if cnt == 10:
                break

    return l


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    t = ()
    try:
        soup = BeautifulSoup(requests.get(book_url).text, "html.parser")
    except:
        print("Something went wrong.")
        return t

    return (soup.find('h1', id="bookTitle").text.strip(), soup.find('a', class_='authorName').text.strip(), int(re.match('\d*', soup.find('span', itemprop='numberOfPages').text).group(0)))



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    t = []
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        for cat in soup.findAll('div', class_='category clearFix'):
            t.append((cat.find('h4', class_='category__copy').text.strip(), cat.find('img', class_='category__winnerImage')['alt'].strip(), cat.find('a')['href']))
    return t


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w') as f:
        cw = csv.writer(f)
        cw.writerow(['Book title,Author Name'])
        for row in data:
            cw.writerow(row)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        t = soup.find('div', id='description').text
        return list(map(str.strip, re.findall(r'\b[A-Z]\w{2,}\b ?(?:\b[A-Z]\w{2,}\b ?)+', t)))


class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        l = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(l), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(l, list)
        # check that each item in the list is a tuple
        for li in l:
            self.assertIsInstance(li, tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertTupleEqual(l[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(l[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(self.search_urls, list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in self.search_urls:
            self.assertIsInstance(url, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertIsNotNone(re.search(r'https://www\.goodreads\.com/book/show', url))

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = list(map(get_book_summary, TestCases.search_urls))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        # check that each item in the list is a tuple
        for summary in summaries:
        # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
        # check that the first two elements in the tuple are string
            self.assertIsInstance(summary[0], str)
            self.assertIsInstance(summary[1], str)

        # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(summary[2], int)


        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summaries = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(summaries), 20)
        # assert each item in the list of best books is a tuple
        for summary in summaries:
            self.assertIsInstance(summary, tuple)
        # check that each tuple has a length of 3
            self.assertEqual(len(summary), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertTupleEqual(summaries[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertTupleEqual(summaries[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        s = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(s, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as f:
            r = csv.reader(f)
            l = [line for line in r]

            # check that there are 21 lines in the csv
            self.assertEqual(len(l), 21)

            # check that the header row is correct
            self.assertListEqual(l[0], ['Book title,Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
            self.assertListEqual(l[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertListEqual(l[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])

    def test_extra_credit(self):
        print(extra_credit('extra_credit.htm'))


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)

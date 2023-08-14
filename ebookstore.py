#=====importing libraries===========
import sqlite3

#=====Connect to db=======
try:
    #connect to database and create cursor obj
    db = sqlite3.connect('ebookstore') 
    curs = db.cursor()

    curs.execute('''
        CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)
    ''')

    print("Database & table created.")

#handle error
except Exception as e:
    db.rollback()
    raise e

#=====Populating table=======
try:
    #check if table is empty
    curs.execute('SELECT * FROM books')
    table = curs.fetchall()

    if table == []:
        #populating the table
        values = (
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, "Harry Potter and the Philosopher's stone", 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
        )

        insert_statment = ('INSERT INTO books VALUES (?,?,?,?)')
        curs.executemany(insert_statment, values)

        db.commit()
        print('Items inserted!')
    
    else:
        pass

except Exception as e:
    db.rollback()
    raise e


#=====Functions=======
def get_id(param):
    #get tuple of id
    curs.execute('SELECT id FROM books')
    id_list = curs.fetchall()
    #convert id to list
    converted_list = [i[0] for i in id_list]

    #get id with error handling
    id = ''
    while True:
        try:
            id = int(input(f"Please enter id of book to {param} or '0' to retrn to menu: "))
            if id == 0:
                break
            while id not in converted_list:
                try:
                    id = int(input("Incorrect id, please try again. Press '0' to retrn to menu: "))
                    if id == 0:
                        break
                except:
                    pass

        except:
            print("Please ensure that the id is an integer value or '0' to return to menu: ")
        else:
            break
    
    return id

def ent_book():
    #get list of all ids in the table to see if new id exists
    curs.execute('SELECT id FROM books')
    id_list = curs.fetchall()    
    #convert id to list
    converted_list = [i[0] for i in id_list]

    #get id
    id = ''
    while True:
        try:
            id = int(input(f'Please enter id of book to enter: '))
            while id in converted_list:
                try:
                    id = int(input('id already exist, please enter unique id: '))
                except:
                    print("Please ensure that the id is an integer value!")

        except:
            print("Please ensure that the id is an integer value: ")
        else:
            break
    
    #get book title and author from user
    title = input('Please enter book title: ')
    author = input('Please enter book author: ')

    #get qty
    while True:
        try:
            qty = int(input('Please enter book quantity: '))
        except:
            print("Please ensure that the quantity is an integer value: ")
        else:
            break

    #insert data into db
    curs.execute('INSERT INTO books VALUES (?,?,?,?)', (id, title, author, qty))
    
    db.commit()
    print('\nBook Entered!\n')


def upd_book():
    #get book id
    id = get_id('update')

    #code to be executed when user doesn't opt to return to menu
    if id != 0:
        update_param = input('''Please choose parameter to update: ''').lower()
        while update_param not in ['id', 'title','author','qty']:
            update_param = input("Oops! Incorrect selection. Please try again: ")

        if update_param == 'qty' or update_param == 'id':

            try:
                update = int(input("Enter update: "))
            except:
                print("Please ensure that you enter an integer value!")
        else:
            update = input("Enter update: ")

        try:
            #update data in db
            exe_statement = f'UPDATE books SET {update_param} = ? WHERE id = ?'
            curs.execute(exe_statement, (update, id))
            db.commit()

        except Exception as e:
            db.rollback()
            raise e

        print('\nUpdate complete!\n')
    
    else:
        pass

def del_book():
    #get i of book to del
    id = get_id('delete')

    #code to be executed when user doesn't opt to return to menu
    if id != 0:
        try:
            #del book
            curs.execute('DELETE FROM books WHERE id = ?', (id,))
            print('\nBook deleted!\n')

        except Exception as e:
            db.rollback()
            raise e
        
    else:
        pass

def srch_book():
    #get i of book to search
    id = get_id('search')

    #code to be executed when user doesn't opt to return to menu
    if id != 0:

        try:
            #search book
            curs.execute('SELECT * FROM books WHERE id = ?', (id,))
            selected_book = list(curs.fetchone())
            print(f'\nBook id: {id}\nTitle: {selected_book[1]}\nAuthor: {selected_book[2]}\nQty: {selected_book[3]}\n')

        except Exception as e:
            db.rollback()
            raise e
    else:
        pass


def exit_code():
    print('Goodbye!!!')
    exit()
    
#=====Menu=======

print('\nWelcome!\n')
try:
    while True:
        while True:
        #menu
            try:
                menu = int(input('''\nSelect the number of the action to perform:
                1. Enter book
                2. Update book
                3. Delete book
                4. Search books
                0. Exit

                selection: '''))
            except: 
                print('\nOops! Please ensure that you enter an integer value.\n')
            else:
                break

        if menu == 1:
            ent_book()
        elif menu == 2:
            upd_book()
        elif menu == 3:
            del_book()
        elif menu == 4:
            srch_book()
        elif menu == 0:
            exit_code()
        else:
            print('Entry incorrect. Please try again!')

except Exception as e:
    raise e

finally:
    #close database
    db.close()
from setup import Merch, Shows, Sales
from sqlalchemy import create_engine, func, inspect, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///MerchManager.db', echo=False)
Session = sessionmaker(bind=engine)
inspector = inspect(engine)


# View all rows and columns in the merch table
def view_merch():
    view_session = Session()
    shows = view_session.query(Shows).all()
    view_session.close()
    return shows


# View all rows and columns in the shows table
def view_shows():
    view_session = Session()
    shows = view_session.query(Shows).all()
    view_session.close()
    return shows


# View all rows and columns in the sales table
def view_sales():
    view_session = Session()
    sales = view_session.query(Sales).all()
    view_session.close()
    return sales


# Add a row to the merch table
def add_merch(item, price):
    merch = Merch(item=item, price=price)
    add_merch_session = Session()
    add_merch_session.add(merch)
    add_merch_session.commit()
    add_merch_session.close()


# Add a row to the shows table
def add_show(date, venue):
    show = Shows(date=date, venue=venue)
    add_show_session = Session()
    add_show_session.add(show)
    add_show_session.commit()
    add_show_session.close()


# Add a row to the sales table
def add_sale(show_id, item, sold):
    sale = Sales(show_id=show_id, item=item, sold=sold)
    add_sale_session = Session()
    add_sale_session.add(sale)
    add_sale_session.commit()
    add_sale_session.close()


# Search the merch table for a user-provided term
def search_merch(term, column):
    search_merch_session = Session()
    if column == '1':
        results = search_merch_session.query(Merch).filter(Merch.item.like('%' + term + '%')).all()
        return results
    elif column == '2':
        results = search_merch_session.query(Merch).filter(Merch.price.like('%' + term + '%')).all()
        return results


# Search the shows table for a user-provided term
def search_shows(term, column):
    search_shows_session = Session()
    if column == '1':
        results = search_shows_session.query(Shows).filter(Shows.show_id.like('%' + term + '%')).all()
        return results
    elif column == '2':
        results = search_shows_session.query(Shows).filter(Shows.date.like('%' + term + '%')).all()
        return results
    elif column == '3':
        results = search_shows_session.query(Shows).filter(Shows.venue.like('%' + term + '%')).all()
        return results


# Search the sales table for a user-provided term
def search_sales(term, column):
    search_sales_session = Session()
    if column == '1':
        results = search_sales_session.query(Sales).filter(Sales.show_id.like('%' + term + '%')).all()
        return results
    elif column == '2':
        results = search_sales_session.query(Sales).filter(Sales.item.like('%' + term + '%')).all()
        return results
    elif column == '3':
        results = search_sales_session.query(Sales).filter(Sales.sold.like('%' + term + '%')).all()
        return results


# Return a string telling user which item sold the most units at any one show
def get_most_sold():
    get_stats_session = Session()
    max_sold_query = get_stats_session.query(Sales.item, func.max(Sales.sold), Sales.show_id)
    get_stats_session.close()
    for item in max_sold_query:
        return 'Best-selling item at any one show: ' + str(item[0]) + ' at ' + str(item[1]) + \
               ' units sold during show #' + str(item[2]) + "\n"


# Return a string telling user which item earned the most money at any one show
def get_best_earner():
    get_stats_session = Session()
    best_earner_query = get_stats_session.query(Sales.item, func.max(Sales.sold * Sales.price), Sales.show_id)
    get_stats_session.close()
    for item in best_earner_query:
        return 'Best-earning item at any one show: ' + str(item[0]) + ' at $' + '{0:.2f}'.format(item[1]) + \
               ' earned during show #' + str(item[2]) + "\n"


# Return a string telling user which item they sold the most of in total
def get_most_sold_lifetime():
    get_stats_session = Session()
    most_sold_query = get_stats_session.query(Sales.item, func.sum(Sales.sold)).group_by(Sales.item).order_by(desc('sum_1'))
    get_stats_session.close()
    for item in most_sold_query:
        return 'Best selling item overall: ' + str(item[0] + " at " + str(item[1]) + " units sold.\n")


# Return a string telling the user which item they sold the fewest of in total
def get_fewest_sold_lifetime():
    get_stats_session = Session()
    most_sold_query = get_stats_session.query(Sales.item, func.sum(Sales.sold)).group_by(Sales.item).order_by('sum_1')
    get_stats_session.close()
    for item in most_sold_query:
        return 'Worst selling item overall: ' + str(item[0] + " at " + str(item[1]) + " units sold.\n")


# Combine all stat functions into one string to return to ui
def get_stats():
    string1 = get_most_sold()
    string2 = get_best_earner()
    string3 = get_most_sold_lifetime()
    string4 = get_fewest_sold_lifetime()
    return string1 + string2 + string3 + string4


# Check if user-provided show id is a valid number in the shows table
def check_id(show_id):
    check_id_session = Session()
    num_ids = check_id_session.query(Shows).filter_by(show_id=show_id).count()
    check_id_session.close()
    if num_ids > 0:
        return True
    else:
        return False


# Check if user-provided item name is a valid name in the merch table
def check_item(item):
    check_item_session = Session()
    num_items = check_item_session.query(Merch).filter_by(item=item).count()
    check_item_session.close()
    if num_items > 0:
        return True
    else:
        return False

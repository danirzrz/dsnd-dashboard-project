# Import the QueryBase class
#### YOUR CODE HERE
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
#### YOUR CODE HERE
from .sql_execution import QueryMixin

# Define a subclass of QueryBase
# called Employee
#### YOUR CODE HERE
class Employee(QueryBase, QueryMixin):
    # Class attribute
    name = "employee"

    # Set the class attribute `name`
    # to the string "employee"
    #### YOUR CODE HERE


    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
        # Method: names
    def names(self):
        sql = """
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM employee
        """
        return self.query(sql)  # Usando método de QueryMixin

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
        # Method: username
    def username(self, id):
        sql = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return self.query(sql)

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):
        sql = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
        """
        return self.pandas_query(sql)

    # Método: event_counts
    def event_counts(self, id):
        sql = f"""
            SELECT event_date
                 , SUM(positive_events) AS positive_events
                 , SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """
        return self.pandas_query(sql)

    # Método: notes
    def notes(self, id):
        sql = f"""
            SELECT note_date, note
            FROM notes
            JOIN {self.name}
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(sql)   
    
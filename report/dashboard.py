from fasthtml.common import fast_app, serve, H1, Div
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE
from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team

# import the load_model function from the utils.py file
#### YOUR CODE HERE
from report.utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from report.base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from report.combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
#### YOUR CODE HERE
class ReportDropdown(Dropdown):
        
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE
    def build_component(self, *args, **kwargs):

        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        #### YOUR CODE HERE
        # Set label equal to model name
        self.label = kwargs.get('model').name if 'model' in kwargs else self.name
 

        # Return the output from the
        # parent class's build_component method
        #### YOUR CODE HERE
        return super().build_component(*args, **kwargs)

    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
    def component_data(self, entity_id, model, *args, **kwargs):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        if model is None or not hasattr(model, 'names'):
           return []
        try:
            # Usamos el método names() de Employee/Team
            rows = model.names()  # lista de tuplas (full_name, id)
            # Convertimos a (id, nombre) para el dropdown
            return [(row[0], row[1]) for row in rows]
        except Exception as e:
            print("Error en ReportDropdown:", e)
            return []

# Create a subclass of base_components/BaseComponent
# called `Header`
#### YOUR CODE HERE
class Header(BaseComponent):
        
    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE
    def build_component(self, entity_id, model, *args, **kwargs):

        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        #### YOUR CODE HERE
        title = getattr(model, "name", "Employee Events Dashboard")
        return H1(title)

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
#### YOUR CODE HERE
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model, *args, **kwargs):

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        #### YOUR CODE HERE
        
        # Use the pandas .fillna method to fill nulls with 0
        #### YOUR CODE HERE
        
        # User the pandas .set_index method to set
        # the date column as the index
        #### YOUR CODE HERE
        
        # Sort the index
        #### YOUR CODE HERE
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        #### YOUR CODE HERE
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        #### YOUR CODE HERE
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        #### YOUR CODE HERE
        
        # call the .plot method for the
        # cumulative counts dataframe
        #### YOUR CODE HERE
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        #### YOUR CODE HERE
        
        # Set title and labels for x and y axis
        #### YOUR CODE HERE
        if model is None:
           return plt.figure()  # retorna un gráfico vacío
        asset_id = kwargs.get("asset_id", entity_id)
        df = model.event_counts(asset_id)
        if df.empty:
            fig, ax = plt.subplots()
            ax.set_title("No events available")
            return fig
        
        df = df.fillna(0).set_index('event_date').sort_index().cumsum()
        df.columns = ['Positive', 'Negative']

        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Event Counts')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        return fig

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE
class BarChart(MatplotlibViz):
        
    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model, *args, **kwargs):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE
        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE
        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE
            
        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE
        
        # Initialize a matplotlib subplot
        #### YOUR CODE HERE
        if model is None:
            fig, ax = plt.subplots()
            ax.set_title("No data available")
            return fig
        asset_id = kwargs.get("asset_id", entity_id)
        data = model.model_data(asset_id)
        pred_probs = self.predictor.predict_proba(data)[:, 1]
        if model.name == "team":
            pred = pred_probs.mean()
        else:
            pred = pred_probs[0]

        fig, ax = plt.subplots()

        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        return fig

# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
#### YOUR CODE HERE
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE
    children = [LineChart(), BarChart()]
    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
#### YOUR CODE HERE
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE
    def component_data(self, entity_id, model, *args, **kwargs):       
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        #### YOUR CODE HERE
        if model is None:
            return[]
        return model.notes(entity_id)

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE
    children = [
        Header(),                 # Header sin pasar por modelo
        DashboardFilters(),       # Filtros
        Visualizations(),         # LineChart + BarChart
        NotesTable()              # Tabla de notas
    ]

# Initialize a fasthtml app 
#### YOUR CODE HERE
# not necessary with this fasthtml version - from fasthtml.common import App, Div
# not necessary with this fasthtml version - app = App(title="Employee Events Dashboard")

# Initialize the `Report` class
#### YOUR CODE HERE
# report = Report()
# Creamos la app y el router con fast_app()
app, rt = fast_app()

# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE
# not necessary with this fasthml version @get('/')
# Definimos rutas usando rt
@rt("/")
def root():

    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
    #### YOUR CODE HERE
    report = Report()
    employee_model = Employee()
    return report(1, employee_model)

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
#### YOUR CODE HERE
# not necessary with this fasthml version @get('/employee/{employee_id}')
@rt("/employee/{employee_id}")
def employee_page(employee_id: str):

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    report = Report()
    return report(employee_id, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
#### YOUR CODE HERE
# not necessary with this fasthml version @get('/team/{team_id}')
@rt("/team/{team_id}")
def team_page(team_id: str):

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    report = Report()
    return report(team_id, Team())

# Keep the below code unchanged!
# not necessary with this fasthml version @get('/update_dropdown{r}')
@rt("/update_dropdown")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]

    # Depuración: imprime el profile_type
    profile_type = r.query_params.get('profile_type', 'Employee')
    print('PARAM', profile_type)

    # Crea la instancia del modelo según el tipo
    if profile_type == 'Team':
        model = Team()
    else:
        model = Employee()

    # Llamamos al componente para que genere el HTML
    return dropdown(None, model)


# not necessary with this fasthml version @post('/update_data')
@rt("/update_data", methods=["POST"])
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    

# luego ejecuta el servidor si el script es directo
if __name__ == "__main__":
    print("Ejecuta este módulo con: uvicorn report.dashboard:app --reload")
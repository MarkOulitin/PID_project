# Maintenance Manual

## Table of Contents
1. [Database maintenance](#database_maintenance)
2. [Samples parser](#samples_parser)
3. [Frontend implementation](#frontend_implementation)


### Database maintenance <a name="database_maintenance"></a>
The current system implementation uses SQLite. This is the lightest SQL implementation which could meet our needs. 
However, when the software has accumulated a vast amount of data, it may not be sufficient anymore.

Thus, we allow the user to replace the DAO implementation of the system. As such, the implementor has to create a class which
implements the DB interface, as such:

* **Save query**:

    Signature -
```def create_request(self, request: QueryRequest)```
  (Return value is ignored). 

    Contatins the query attributes:   
    * PLC name
    * PID coefficeints that already used in that PLC
    * Simulation minutes - the requested amount of minutes the performance simulation of PID closed loop will take. 
    * Simulation seconds - the requested amount of seconds the performance simulation of PID closed loop will take. 
    

* **Get queries**:

    Signature - 
    ```python
  def get_query_requests(self, plc_path: str) # (Return value is ignored).
  ```
    It returns a list of query requests matching the ```plc_path``` argument.


####    QueryRequest is as follows:

| Name               | Type   | Description                                                           |
|--------------------|--------|-----------------------------------------------------------------------|
| id                 | String | A string representation of a UUID4 id, auto-generated for the request |
| plc_id             | String | The id of the queried controller                                      |
| p                  | Number | P value for PID                                                       |
| i                  | Number | I value for PID                                                       |
| d                  | Number | D value for PID                                                       |
| simulation_minutes | Number | Number of minutes requested for the simulation                        |
| simulation_seconds | Number | Number of seconds requested for the simulation                        |
| set_point          | Number | The desired set point for the process recommendation                  |


After Implementing these interfaces, replace the instance creation [here](https://github.com/MarkOulitin/PID_project/blob/e6e17ac014f01798949ea83347c188fa55e8832e/server.py#L27) with the new implementation.



### Request parser <a name="samples_parser"></a>

In order to support new CSV formats which could potentially be adopted by the factory, the system needs to update its CSV
parsing function.

In order to do so, the maintainer has to implement a parsing function with the following signature:

```python
from werkzeug.datastructures import FileStorage

def simulation_data_from_file(file: FileStorage) -> List[SimulationData]
```

SimulationData is as follows:

```python
class SimulationData:  # each represents an entry in samples db
    def __init__(self, timestamp: Number, process_value: Number, set_point: Number, out_value: Number, pid: PID):
        self.timestamp = timestamp
        self.pid = pid
        self.process_value = process_value
        self.pid_value = out_value
        self.set_point = set_point

class PID:
    def __init__(self, p: Number, i: Number, d: Number):
        self.p = p
        self.i = i
        self.d = d
```


The system assumes that each simulation data entry has no missing data. As such, our implementation fills empty fields with
their previous value (recursively until there is a value). If there is no value to fallback to, the entry is deleted.

The maintainer may choose to keep this behavior or implement his/her own fallback function.

When the code is ready to be deployed, simply replace the new implementation with the code [here](https://github.com/MarkOulitin/PID_project/blob/e6e17ac014f01798949ea83347c188fa55e8832e/server.py#L59).


### Recommendation Presentation <a name="frontend_implementation"></a>

The maintainer may choose to display the server response in a different manner. This could be in order to print it in a format that is easy to input to their controllers,
and even to use a new library which handles graphs differently.

UI - Maintenance

The validation of the form is the most basic file in the UI and it determines what is considered a valid data, in case of changes one can change the validation scheme and extend the options for user input.
(https://github.com/MarkOulitin/PID_project/blob/19388dc8ea5fb3531602fffdecb61cb5c2ee6c08/my-app/src/components/Home/Home.tsx#L21)

The UI uses material UI library, meaning if changes are needed to the base component's one can switch between the options available in the material ui library without breaking the code as long as it sticks to the same interface.
Link to material ui library:
https://mui.com/material-ui/

The folder structure is easy to use with informative names.
one can switch components in the main page easily by editing the code in the specific required folder.
All the UI components can be found under the components folder and be switched out according to necessary use as long as they use the same props.
Link:
https://github.com/MarkOulitin/PID_project/tree/master/my-app/src/components

import pandas as pd

class Commands:

    def input_command(self, command:str, attributes: dict) -> pd.DataFrame:
        if command == 'reset':
            if 'filepath' in attributes:
                print('reset file')
                return { 
                    'dataframe': pd.read_csv(attributes['filepath']),
                    'command': 'reset',
                    'info': 'load dataset from csv file'
                    }
        elif command == 'add':
            pass
        elif command == 'remove':
            if 'dataframe' in attributes and 'column' in attributes:
                pd.DataFrame.drop(attributes['dataframe'], columns=attributes['column'])
                return {
                    'dataframe': pd.DataFrame.drop(attributes['dataframe'], columns=attributes['column']),
                    'command': 'remove',
                    'info': 'drop column labeld' + attributes['column']
                    }
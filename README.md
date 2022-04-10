# python-data-analysis-studio
Data Analysis/Science Tool to generate python code and automate data cleaning, transformation and modeling pipelines using scikit-learn and pandas.

# Installation
1. clone this github repository into your local machine.
2. setup a new conda environment with all the packages listed in the requirments.txt file using the commmand below. requirements.txt file is located inside the web_app folder.

```conda create --name <env> --file requirements.txt```
  
# Getting started
To start usng the web app:
1. activate the conda environment that you just created using the command below in the terminal:

```conda activate <env>``` env:the environment name that you chose.

2. from the terminal,  browse to the folder web_app that contains the file manage.py and run the following command to start the web server:

```python manage.py runserver```

3. if the previous command run successfully, then you can head to the web browser and open the folloing url:

```http://localhost:8000/mlstudio/```

4. from the File Menu, choose open project and put the file path for a new project file or the file path for an existing project file. The Project file extension is ```.pickle```. 

# Contributors
- [Raafat H](https://github.com/raafat-hantoush)
- [Enrique H](https://github.com/NHer0)
- [Denny M](https://github.com/Denny-Meyer)

# MIT LICENSE

Copyright 2022 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

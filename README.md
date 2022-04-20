# python-data-analysis-studio
Data Analysis/Science Tool to generate python code and automate data cleaning, transformation and modeling pipelines using scikit-learn and pandas.

# Installation
1. clone this github repository into your local machine.
2. setup a new conda environment with all the packages listed in the requirments.txt file using the command below.

  ```conda create --name mlstudio --file requirements.txt```

```mlstudio: is the environment name. You can choose any other name that you prefer.```
 
#### or you can simply install the required libraries from requirments.txt to an existing conda environment using the following conda command:

  ``` conda install --name <yourenv>  --file requirements.txt ```
  
  
## Required Libraries
- Django
``` conda install -c anaconda django ```

- nbformat 
``` conda install -c conda-forge nbformat ```

- websocket-client
``` conda install -c conda-forge websocket-client ```

- Requests
```conda install -c anaconda requests ```

- pandas
```conda install pandas ```

- numpy
``` conda install numpy ```

- matplotlib
``` conda install -c conda-forge matplotlib ```

- seaborn
``` conda install -c anaconda seaborn ```

- pillow 
```conda install -c anaconda pillow ```

- Juypter
```conda install -c anaconda jupyter ```

# Getting started
To start usng the web app:
1. activate the conda environment that you just created using the command below in the terminal:

```conda activate <env>``` 

```env:the environment name that you chose. e.g. mlstudio```

2. from the terminal,  browse to the folder web_app that contains the file manage.py and run the following command to start the web server:

```python manage.py runserver```

3. if the previous command run successfully, then you can head to the web browser and open the folloing url:

```http://localhost:8000```

4. From the home page, browse to the folder where you want to create a new project in. Click ```New Project``` button. A new project will be created and opened. The Project file extension is ```.pickle```. 

# Contributors
- [Raafat H](https://github.com/raafat-hantoush)
- [Enrique H](https://github.com/NHer0)
- [Denny M](https://github.com/Denny-Meyer)

# MIT LICENSE

Copyright 2022 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

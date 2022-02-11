from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import pandas as pd

# Create your views here.
def index(request):
    df=pd.DataFrame({"name":["Kike","Nelson","Rafa"],"Age":[19,18,22]})
    print(df.to_html())
    #template = loader.get_template('/py_data_analysis_code_generator/index.html')
    #return HttpResponse("<b> Hello Kike")
    return render(request, 'py_data_analysis_code_generator/index.html')    
    ##return HttpResponse(template.render(request))
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render
from .models import Rotation_option, data_to_process

from .utils import util_predictor as predictor
from .utils import util_scraper

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', 
                    level=logging.INFO)

# for logging
_printProcess = True

# rotation_option_set: Options (with or w/o rotation) list
# data_proc: Selected option and an image prepared in database
rotation_option_set = Rotation_option.objects.all()
data_proc = data_to_process.objects.all()

# option: default option
# option_data and img_url: selected option and image in the html respectively
option = None
option_data = None
img_url = None

# identified aircraft data (type and wikipedia data)
aircraft_id = None
wikitable = None
wikiimg = None

# load tensorflow model and scraper class
pred = predictor.getResults()
scraper = util_scraper.retrieveDetails()

def printProcess(opt_data):
    logging.info(str(opt_data))
    logging.info(str(data_proc.last().rotationOption))
    logging.info(str(data_proc.last().img))

def main(request):
    global option_data
    global img_url
    global option
    global aircraft_id
    global wikitable
    global wikiimg

    img_url = None
    aircraft_id = None
    wikitable = None
    details = None
    wikiimg = 'https://img.freepik.com/free-icon/plane-silhouette_318-1385.jpg?w=2000'

    # Upload image
    if request.method == 'POST' and 'uploadImg' in request.POST:

        # delete previous (last) data
        

        # Variable for selected option from html
        # <form method = "POST>"
        option_data = request.POST

        # image selection
        img_url = request.FILES.get('plane_image')

        # file_name = default_storage.save(file.name, file)
        # file_url = default_storage.path(file_name)

        if option_data['rotation_option_set'] != 'none':
            option = rotation_option_set.get(id = option_data['rotation_option_set'])
        elif option_data['rotation_option_set'] == 'none':
            # id=1 : Apply rotations
            option = rotation_option_set.get(id=3)
        
        # Save data in 'data_to_process' database in correct order
        data_to_process.objects.create(rotationOption = option, 
                                       img = img_url)
    
    # Identify aircraft
    elif request.method == 'POST' and 'identify' in request.POST:
        img_url = data_proc.last().img
        option = data_proc.last().rotationOption
        option = str(option)       

        if option == 'Apply rotations':
            result = pred(file_dir=img_url.path, rotations=True)
        elif option == 'No rotations':
            result = pred(file_dir=img_url.path, rotations=False)
        
        # default value
        else:
            result = pred(file_dir=img_url.path, rotations=True)

        wikiimg = scraper(function='img', aircraft=str(result))
        details = scraper(function='infobox', aircraft=str(result))
        aircraft_id = result

    if _printProcess:
        printProcess(option_data)
       
    if img_url:
        img = data_proc.last().img
    elif not img_url:
        # pre-saved default image at
        # default_files/
        img = data_proc.first().img
        
    context = {'rots': rotation_option_set, 'plane_image': img,
               'wikiimg': wikiimg, 
               'selected_opt': option, 
               'details': details, 
               'aircraft_id': aircraft_id}
    
    return render(request, 'predictor/main.html', context)



from django.shortcuts import render
from django.http import HttpResponse
from .forms import get_link
from src import AddBg, RemoveBg, download_video
import cv2

def render_index(request):
    return render(request, 'index.html')

def render_image(request):
    return render(request, 'index_image.html')

def render_video(request):
    return render(request, 'index_video.html')

# Create your views here.
def img_url_get(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        getting_url = get_link(request.POST)
        # check whether it's valid:
        if getting_url.is_valid():
            # process the data in form.cleaned_data as required
            obj_link = getting_url.cleaned_data['obj_link']
            bg_link = getting_url.cleaned_data['bg_link']
            algo = request.POST['algo']
            print (algo)
            # obj, mask = rm.RemoveBg().remove_background(rm.RemoveBg().url_to_image(obj_link), rm.Algorithm['Laplacian'] ,6)
            # result = add.AddBg(obj, mask, bg_link, 1)
            img, mask = RemoveBg.RemoveBg().remove_background(RemoveBg.RemoveBg().url_to_image(obj_link), RemoveBg.Algorithm[algo],6)
            result = AddBg.AddBg(img, mask, bg_link, 1)
            img_path = None
            if (len(result) != 0):
                cv2.imwrite('removebg/static/result.jpg', result)
                img_path = 'result.jpg'

            # redirect to a new URL:
            return render(request, 'index_image.html', {'obj_link': obj_link, 'bg_link': bg_link, 'img_path':img_path})
        else:
            return HttpResponse('outs')

def video_url_get(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        getting_url = get_link(request.POST)
        # check whether it's valid:
        if getting_url.is_valid():
            # process the data in form.cleaned_data as required
            obj_link = getting_url.cleaned_data['obj_link']
            bg_link = getting_url.cleaned_data['bg_link'] # is image

            
            
            download_video.download_video_from_google_drive(obj_link, './static/obj_video.mp4')
            # download_video.download_video_from_google_drive('bg_link', './static/bg_video.mp4')
            
            output_path = './static/output.avi'
            img_path = None
            cap = cv2.VideoCapture('./static/obj_video.mp4')
            out = cv2.VideoWriter(output_path, -1, 20.0, (640,480))
            while True:
                _, frame = cv2.VideoCapture()
                img, mask = RemoveBg.RemoveBg().remove_background(obj_link, 6, frame)
                bg = RemoveBg.RemoveBg().url_to_image(bg_link)
                result = AddBg.AddBg(img, mask, bg, 1)           
                out.write(result)
            # redirect to a new URL:
            return render(request, 'index_video.html', {'obj_link': obj_link, 'bg_link': bg_link, 'img_path':img_path})
        else:
            return HttpResponse('Something went wrong')
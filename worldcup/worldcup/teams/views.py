from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from nymdesign.portfolio.models import *


def view_single_project(request, portfolio_slug, image_number=1):
    """
    View a single project including it's images and other projects in that category
    """
    image_number = int(image_number)

    # retrieve the project
    try:
        project = Project.objects.get(slug=portfolio_slug)
    except:
        return HttpResponse('project not found')

    # retrieve the images
    project_images = project.get_image_list()

    # set the selected image
    selected_image = None
    if project_images.count() > 0:
        if image_number > 0 and  project_images.count() >= image_number:
            selected_image = project_images[(image_number-1)]

    # retrieve projects in same category
    category_projects = Project.objects.filter(media_type=project.media_type)


    lu = { 'p' : project 
        , 'image_number' : image_number
        , 'selected_image' : selected_image
        , 'project_images' : project_images
        , 'category_projects' :category_projects
    }
    return render_to_response('portfolio/view_single_project.html', lu) 
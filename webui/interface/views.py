from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as et
from django.views.decorators.csrf import csrf_exempt
from time import localtime, strftime
from os.path import expanduser
import os
import subprocess
from interface.models import SpeechText, Waypoint
import json

def index(request):
    context = {'baseurl': request.get_host().rsplit(':', 1)[0] }
    return render(request, 'index.html', context)

def tracking(request):
    context = {'baseurl': request.get_host().rsplit(':', 1)[0] }
    return render(request, 'tracking.html', context)

@csrf_exempt
def navigation(request, action=""):
    if action == 'save':
      try:
        t = Waypoint(name=request.POST['name'], x=request.POST['x'], y=request.POST['y'], theta=request.POST['theta'])
        t.save()
        return HttpResponse(json.dumps({'id' : t.id, 'name' : t.name, 'x' : t.x, 'y' : t.y, 'theta' : t.theta}), content_type="application/json")
      except:
        return HttpResponse("error")
    elif action == 'remove':
      try:
        t = Waypoint.objects.get(id=request.POST['id'])
        t.delete()
        return HttpResponse(request.POST['id'])
      except:
        return HttpResponse("error")
    context = {'baseurl': request.get_host().rsplit(':', 1)[0], 'waypoints': Waypoint.objects.order_by('id') }
    return render(request, 'navigation.html', context)

def local(request):
    context = {'baseurl': request.get_host().rsplit(':', 1)[0] }
    return render(request, 'local.html', context)

@csrf_exempt    
def speech(request, predefined=""):
    if predefined == 'save':
      t = SpeechText(text=request.POST['text'])
      t.save()
      return HttpResponse("saved")
    elif predefined == 'remove':
      t = SpeechText.objects.get(id=request.POST['id'])
      t.delete()
      return HttpResponse("removed")
      
    context = {'baseurl': request.get_host().rsplit(':', 1)[0], 'speeches': map(lambda x: SpeechText(id=x.id, text=x.text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')) , SpeechText.objects.order_by('id').reverse()) }
    
    return render(request, 'speech.html', context)

@csrf_exempt    
def setup(request, config_name=""):
    home = expanduser("~")
    current_config = home + "/WebUI/ros_launch_files/eddie.launch"
    loaded = False
    
    if config_name == "reboot":
        subprocess.Popen(["nohup", "/bin/bash", "-i", "-c", "cd ~/WebUI/startup_script; ./ros.sh restart silent"])
        return HttpResponse("rebooted")
    elif config_name == "save":
      xml = et.parse(current_config)
      xml.write(home + "/WebUI/ros_launch_files/saved_configs/" + strftime("%d_%b_%Y_%H:%M:%S", localtime()))
      root = xml.getroot()
      for key, b in request.POST.items():
        a = key.split("___")
        node = root.find("./node[@name='"+a[0]+"']/param[@name='"+a[1]+"']")
        if node is not None:
          node.set("value", b)
      
      os.remove(current_config)
      xml.write(current_config)
      
      return HttpResponse("success")
    elif config_name != "":
      current_config = home + "/WebUI/ros_launch_files/saved_configs/" + config_name
      loaded = True

    xml = et.parse(current_config)
    root = xml.getroot()
    
    params = []
    for node in root.findall("node"):
        for param in node.findall('param'):
            params.append((node.attrib['name'], param.attrib['name'], param.attrib['value']))
            
    configs = []
    for name in os.listdir(home + "/WebUI/ros_launch_files/saved_configs"):
      configs.append(name)
    configs.sort()
    configs.reverse()
    context = {'params': params, 'configs': configs, 'loaded': loaded}
    return render(request, 'setup.html', context)


@csrf_exempt    
def voice(request, predefined=""):
    if predefined == 'save':
      t = SpeechText(text=request.POST['text'])
      t.save()
      return HttpResponse("saved")
    elif predefined == 'remove':
      t = SpeechText.objects.get(id=request.POST['id'])
      t.delete()
      return HttpResponse("removed")
      
    context = {'baseurl': request.get_host().rsplit(':', 1)[0], 'speeches': map(lambda x: SpeechText(id=x.id, text=x.text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')) , SpeechText.objects.order_by('id').reverse()) }
    
    return render(request, 'voice.html', context)






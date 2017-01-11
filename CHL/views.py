from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator
from django.db.models import Q
import boto3,requests,json,humanize,base64
from collections import defaultdict
from chlib import aggregate_visits as N1
from chlib.aggregate_edges import readmits as N2
from chlib.aggregate_edges import revisits as N3
from chlib import aggregate_patients as N4
from chlib.entity import presentation
from chlib.entity.enums import STRINGS
from chlib import codes
from chlib.entity import enums
from django.template.defaulttags import register
from chlib.entity.visit import Patient
import google
import tasks
import os,logging
import boto3,botocore
from boto3.session import Session
from django.shortcuts import render

# Create your views here.



def app(request):
    context = {}
    return render(request, 'app.html',context,using='jtlte')

def get_patient(db,patient_id):
    """
    get all data associated with the patient
    :param patient_id:
    :return:
    """
    result = tasks.data_get_patient.apply_async(args=[db,patient_id],queue=tasks.Q_DATA)
    result.wait()
    return result.get()


def get_databases():
    """
    get a list of databases
    :return:
    """
    examples = tasks.data_examples.apply_async(queue=tasks.Q_DATA)
    examples.wait()
    return examples.get()


@login_required
def patient_viewer(request):
    payload = {'DB_LIST':get_databases()}
    if request.GET.get('patient_id') and request.GET.get('db'):
        patient_id = request.GET.get('patient_id')
        db = request.GET.get('db')
        patient_coded = get_patient(db,patient_id)
        temp = Patient()
        v = base64.decodestring(patient_coded["data"])
        temp.ParseFromString(v)
        raw_string = temp.raw
        temp.raw = ""
        payload['coder'] = codes.Coder()
        payload['patient_obj'] = temp
        payload['next_key'] = patient_coded["next"]
        payload['patient'] = {'patient_id':patient_id,'db':db,'data':str(temp),'raw_string':raw_string}
    context = {'payload':payload}
    return render(request,'patient_viewer.html', context=context, using='jtlte')

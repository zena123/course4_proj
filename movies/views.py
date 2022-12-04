import urllib.parse

from celery.exceptions import TimeoutError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from course4_proj.celery import app
from movies.models import Movie
from movies.tasks import search_and_save


import urllib.parse

from celery.exceptions import TimeoutError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from course4_proj.celery import app
from movies.models import Movie
from movies.tasks import search_and_save



def search(request):

  search_term = request.GET["search_term"]
  res = search_and_save.delay(search_term)
  try:
    res.get(timeout=2)
  except TimeoutError:
    return redirect(
        reverse("search_wait", args=(res.id,))
        + "?search_term="
        + urllib.parse.quote_plus(search_term)
    )
  return redirect(
      reverse("search_results")
      + "?search_term="
      + urllib.parse.quote_plus(search_term),
      permanent=False,
    )


def search_wait(request, result_uuid):

  search_term = request.GET["search_term"]
  res = app.AsyncResult(result_uuid)

  try:
    res.get(timeout=-1)
  except TimeoutError:
    return HttpResponse("Task pending, please refresh.", status=200)

  return redirect(
      reverse("search_results")
      + "?search_term="
      + urllib.parse.quote_plus(search_term)
    )

def search_results(request):
  search_term = request.GET["search_term"]
  movies = Movie.objects.filter(title__icontains=search_term)
  return HttpResponse(
      "\n".join([movie.title for movie in movies]), content_type="text/plain"
  )

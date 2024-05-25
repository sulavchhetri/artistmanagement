from django.shortcuts import render, redirect
from rest_framework.views import APIView
from datetime import datetime
from django.core.paginator import Paginator
from .models import Artist, Music
from django.db import connection


class RegisterView(APIView):
    def post(self, request):
        name = request.POST.get('name').strip()
        dob = request.POST.get('dob').strip()
        if datetime.strptime(dob, '%Y-%m-%d').date() > datetime.now().date():
            return render(request, 'artist/register.html', {'error': 'Enter correct date of birth'})
        gender = request.POST.get('gender').strip()
        address = request.POST.get('address').strip()
        first_release_year = request.POST.get('first_release_year')
        no_of_albums_released = request.POST.get('no_of_albums_released')
        sql_query = """
            INSERT INTO artist_Artist (name, dob, gender, address, first_release_year, no_of_albums_released, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [name, dob, gender, address, first_release_year, no_of_albums_released, datetime.now(), datetime.now()]
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
        return redirect("/artist/all/")

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        return render(request, 'artist/register.html', context={'active_user': request.user.is_authenticated})


class ViewArtist(APIView):
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        artist = Artist.objects.raw(f'select * from artist_Artist where id={pk} LIMIT 1')[0]
        if artist:
            context = {
                'name': artist.name,
                'address': artist.address,
                'dob': artist.dob.strftime('%Y-%m-%d'),
                'gender': artist.gender,
                'updated_at': artist.updated_at.strftime('%Y-%m-%d'),
                'created_at': artist.created_at.strftime('%Y-%m-%d'),
                'first_released_year': artist.first_release_year,
                'no_of_albums_released': artist.no_of_albums_released,
                'active_user': request.user.is_authenticated
            }
            return render(request, 'artist/artist.html', context=context)


class ViewArtists(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        artists = Artist.objects.raw('select * from artist_Artist order by created_at desc')
        paginator = Paginator(artists, 5)
        try:
            page_number = int(request.GET.get('page'))
        except Exception as e:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        artist_details = [(artist.name, artist.id) for artist in artists]
        artist_details = artist_details[(page_number - 1) * 5:5 * page_number]
        return render(request, 'artist/artists.html',
                      {'users': artist_details, 'page_obj': page_obj, 'active_user': request.user.is_authenticated})


class DeleteArtist(APIView):
    def post(self, request, pk=None):
        sql_query = """
            DELETE FROM artist_Artist
            WHERE id = %s
        """
        value = pk
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [value])

        return redirect('/artist/all/')


class ModifyArtist(APIView):
    def get(self, request, pk=None):
        artist = Artist.objects.raw(f'select * from artist_Artist where id={pk} LIMIT 1')[0]
        context = {
            'name': artist.name,
            'address': artist.address,
            'dob': artist.dob.strftime('%Y-%m-%d'),
            'gender': artist.gender,
            'updated_at': artist.updated_at.strftime('%Y-%m-%d'),
            'created_at': artist.created_at.strftime('%Y-%m-%d'),
            'first_release_year': artist.first_release_year,
            'no_of_albums_released': artist.no_of_albums_released,
            'active_user': request.user.is_authenticated,
            'modify': True
        }
        return render(request, 'artist/register.html', context)

    def post(self, request, pk=None):
        name = request.POST.get('name').strip()
        dob = request.POST.get('dob').strip()
        if datetime.strptime(dob, '%Y-%m-%d').date() > datetime.now().date():
            return render(request, 'artist/register.html', {'error': 'Enter correct date of birth'})
        gender = request.POST.get('gender').strip()
        address = request.POST.get('address').strip()
        first_release_year = request.POST.get('first_release_year')
        no_of_albums_released = request.POST.get('no_of_albums_released')

        sql_query = """
                        UPDATE artist_Artist
                        SET name = %s, dob = %s, gender = %s, address = %s, first_release_year=%s, no_of_albums_released=%s, updated_at=%s
                        WHERE id = %s
                        """
        values = [name, dob, gender, address, first_release_year, no_of_albums_released, datetime.now(), pk]
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)

        return redirect('/artist/all/')

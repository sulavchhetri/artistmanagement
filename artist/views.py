from django.shortcuts import render, redirect
from rest_framework.views import APIView
from datetime import datetime
from django.core.paginator import Paginator
from django.db import connection


class RegisterView(APIView):
    def post(self, request):
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        if datetime.strptime(dob, '%Y-%m-%d').date() > datetime.now().date():
            return render(request, 'artist/register.html', {'error': 'Enter correct date of birth'})
        gender = request.POST.get('gender')
        address = request.POST.get('address')
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
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artist_Artist WHERE id = %s LIMIT 1', [pk])
            artist = cursor.fetchone()
        if artist:
            artist_id, name, dob, gender, address, first_release_year, created_at, updated_at, no_of_albums_released = artist
            context = {
                'id': artist_id,
                'name': name,
                'address': address,
                'dob': dob.strftime('%Y-%m-%d'),
                'gender': gender,
                'updated_at': updated_at.strftime('%Y-%m-%d'),
                'created_at': created_at.strftime('%Y-%m-%d'),
                'first_released_year': first_release_year,
                'no_of_albums_released': no_of_albums_released,
                'active_user': request.user.is_authenticated
            }
            return render(request, 'artist/artist.html', context=context)


class ViewArtists(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        artists = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artist_Artist order by created_at asc')
            artists = cursor.fetchall()
        paginator = Paginator(artists, 5)
        try:
            page_number = int(request.GET.get('page'))
        except Exception as e:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        artist_details = [(artist[1], artist[0]) for artist in artists]
        artist_details = artist_details[(page_number - 1) * 5:5 * page_number]
        return render(request, 'artist/artists.html',
                      {'users': artist_details, 'page_obj': page_obj, 'active_user': request.user.is_authenticated})


class DeleteArtist(APIView):
    def post(self, request, pk=None):
        delete_music_query = """
                    DELETE FROM artist_Music
                    WHERE artist_id = %s
                """
        delete_artist_query = """
            DELETE FROM artist_Artist
            WHERE id = %s
        """
        value = pk
        with connection.cursor() as cursor:
            cursor.execute(delete_music_query, [value])
            cursor.execute(delete_artist_query, [value])

        return redirect('/artist/all/')


class ModifyArtist(APIView):
    def get(self, request, pk=None):
        artist = None
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artist_Artist WHERE id = %s LIMIT 1', [pk])
            artist = cursor.fetchone()
        if artist:
            _, name, dob, gender, address, first_release_year, created_at, updated_at, no_of_albums_released = artist
            context = {
                'name': name,
                'address': address,
                'dob': dob.strftime('%Y-%m-%d'),
                'gender': gender,
                'updated_at': updated_at.strftime('%Y-%m-%d'),
                'created_at': created_at.strftime('%Y-%m-%d'),
                'first_release_year': first_release_year,
                'no_of_albums_released': no_of_albums_released,
                'active_user': request.user.is_authenticated,
                'modify': True
            }
            return render(request, 'artist/register.html', context)

    def post(self, request, pk=None):
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        if datetime.strptime(dob, '%Y-%m-%d').date() > datetime.now().date():
            return render(request, 'artist/register.html', {'error': 'Enter correct date of birth'})
        gender = request.POST.get('gender')
        address = request.POST.get('address')
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


class ViewSongs(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        sql_query = f"SELECT * from artist_Music where artist_id = {pk} order by created_at desc"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            songs = cursor.fetchall()

        paginator = Paginator(songs, 5)
        try:
            page_number = int(request.GET.get('page'))
        except Exception as e:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        songs_details = [(song[1], song[0], pk) for song in songs]
        songs_details = songs_details[(page_number - 1) * 5:5 * page_number]
        return render(request, 'songs/songs.html',
                      {'users': songs_details, 'page_obj': page_obj, 'active_user': request.user.is_authenticated})


class AddSong(APIView):
    def post(self, request, pk=None):
        title = request.POST.get('title')
        album_name = request.POST.get('album_name')
        genre = request.POST.get('genre')

        sql_query = """
            INSERT INTO artist_Music (title, album_name, genre, artist_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = [title, album_name, genre, pk, datetime.now(), datetime.now()]
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
        return redirect("/artist/all/")

    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        return render(request, 'songs/register.html', context={'active_user': request.user.is_authenticated})


class ViewSong(APIView):
    def get(self, request, pk=None, song_id=None):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artist_Artist WHERE id = %s LIMIT 1', [pk])
            artist = cursor.fetchone()

            cursor.execute('SELECT * FROM artist_Music WHERE id = %s LIMIT 1', [song_id])
            music = cursor.fetchone()

        if artist and music:
            _, title, album_name, genre, created_at, updated_at, _ = music
            context = {
                'artist_name': artist[1],
                'title': title,
                'genre': genre,
                'updated_at': updated_at.strftime('%Y-%m-%d'),
                'created_at': created_at.strftime('%Y-%m-%d'),
                'album_name': album_name,
                'active_user': request.user.is_authenticated
            }
            return render(request, 'songs/song.html', context=context)


class DeleteSong(APIView):
    def post(self, request, pk=None, song_id=None):
        sql_query = """
                DELETE FROM artist_Music
                WHERE id = %s
            """
        value = song_id
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [value])

        return redirect(f'/artist/{pk}/songs/')


class ModifySong(APIView):
    def get(self, request, pk=None, song_id=None):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artist_Music WHERE id = %s LIMIT 1', [song_id])
            music = cursor.fetchone()
        if music:
            _, title, album_name, genre, *_ = music
            context = {
                'title': title,
                'album_name': album_name,
                'genre': genre,
                'active_user': request.user.is_authenticated,
                'modify': True
            }
            return render(request, 'songs/register.html', context)

    def post(self, request, pk=None, song_id=None):
        title = request.POST.get('title')
        album_name = request.POST.get('album_name')
        genre = request.POST.get('genre')
        sql_query = """
                        UPDATE artist_Music
                        SET title = %s, album_name = %s, genre = %s, updated_at = %s
                        WHERE id = %s
                        """
        values = [title, album_name, genre, datetime.now(), song_id]
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)

        return redirect(f'/artist/{pk}/songs/{song_id}/')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from ski.models import Mountain, State, Comments, Fav
from ski.forms import CommentForm
from ski.util import CommentDeleteView
from django.db import connection
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from ski.map import plot_map
from django.db.models.functions import Cast
from django.db.models import FloatField

class SkiHomeView(View):
    def get(self, request):
        comments = Comments.objects.all().order_by('-updated_at')[:5]
        ctx = {'comments':comments}
        fav_mountains = Fav.objects.values('mountain_id').annotate(Count('mountain_id')).order_by('-mountain_id__count')[:5]
        for index, match in enumerate(fav_mountains):
            fav_mountains[index]['mountain'] = Mountain.objects.get(id=match['mountain_id'])
        ctx['high_snow'] = Mountain.objects.all().order_by('-new_snow')[:5]
        # ctx['high_snow'] = Mountain.objects.annotate(new_snow=Cast('new_snow', FloatField())).order_by('-new_snow')[:5]
        ctx['fav_mountains'] = fav_mountains
        map1 = plot_map()
        ctx['plot_url'] = map1[0]
        ctx['div_id'] = map1[1]
        return render(request,'ski/home.html', ctx)

class SkiMountains(View):
    def get(self, request):
        with connection.cursor() as cursor:
            statement = """SELECT ski_state.state_name, COUNT(state_name_id)
                        FROM ski_mountain JOIN ski_state on
                        ski_mountain.state_name_id == ski_state.id
                        GROUP BY state_name_id"""
            cursor.execute(statement)
            rows = cursor.fetchall()
            ctx = {'state_dict_1': rows[::3], 'state_dict_2': rows[1::3],'state_dict_3': rows[2::3]}
        return render(request,'ski/main_state_mountain_list.html', ctx)

class StateList(View):
    def get(self, request, state):
        state = State.objects.get(state_name=state)
        mountains = Mountain.objects.filter(state_name=state)
        ctx = {'mountains_1': mountains[::2], 'mountains_2': mountains[1::2]}
        ctx['state_name'] = state
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_mountain.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx['favorites'] = favorites
        return render(request, 'ski/state_list.html', ctx)

class Montain(View):
    def get(self, request, state, mountain):
        state_mod = State.objects.get(state_name=state)
        mountain = Mountain.objects.get(name=mountain,state_name=state_mod)
        comments = Comments.objects.filter(mountain=mountain).order_by('-updated_at')
        comment_form = CommentForm()
        ctx = {'mountain': mountain, 'comments': comments, 'comment_form': comment_form}
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_mountain.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx['favorites'] = favorites
        return render(request,'ski/mountain.html', context=ctx)

class CommentCreateView(View):
    def post(self, request, state, mountain) :
        f = get_object_or_404(Mountain, name=mountain)
        comment_form = CommentForm(request.POST)
        comment = Comments(text=request.POST['comment'], owner=request.user, mountain=f)
        comment.save()
        return redirect(reverse_lazy('mountain', args=[state, mountain]))

class CommentDeleteView(CommentDeleteView):
    model = Comments
    template_name = "comment_delete.html"

    def get_success_url(self):
        mountain = self.object.mountain
        return reverse_lazy('mountain', args=[mountain.state_name, mountain.name])

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, state, mountain) :
        t = get_object_or_404(Mountain, name=mountain)
        fav = Fav(user=request.user, mountain=t)
        try:
            fav.save()
        except IntegrityError as e:
            print('Integrity error: ', e)
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request,state, mountain) :
        print("Delete Favorite",mountain)
        t = get_object_or_404(Mountain, name=mountain)
        try:
            fav = Fav.objects.get(user=request.user, mountain=t).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()

class MyFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        favorites = list()
        ctx = {}
        rows = request.user.favorite_mountain.values("id")
        favorites_ids = [ row['id'] for row in rows ]
        favorite_mountains = Mountain.objects.filter(id__in=favorites_ids).order_by('state_name')
        ctx['mountains'] = favorite_mountains
        ctx['favorites'] = favorites_ids
        return render(request, 'ski/my_favorites.html', ctx)

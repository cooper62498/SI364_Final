from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        qs = super(CommentDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

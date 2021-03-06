from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        qs = super(CommentDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

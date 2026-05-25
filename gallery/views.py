import cloudinary.uploader
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AlbumForm, PhotoForm
from .models import Album, Photo


# --- RBAC Mixins ---

class AlbumOwnerMixin(UserPassesTestMixin):
    """Only the album owner or staff can edit/delete."""
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.owner or self.request.user.is_staff


class PhotoOwnerMixin(UserPassesTestMixin):
    """Only the album owner or staff can edit/delete a photo."""
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.album.owner or self.request.user.is_staff


# --- Album Views ---

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 9

    def get_queryset(self):
        qs = Album.objects.select_related('owner').prefetch_related('photos')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Album '{form.instance.name}' created!")
        return super().form_valid(form)


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photos'] = self.object.photos.all()
        ctx['photo_form'] = PhotoForm()
        ctx['is_owner'] = (self.request.user == self.object.owner or self.request.user.is_staff)
        return ctx


class AlbumUpdateView(LoginRequiredMixin, AlbumOwnerMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'

    def get_success_url(self):
        messages.success(self.request, "Album updated successfully.")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(LoginRequiredMixin, AlbumOwnerMixin, DeleteView):
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        for photo in self.object.photos.all():
            if photo.image and photo.image.public_id:
                try:
                    cloudinary.uploader.destroy(photo.image.public_id)
                except Exception as e:
                    print(f"Cloudinary error: {e}")
        messages.success(self.request, f"Album '{self.object.name}' deleted.")
        return super().form_valid(form)


# --- Photo Views ---

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=kwargs['album_pk'])
        if request.user != self.album.owner and not request.user.is_staff:
            messages.error(request, "You don't have permission to add photos here.")
            return redirect('album_detail', pk=self.album.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        form.instance.uploader = self.request.user
        messages.success(self.request, f"Photo '{form.instance.title}' uploaded!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.album.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['album'] = self.album
        return ctx


class PhotoUpdateView(LoginRequiredMixin, PhotoOwnerMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'

    def get_success_url(self):
        messages.success(self.request, "Photo updated.")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['album'] = self.object.album
        ctx['photo'] = self.object
        return ctx

class PhotoDeleteView(LoginRequiredMixin, PhotoOwnerMixin, DeleteView):
    model = Photo
    template_name = 'gallery/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

    def form_valid(self, form):
        if self.object.image and self.object.image.public_id:
            try:
                cloudinary.uploader.destroy(self.object.image.public_id)
            except Exception as e:
                print(f"Cloudinary error: {e}")
        messages.success(self.request, f"Photo '{self.object.title}' deleted.")
        return super().form_valid(form)
from braces.views._access import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.views.generic.edit import CreateView, UpdateView
from cfp.forms import PaperApplicationForm
from cfp.models import Applicant, PaperApplication, CallForPaper


class PaperApplicationBaseView(LoginRequiredMixin):
    model = PaperApplication
    form_class = PaperApplicationForm
    template_name = 'cfp/paperapplication_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.cfp = CallForPaper.objects.get(pk=kwargs['cfp_id'])
        return super(PaperApplicationBaseView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        c = super(PaperApplicationBaseView, self).get_context_data(**kwargs)
        c['cfp_active'] = self.cfp.is_active()
        return c

    def form_valid(self, form):
        if not self.cfp.is_active():
            return HttpResponse('Cfp is not active', status=403)
        applicant = self._build_or_update_applicant(form)
        form.instance.applicant_id = applicant.pk
        form.instance.cfp_id = self.cfp.pk

        return super(PaperApplicationBaseView, self).form_valid(form)

    def get_initial(self):
        initial = super(PaperApplicationBaseView, self).get_initial()
        try:
            applicant = self.request.user.applicant
            initial.update({
                'about_applicant': applicant.about,
                'biography': applicant.biography,
                'speaker_experience': applicant.speaker_experience,
                'image': applicant.image,
            })
        except Applicant.DoesNotExist:
            pass

        return initial

    def _build_or_update_applicant(self, form):
        user = self.request.user
        args = {
            'user': user,
            'about': form.cleaned_data['about_applicant'],
            'biography': form.cleaned_data['biography'],
            'speaker_experience': form.cleaned_data['speaker_experience'],
            'image': form.cleaned_data['image'],
        }

        applicant, created = Applicant.objects.update_or_create(user=user, defaults=args)
        return applicant

    def get_success_url(self):
        return reverse('user_profile')


class PaperApplicationCreateView(PaperApplicationBaseView, CreateView):
    pass


class PaperApplicationUpdateView(PaperApplicationBaseView, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        self._check_allowed(request.user)
        return super(PaperApplicationUpdateView, self).dispatch(request, *args, **kwargs)

    def _check_allowed(self, user):
        allow = False
        application = self.get_object()
        try:
            if application.applicant_id == user.applicant.pk:
                allow = True
        except Applicant.DoesNotExist:
            pass

        if not allow:
            raise Http404()


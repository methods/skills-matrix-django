from django.views import View
from job_roles.models import Job, Competency


class CustomView(View):
    def dispatch(self, request, *args, **kwargs):
        for key in request.POST.keys():
            if 'delete' in key:
                handler = getattr(self, 'delete', self.http_method_not_allowed)
                return handler(request, *args, **kwargs)
            if 'edit' in key:
                handler = getattr(self, 'edit', self.http_method_not_allowed)
                return handler(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def set_job_and_competencies(self, job_title):
        job = Job.objects.get(job_title=job_title.title().replace('-', ' '))
        competencies = Competency.objects.filter(job_role_title=job.id).order_by('id')
        return job, competencies

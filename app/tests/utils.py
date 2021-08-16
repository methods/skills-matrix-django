from job_roles.models import Job


def creates_job_role_title_instance():
    test_job = Job.objects.create(job_title='Junior Developer')
    return {'test_job_role': test_job}

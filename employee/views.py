from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Employee
from django.utils import timezone


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'employee/index.html'
    context_object_name = 'latest_Employee_list'

    def get_queryset(self):
        """
        Return the last five published Employees (not including those set to be
        published in the future).
        """
        return Employee.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # return Employee.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Employee
    template_name = 'employee/detail.html'

    def get_queryset(self):
        """
        Excludes any Employees that aren't published yet.
        """
        return Employee.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Employee
    template_name = 'employee/results.html'


def vote(request, Employee_id):
    employee = get_object_or_404(Employee, pk=Employee_id)
    try:
        selected_choice = employee.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Employee.DoesNotExist):
        # Redisplay the Employee voting from
        return render(request, 'polls/detail.html', {
            'employee': employee,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(Employee.id,)))


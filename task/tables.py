import django_tables2 as tables
from django_tables2.utils import Accessor
from task.models import Task

#class ATModel(task.models.Task):
#    pass
#   assignment_set = 'hi'

class ActiveTaskTable(tables.Table):
 #   date_start = tables.Column()
#   _location = tables.LinkColumn('task_detail', args={Accessor('pk')})
    id = tables.URLColumn()
#    assignment_set = tables.LinkColumn('detail', args=[A('pk'), A('_location')])
#    assignment_set = tables.Column('')
    
    def get_context_data(self, **kwargs):
        assignment_set = []
        for s in model.assignment_set:
            assignment_set = s.slave
        return assignment_set

    class Meta:
        model = Task 
        attrs = {'assignment_set': 'hi'}
#       assignment_set = super(Meta, self).get_context_data(**kwargs)

        def get_context_data(self, **kwargs):
            assignment_set = []
            for s in model.assignment_set:
                assignment_set = s.slave
            return assignment_set

#       assignment_set = []
#       for s in model.assignment_set:
#           assignment_set = s.slave
#        print(assignment_set)
        #        _date_start= tables.Column()
#        slave_set = tables.Column()
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}



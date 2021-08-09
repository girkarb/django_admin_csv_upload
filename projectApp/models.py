from django.db import models

"""
This  model will contain sample information
"""
# Create your models here.
class LearningObjective(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Child(models.Model):
    name = models.CharField(max_length=20, unique=True)
    parent_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=20, null=True, blank=True)
    grade = models.CharField(max_length=20, null=True, blank=True)
    teacher_allocated = models.CharField(max_length=50, null=True, blank=True)
    current_teacher = models.CharField(max_length=50, null=True, blank=True)
    sales_manager = models.CharField(max_length=50, null=True, blank=True)
    lsq_id = models.CharField(max_length=100, null=True, blank=True)
    last_active_date = models.DateTimeField(null=True, blank=True)
    ptm_status = models.BooleanField(default=False)
    last_ptm_date = models.DateTimeField(null=True, blank=True)
    batch_name = models.CharField(max_length=100, null=True, blank=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    sessions_credited = models.CharField(max_length=100, null=True, blank=True)
    allowed_total_classes = models.IntegerField(default=0)
    taken_total_classes = models.IntegerField(default=0)
    remaining_classes = models.IntegerField(default=-1)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.CharField(max_length=30, null=True, blank=True)
    learning_objective = models.ManyToManyField(LearningObjective)

    def __str__(self):
        return self.name

    def get_learning_objective0(self):
        try:
            return str(self.learning_objective.all()[0])
        except:
            return "NA"

    def get_learning_objective1(self):
        try:
            return str(self.learning_objective.all()[1])
        except:
            return "NA"

    def get_learning_objective2(self):
        try:
            return str(self.learning_objective.all()[2])
        except:
            return "NA"

    def get_learning_objective3(self):
        try:
            return str(self.learning_objective.all()[3])
        except:
            return "NA"

    def get_learning_objective4(self):
        try:
            return str(self.learning_objective.all()[4])
        except:
            return "NA"

    def get_learning_objective5(self):
        try:
            return str(self.learning_objective.all()[5])
        except:
            return "NA"

    def get_learning_objective6(self):
        try:
            return str(self.learning_objective.all()[6])
        except:
            return "NA"


class Payment(models.Model):
    child_name = models.ForeignKey(Child, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_fees = models.FloatField(default=0.0)
    fees_paid = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    sessions_credited = models.CharField(max_length=100, null=True, blank=True)
    latest_payment_date = models.DateTimeField(null=True, blank=True)
    balance_fee_follow_date = models.DateTimeField(null=True, blank=True)
    renewal1_date = models.DateTimeField(null=True, blank=True)
    renewal2_date = models.DateTimeField(null=True, blank=True)
    renewal_status = models.BooleanField(default=False)
    payment_pending = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.child.name
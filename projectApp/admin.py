from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from . import models
from .models import Student, LearningObjective, Payment, Child
import csv
import datetime
from .forms import CsvImportForm


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stud_id', 'fname', 'lname', 'gender', 'age', 'status', 'goToProfileReviewed', 'goToNotify')
    search_fields = ('stud_id', 'fname', 'lname', 'gender')

    def get_urls(self):
        """
        To fetch urls and add import csv url.
        :return:
        """

        urls = super().get_urls()
        my_urls = [path('import-csv/', self.import_csv), ]
        my_urls1 = [path('update_reviewed/<stud_id>', self.updateProfileReviewed), ]
        my_urls2 = [path('update_notify/<stud_id>', self.updateNotify), ]
        return my_urls + my_urls1 + my_urls2 + urls

    @mark_safe
    def goToProfileReviewed(self, obj):

        return format_html(
            '<a class="button" href="/admin/projectApp/student/update_reviewed/%s" target="blank">Profile '
            'Reviewed</a>&nbsp;' % (obj.pk))

    goToProfileReviewed.short_description = 'ProfileReviewed'
    goToProfileReviewed.allow_tags = True

    @mark_safe
    def goToNotify(self, obj):

        return format_html(
            '<a class="button" href="/admin/projectApp/student/update_notify/%s" target="blank">Notify</a>&nbsp;' % (obj.pk))

    goToNotify.short_description = 'Notify'
    goToNotify.allow_tags = True

    def updateProfileReviewed(self, request, stud_id):
        Student.objects.filter(id=stud_id).update(status='Reviewed')
        url = reverse('admin:index')
        return HttpResponseRedirect(url)

    def updateNotify(self, request, stud_id):
        Student.objects.filter(id=stud_id).update(status='Notify')
        url = reverse('admin:index')
        return HttpResponseRedirect(url)

    def import_csv(self, request):
        """
        To write data from csv to student model.
        :param request:
        :return:
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            del lines[0]  # to delete header
            for line in lines:
                if line:
                    fields = line.split(",")
                    try:
                        is_exist = Student.objects.get(id=fields[0])
                    except Exception as e:
                        is_exist = None
                    if is_exist is None:
                        Student.objects.create(
                            id=fields[0].strip(),
                            stud_id=fields[1].strip(),
                            fname=fields[2].strip(),
                            lname=fields[3].strip(),
                            gender=fields[4].strip(),
                            age=fields[5].strip(),
                            status='Created'

                        )
                    else:
                        stud_obj = Student.objects.get(id=fields[0])
                        Student.objects.filter(id=fields[0]).update(
                            stud_id=fields[1].strip(),
                            fname=fields[2].strip(),
                            lname=fields[3].strip(),
                            gender=fields[4].strip(),
                            age=fields[5].strip(),
                            status=stud_obj.status

                        )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        payload = {"form": form}

        return render(request, "admin/csv_form.html", payload)


admin.site.register(Student, StudentAdmin)


class LearningAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_name')

    def get_urls(self):
        """
        To fetch urls and add import csv url.
        :return:
        """

        urls = super().get_urls()
        child_import_csv = [path('import-csv/', self.child_import_csv), ]
        return child_import_csv + urls

    def child_import_csv(self, request):
        """
        To write data from csv to child model.
        :param request:
        :return:
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8", errors='ignore')
            lines = file_data.split("\n")
            del lines[0]  # to delete header
            for line in lines:
                if line:
                    fields = line.split(",")
                    dict_val = {fields[6].split(":")[0]: fields[6].split(":")[1],
                                fields[7].split(":")[0]: fields[7].split(":")[1],
                                fields[8].split(":")[0]: fields[8].split(":")[1],
                                fields[9].split(":")[0]: fields[9].split(":")[1],
                                fields[10].split(":")[0]: fields[9].split(":")[1],
                                fields[11].split(":")[0]: fields[11].split(":")[1],
                                fields[12].split(":")[0]: fields[12].split(":")[1]}
                    code_list = [fields[6].split(":")[0], fields[7].split(":")[0], fields[8].split(":")[0],
                                 fields[9].split(":")[0], fields[10].split(":")[0], fields[11].split(":")[0],
                                 fields[12].split(":")[0]]
                    for k, v in dict_val.items():
                        try:
                            if k and v:
                                LearningObjective.objects.get_or_create(code=k, description=v, status=1,
                                                                        added_on=str(datetime.datetime.now()),
                                                                        updated_on=str(datetime.datetime.now()))
                        except Exception as e:
                            print(e)
                    try:
                        learning_obj = LearningObjective.objects.filter(code__in=code_list)
                        child_instance = Child.objects.get_or_create(
                            name=fields[2].strip(),
                            parent_name='NA',
                            mobile=fields[13].strip(),
                            email=fields[1].strip(),
                            grade='NA',
                            teacher_allocated=fields[3].strip(),
                            current_teacher='NA',
                            sales_manager='NA',
                            lsq_id='NA',
                            last_active_date=str(datetime.datetime.now()),
                            ptm_status=0,
                            last_ptm_date=str(datetime.datetime.now()),
                            batch_name='NA',
                            course_name=fields[5].strip(),
                            sessions_credited=fields[14].strip(),
                            start_date=fields[4].strip(),
                            status=1,
                            added_on=str(datetime.datetime.now()),
                            updated_on=str(datetime.datetime.now()),
                            timestamp=str(fields[0].strip()),
                        )
                        child_instance.learning_objective.set(tuple(learning_obj))
                    except Exception as e:
                        print(e)
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        payload = {"form": form}

        return render(request, "admin/csv_form.html", payload)


class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


class PaymentAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in Payment._meta.get_fields()]
    list_display = ('child_name', 'total_fees')


admin.site.register(LearningObjective, LearningObjectiveAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Child, ChildAdmin)

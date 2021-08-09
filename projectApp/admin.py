from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .admin_view import StudentAdminManager, ChildManager
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
            '<a class="button" href="/admin/projectApp/student/update_notify/%s">Notify</a>&nbsp;' % (
                obj.pk))

    goToNotify.short_description = 'Notify'
    goToNotify.allow_tags = True

    def updateProfileReviewed(self, request, stud_id):
        obj = StudentAdminManager().updateProfileReviewed(stud_id)
        if obj ==True:
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

    def updateNotify(self, request, stud_id):
        obj = StudentAdminManager().updateNotify(stud_id)
        if obj == True:
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
            obj = StudentAdminManager().import_csv(lines)
            if obj == True:
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
            obj = ChildManager().csv_import(lines)
            if obj ==True:
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

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Student
import csv
from .forms import CsvImportForm


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stud_id', 'fname', 'lname', 'gender', 'age')
    search_fields = ('stud_id', 'fname', 'lname', 'gender')

    def get_urls(self):
        """
        To fetch urls and add import csv url.
        :return:
        """
        urls = super().get_urls()
        my_urls = [path('import-csv/', self.import_csv),]
        return my_urls + urls

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
                            age=fields[5].strip()
                        )
                    else:
                        Student.objects.filter(id=fields[0]).update(
                            stud_id=fields[1].strip(),
                            fname=fields[2].strip(),
                            lname=fields[3].strip(),
                            gender=fields[4].strip(),
                            age=fields[5].strip()
                        )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        payload = {"form": form}

        return render(request, "admin/csv_form.html", payload)


admin.site.register(Student, StudentAdmin)

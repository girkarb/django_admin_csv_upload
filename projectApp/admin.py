from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .admin_view import ChildManager
from .models import LearningObjective, Payment, Child
from .forms import CsvImportForm


class LearningAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_name', 'status', 'goToProfileReviewed', 'goToNotify')

    def get_urls(self):
        """
        To fetch urls and add import csv url.
        :return:
        """

        urls = super().get_urls()
        import_csv = [path('import-csv/', self.child_import_csv), ]
        prof_review_urls = [path('update_reviewed/<stud_id>', self.updateProfileReviewed), ]
        notify_urls = [path('update_notify/<stud_id>', self.updateNotify), ]
        return import_csv + prof_review_urls + notify_urls + urls

    @mark_safe
    def goToProfileReviewed(self, obj):

        return format_html(
            '<a class="button" href="/admin/projectApp/child/update_reviewed/%s">Profile '
            'Reviewed</a>&nbsp;' % (obj.pk))

    goToProfileReviewed.short_description = 'ProfileReviewed'
    goToProfileReviewed.allow_tags = True

    @mark_safe
    def goToNotify(self, obj):

        return format_html(
            '<a class="button" href="/admin/projectApp/child/update_notify/%s">Notify</a>&nbsp;' % (obj.pk))

    goToNotify.short_description = 'Notify'
    goToNotify.allow_tags = True

    def updateProfileReviewed(self, request, stud_id):
        obj = ChildManager().updateProfileReviewed(stud_id)
        if obj == True:
            print("Profile reviewed")
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

    def updateNotify(self, request, stud_id):
        obj = ChildManager().updateNotify(stud_id)
        if obj == True:
            print("Notify")
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

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

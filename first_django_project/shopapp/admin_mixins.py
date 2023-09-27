import csv
from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest,HttpResponse


class ExportAsCSVMixin: #данный класс можно использовать, чтобы в админке проводить экспорт разных моделей. Данные в формате csv
    def export_csv(self, request:HttpRequest, queryset:QuerySet):
        meta:Options =self.model.meta
        field_names =(field.name for field in meta.fields) #чтобы собрать список из строк-названий полей этой модели

        response = HttpResponse(content_type="text/csv")   #объект, в который будут выводиться данные
        response["Content-Disposition"] = f"attachment;filename={meta} - export.csv"

        csv_writer = csv.writer(response)
        #файл для записи результата. Вместо файла используем response

        csv_writer.writerow(field_names)  #нужно записать заголовки, чтобы первой строчкой было имя каждой из колонок

        for obj in queryset:
            csv_writer.writerow([getattr(obj,field) for field in field_names])

        return response   #по команде return браузер выполняет скачивание файла

    export_csv.short_description = "Export as CSV" #назначаем описание

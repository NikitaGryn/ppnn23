from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import JsonUploadForm
from .serializers import JsonItemSerializer
from .models import JsonData
import json
from django.views.generic import ListView


class JsonUploadFormView(FormView):
    template_name = 'upload.html'
    form_class = JsonUploadForm
    success_url = reverse_lazy('upload-json')

    def form_valid(self, form):
        json_file = form.cleaned_data['json_file']
        try:
            raw_data = json.load(json_file)
        except json.JSONDecodeError:
            messages.error(self.request, "Неверный формат JSON")
            return self.form_invalid(form)

        serializer = JsonItemSerializer(data=raw_data, many=True)
        if not serializer.is_valid():
            messages.error(self.request, f"Ошибка валидации: {serializer.errors}")
            return self.form_invalid(form)

        for item in serializer.validated_data:
            JsonData.objects.create(**item)

        messages.success(self.request, "Файл успешно загружен!")
        return super().form_valid(form)


class JsonDataListView(ListView):
    model = JsonData
    template_name = 'view_data.html'
    context_object_name = 'data'

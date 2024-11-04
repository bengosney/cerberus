from vanilla import CreateView, UpdateView

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from ..filters import PetFilter
from ..forms import PetForm
from ..models import Customer, Pet
from .crud_views import Actions, CRUDViews


class PetCreateView(CreateView):
    model = Pet
    form_class = PetForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        customer = get_object_or_404(Pet, pk=kwargs["pk"])
        context = self.get_context_data(form=form, customer=customer)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=kwargs["pk"])
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.customer = customer
            self.object.save()
            form.save_m2m()
            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(form=form, customer=customer)
        return self.render_to_response(context)


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.object.customer

        return context


class PetCRUD(CRUDViews):
    model = Pet
    form_class = PetForm
    filter_class = PetFilter
    sortable_fields = ["name", "customer"]
    lookup_field = "sqid"

    @classmethod
    def url_parts(cls):
        return {
            **super().url_parts(),
            **{Actions.CREATE: f"create-for-customer/{cls.url_lookup()}/"},
        }

    @classmethod
    def get_view_class(cls, action: Actions):
        if action == Actions.CREATE:
            return PetCreateView
        if action == Actions.UPDATE:
            return PetUpdateView
        return super().get_view_class(action)

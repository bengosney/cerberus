# Third Party
from rest_framework import serializers

# Locals
from .models import Address, Booking, BookingSlot, Charge, Contact, Customer, Pet, Service, Vet

default_read_only = [
    "id",
    "created",
    "last_updated",
]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = default_read_only


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = "__all__"
        read_only_fields = default_read_only


class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
        fields = "__all__"
        read_only_fields = default_read_only


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "name",
            "cost",
            "start",
            "end",
            "created",
            "last_updated",
            "state",
            "pet",
            "service",
            "booking_slot",
            "can_move",
            "available_state_transitions",
        ]
        read_only_fields = default_read_only + [
            "state",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = default_read_only


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = default_read_only


class PetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = default_read_only


class VetSerializer(serializers.HyperlinkedModelSerializer):
    pets = PetSerializer(many=True, read_only=True)

    class Meta:
        model = Vet
        fields = "__all__"
        read_only_fields = default_read_only


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    pets = PetSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    charges = ChargeSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = default_read_only

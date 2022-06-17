# Standard Library
from enum import Enum

# Third Party
from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField

# First Party
from crm.utils import id_to_object

# Locals
from .models import Address, Booking, BookingSlot, Charge, Contact, Customer, Pet, Service, Vet

default_read_only = [
    "id",
    "created",
    "last_updated",
]


class EnumSerializer(serializers.Serializer):
    def to_representation(self, obj: Enum) -> str:
        return obj.value


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    type = EnumSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = default_read_only


class ChargeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Charge
        fields = "__all__"
        read_only_fields = default_read_only


class BookingSlotSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = BookingSlot
        fields = "__all__"
        read_only_fields = default_read_only


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            "id",
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
    id = serializers.ReadOnlyField()

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = default_read_only


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = default_read_only


class PetSerializer(TaggitSerializer, serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    tags = TagListSerializerField()
    customer_id = serializers.IntegerField(write_only=True)
    vet_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = default_read_only
        depth = 1

    @id_to_object("vet_id", Vet)
    @id_to_object("customer_id", Customer)
    def create(self, validated_data):
        return super().create(validated_data)

    @id_to_object("vet_id", Vet)
    @id_to_object("customer_id", Customer)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class VetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    pets = PetSerializer(many=True, read_only=True)

    class Meta:
        model = Vet
        fields = "__all__"
        read_only_fields = default_read_only


class CustomerSerializer(TaggitSerializer, serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    pets = PetSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    charges = ChargeSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    vet_id = serializers.IntegerField(write_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = default_read_only
        depth = 1

    @id_to_object("vet_id", Vet)
    def create(self, validated_data):
        return super().create(validated_data)

    @id_to_object("vet_id", Vet)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class TagSerializer(serializers.BaseSerializer):
    def to_representation(self, obj: Tag) -> str:
        return obj.name

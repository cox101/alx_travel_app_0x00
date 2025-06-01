# listings/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model with all fields exposed.
    Includes read-only protection for auto-generated fields.
    """
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model with custom create logic.
    Handles price calculation automatically and protects read-only fields.
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True,
        help_text="ID of the listing being booked"
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'listing', 'listing_id',
            'check_in', 'check_out', 'number_of_guests',
            'total_price', 'created_at', 'status'
        ]
        read_only_fields = [
            'id', 'user', 'listing',
            'total_price', 'created_at', 'status'
        ]
        extra_kwargs = {
            'check_in': {'help_text': 'Booking start date (YYYY-MM-DD)'},
            'check_out': {'help_text': 'Booking end date (YYYY-MM-DD)'},
            'number_of_guests': {'min_value': 1}
        }

    def validate(self, data):
        """Validate booking dates and guest count"""
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        if data['listing'].max_guests < data['number_of_guests']:
            raise serializers.ValidationError(
                f"This listing accommodates maximum {data['listing'].max_guests} guests"
            )
        return data

    def create(self, validated_data):
        """Create booking with automatic price calculation"""
        listing = validated_data['listing']
        duration = (validated_data['check_out'] - validated_data['check_in']).days
        
        return Booking.objects.create(
            user=self.context['request'].user,
            listing=listing,
            total_price=listing.price_per_night * duration * validated_data['number_of_guests'],
            **validated_data
        )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model with read-only user protection
    and listing relationship handling.
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True,
        help_text="ID of the listing being reviewed"
    )

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'listing', 'listing_id',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'listing', 'created_at']
        extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5},
            'comment': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        """Create review with automatic user assignment"""
        return Review.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
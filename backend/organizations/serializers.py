from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        from django.utils.text import slugify
        
        # generate slug automatically
        name = validated_data.get('name')
        base_slug = slugify(name)
        slug = base_slug
        count = 1
        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
            
        validated_data['slug'] = slug
        return super().create(validated_data)

from rest_framework import serializers

from .models import Ticket, Tag


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['reporter'] = instance.reporter.get_full_name()
        data['assignee'] = instance.assignee.get_full_name() if instance.assignee else 'None'
        data['tags'] = ['{} '.format(tag[0]) for tag in instance.tag_set.all().values_list('tag')]
        return data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        tag, created = Tag.objects.get_or_create(
            tag=validated_data['tag']
        )
        tag.ticket.add(validated_data['ticket'][0])
        tag.save()
        return tag

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

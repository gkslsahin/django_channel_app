from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Channel(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
            child_list_content = self.children_content.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        for child_content in child_list_content:
            children.extend(child_content.get_all_children())
        return children

    def get_content_children(self):
        children = [self]
        try:
            child_list = self.children_content.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("A cannot have itself or one of its' children as parent")


class SubChannel(models.Model):
    channel = models.ForeignKey(Channel,
                                on_delete=models.CASCADE, related_name="children")
    title = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    info_sub_channel = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children_sub.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("A cannot have itself or one of its' children as parent")


class Content(models.Model):
    channel = models.ForeignKey(Channel,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name="children_content")
    sub_channel = models.ForeignKey(SubChannel,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name="children_sub"
                                    )
    name = models.CharField(max_length=150)
    image = models.CharField(max_length=150)
    language = models.CharField(max_length=150)
    content_info = models.CharField(max_length=150)
    file = models.CharField(max_length=300)
    rate = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children_sub.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def get_content_cildren(self):
        children = [self]
        try:
            child_list = self.children_content.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def __str__(self):
        return self.name

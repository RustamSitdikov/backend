#!/usr/bin/env python

from wtforms import Form, validators, FormField, StringField, IntegerField, FieldList
import inspect


class SearchUsersForm(Form):
    query = StringField(validators=[validators.data_required()])
    limit = IntegerField(default=10, validators=[validators.optional()])


class SearchChatsForm(Form):
    query = StringField(validators=[validators.data_required()])
    limit = IntegerField(default=10, validators=[validators.optional()])


class CreatePersonalChatForm(Form):
    companion_id = IntegerField(validators=[validators.data_required()])
    user_id = IntegerField(validators=[validators.data_required()])


class CreateGroupChatForm(Form):
    topic = StringField(validators=[validators.data_required()])


class AddMembersGroupChatForm(Form):
    chat_id = IntegerField(validators=[validators.data_required()])
    user_ids = FieldList(FormField(IntegerField), validators=[validators.data_required()])


class LeaveGroupChatForm(Form):
    user_id = IntegerField(validators=[validators.data_required()])
    chat_id = IntegerField(validators=[validators.data_required()])


class SendMessageForm(Form):
    user_id = IntegerField(validators=[validators.data_required()])
    chat_id = IntegerField(validators=[validators.data_required()])
    content = StringField(validators=[validators.data_required()])
    attachment_id = IntegerField(default=None, validators=[validators.optional()])


class ReadMessageForm(Form):
    user_id = IntegerField(validators=[validators.data_required()])
    message_id = IntegerField(validators=[validators.data_required()])


class ListMessagesForm(Form):
    chat_id = IntegerField(validators=[validators.data_required()])
    limit = IntegerField(default=10, validators=[validators.optional()])


class UploadFileForm(Form):
    user_id = IntegerField(validators=[validators.data_required()])
    chat_id = IntegerField(validators=[validators.data_required()])
    content = StringField(validators=[validators.data_required()])
    mime_type = StringField(validators=[validators.data_required()])


class DownloadFileForm(Form):
    key = StringField(validators=[validators.data_required()])


class GenerateKeyForm(Form):
    key = StringField(validators=[validators.data_required()])
    message = StringField(validators=[validators.data_required()])


class GetFileForm(Form):
    key = StringField(validators=[validators.data_required()])


def to_kwargs(function, args, kwargs):
    names, args_name, kwargs_name, defaults = inspect.getargspec(function)

    # assign basic args
    params = {}
    if args_name:
        basic_arg_count = len(names)
        params.update(zip(names[:], args))  # zip stops at shorter sequence
        params[args_name] = args[basic_arg_count:]
    else:
        params.update(zip(names, args))

    # assign kwargs given
    if kwargs_name:
        params[kwargs_name] = {}
        for kw, value in kwargs.iteritems():
            if kw in names:
                params[kw] = value
            else:
                params[kwargs_name][kw] = value
    else:
        params.update(kwargs)

    # assign defaults
    if defaults:
        for pos, value in enumerate(defaults):
            if names[-len(defaults) + pos] not in params:
                params[names[-len(defaults) + pos]] = value

    return params


class wtform(object):
    def __init__(self, factory=Form):
        self.factory = factory

    def __call__(self, func, *args, **kwargs):
        def decorator(*args, **kwargs):
            params = to_kwargs(func, args, kwargs)
            form = self.factory(**params)
            if form.validate():
                return func(*args, **kwargs)

        return decorator

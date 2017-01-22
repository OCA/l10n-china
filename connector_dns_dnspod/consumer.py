# -*- coding: utf-8 -*-
# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.connector.event import (on_record_write,
                                            on_record_create
                                            )
from .unit.export_synchronizer import export_record

_MODEL_NAMES = ('dns.domain', 'dns.record')
_MODEL_NAMES_RECORD = ('dns.record')


@on_record_create(model_names=_MODEL_NAMES)
def create_domain_all_bindings(session, model_name, record_id, fields=None):
    """ Create a job which export all the bindings of a record."""
    if session.context.get('connector_no_export'):
        return
    model = session.pool.get(model_name)
    record = model.browse(
        session.cr,
        session.uid,
        record_id,
        context=session.context
    )
    export_record.delay(
        session,
        record._model._name,
        record.id,
        fields=fields
    )


@on_record_write(model_names=_MODEL_NAMES_RECORD)
def write_export_all_bindings(session, model_name, record_id, fields=None):
    """ Create a job which export all the bindings of a record."""
    if session.context.get('connector_no_export'):
        return
    model = session.pool.get(model_name)
    record = model.browse(
        session.cr,
        session.uid,
        record_id,
        context=session.context
    )

    export_record.delay(
        session,
        record._model._name,
        record.id,
        fields=fields,
        method='write'
    )

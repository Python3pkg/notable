# Python imports
from collections import OrderedDict
import datetime
import logging
import os
import sqlite3
import sys
import uuid

# Constants
log = logging.getLogger(__name__)
mod = sys.modules.get(__name__)
path = os.path.expanduser('~/.notes/notes.sqlite3')

def note(exclude=None, actual=False):
    exclude = exclude or []
    model = [('uid', 'string'),
             ('created', 'string'),
             ('updated', 'string'),
             ('subject', None),
             ('tags', 'string'),
             ('content', 'string'),
             ('password', 'string'),
            ]
    n = OrderedDict((k, v) for k, v in model if not k in exclude)
    if actual:
        now = datetime.datetime.now()
        uid = uuid.uuid4().hex
        n.update(uid=uid, created=now, updated=now)
    return n

def create_note(n):
    c = conn()
    sql = 'INSERT INTO notes (%s) VALUES (%s);'
    cols = ','.join(k for k, t in n.items() if t)
    values = ','.join('?' for k, t in n.items() if t)
    sql = sql % (cols, values)
    c.execute(sql, [v for v in n.values() if not v is None])
    return c.commit()

def conn():
    d = os.path.dirname(path)
    _ = os.makedirs(d) if not os.path.exists(d) else None
    return sqlite3.connect(path)

def calculate_subject(row):
    return row.get('content').split('\n')[0]

def columns(n, row):
    for k, _ in n.items():
        yield dict(v=row.get(k, getattr(mod, 'calculate_subject')(row)))

def dict_factory(c, row):
    return dict((col[0], row[i]) for i, col in enumerate(c.description))

def fields(n):
    for k, v in n.items():
        yield dict(id=k, label=k.capitalize(), type=v)

def rows(n, rs):
    for row in rs:
        yield dict(c=list(columns(n, row)))

def create_schema(c):
    pairs = [' '.join(pair) for pair in note().items() if pair[1]]
    sql ='CREATE TABLE notes (%s);' % ','.join(pairs)
    try:
        c.execute(sql)
    except sqlite3.OperationalError, ex:
        log.warning(ex)

def search(s):
    terms = s.split() if s else []
    n = note(exclude=['password'])
    where = ['1=1'] + ["content LIKE '%{0}%'".format(t) for t in terms]
    sql = 'SELECT %s FROM notes WHERE %s;'
    sql = sql % (','.join(k for k, v in n.items() if v), ' AND '.join(where))
    log.warn(sql)
    c = conn()
    c.row_factory = dict_factory
    _cols = list(fields(n))
    _rows = list(rows(n, c.cursor().execute(sql)))
    return dict(cols=_cols, rows=_rows)

def prepare():
    create_schema(conn())
